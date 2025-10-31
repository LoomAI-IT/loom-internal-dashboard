import asyncio

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pkg.client.client import AsyncHTTPClient
import re
import json

from internal import interface


class LokiClient(interface.ILokiClient):

    def __init__(
            self,
            host: str,
            port: int,
    ):
        self.client = AsyncHTTPClient(
            host,
            port,
            prefix="/loki/api/v1",
            use_tracing=True,
        )

    async def query_logs(
            self,
            filters: dict = None,
            content_filters: dict = None,
            search_text: str | list[str] = None,
            search_mode: str = "and",
            start_time: datetime = None,
            end_time: datetime = None,
            direction: str = "backward",
            parse_json: bool = True,
            limit: int = None,
            batch_size: int = 5000
    ) -> list[dict]:
        """
        Получение логов с фильтрацией и автоматической пагинацией

        Args:
            filters: Словарь с label selectors (например, {"service_name": "my-service"})
            content_filters: Словарь для поиска в содержимом логов (например, {"account_id": "1"})
            search_text: Текст для поиска в логах (строка или список строк)
            search_mode: Режим поиска - "and" (все строки должны присутствовать) или "or" (хотя бы одна)
            start_time: Начало временного диапазона (по умолчанию - 1 час назад)
            end_time: Конец временного диапазона (по умолчанию - сейчас)
            direction: Направление сортировки ("backward" или "forward")
            parse_json: Автоматически парсить JSON из message (по умолчанию True)
            limit: Максимальное количество логов (None = без ограничений, получить все)
            batch_size: Размер одного запроса к Loki (по умолчанию 5000, не рекомендуется увеличивать)

        Returns:
            Список логов в виде словарей
        """
        if filters is None:
            filters = {}
        if content_filters is None:
            content_filters = {}

        if end_time is None:
            end_time = datetime.now()
        if start_time is None:
            start_time = end_time - timedelta(hours=1)

        query = self._build_logql_query(filters, content_filters, search_text, search_mode)

        all_logs = []
        current_end_time = end_time

        # Пагинация: делаем запросы пока есть данные или пока не достигнем лимита
        while True:
            # Определяем размер текущего батча
            if limit is not None:
                remaining = limit - len(all_logs)
                if remaining <= 0:
                    break
                current_batch_size = min(batch_size, remaining)
            else:
                current_batch_size = batch_size

            params = {
                "query": query,
                "start": int(start_time.timestamp() * 1e9),
                "end": int(current_end_time.timestamp() * 1e9),
                "direction": direction,
                "limit": current_batch_size
            }

            try:
                response = await self.client.get(
                    "/query_range",
                    params=params,
                )

                data = response.json()

                batch_logs = []
                if data.get("status") == "success":
                    results = data.get("data", {}).get("result", [])

                    for stream in results:
                        labels = stream.get("stream", {})
                        values = stream.get("values", [])

                        for value in values:
                            timestamp_ns, log_line = value

                            log_entry = {
                                "timestamp": datetime.fromtimestamp(int(timestamp_ns) / 1e9),
                                "timestamp_ns": timestamp_ns,
                                "message": log_line,
                            }

                            log_entry.update(labels)

                            if parse_json:
                                parsed_fields = self._parse_log_line(log_line)
                                if parsed_fields:
                                    log_entry.update(parsed_fields)

                            batch_logs.append(log_entry)

                # Если получили меньше логов чем запрашивали, значит это последний батч
                if len(batch_logs) < current_batch_size:
                    all_logs.extend(batch_logs)
                    break

                all_logs.extend(batch_logs)

                # Если достигли лимита, останавливаемся
                if limit is not None and len(all_logs) >= limit:
                    break

                # Обновляем end_time для следующего запроса
                # Берём timestamp самого старого лога из текущего батча
                if batch_logs:
                    if direction == "backward":
                        # При backward сортировке логи идут от новых к старым
                        oldest_log = batch_logs[-1]
                        # Вычитаем 1 наносекунду чтобы не получить тот же лог снова
                        current_end_time = datetime.fromtimestamp(int(oldest_log["timestamp_ns"]) / 1e9 - 0.000000001)
                    else:
                        # При forward сортировке логи идут от старых к новым
                        newest_log = batch_logs[-1]
                        # Для forward меняем start_time
                        start_time = datetime.fromtimestamp(int(newest_log["timestamp_ns"]) / 1e9 + 0.000000001)
                else:
                    break

            except Exception as e:
                raise e

        return all_logs

    def _parse_log_line(self, log_line: str) -> Optional[Dict[str, Any]]:
        try:
            parsed = json.loads(log_line)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass

        try:
            fields = {}
            pattern = r'(\w+)=("(?:[^"\\]|\\.)*"|[^\s]+)'
            matches = re.findall(pattern, log_line)

            if matches:
                for key, value in matches:
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]

                    try:
                        if '.' in value:
                            fields[key] = float(value)
                        else:
                            fields[key] = int(value)
                    except ValueError:
                        if value.lower() in ('true', 'false'):
                            fields[key] = value.lower() == 'true'
                        else:
                            fields[key] = value

                if fields:
                    return fields
        except Exception:
            pass

        return None

    def _build_logql_query(
            self,
            filters: Dict[str, str],
            content_filters: Dict[str, str],
            search_text: Optional[str | List[str]] = None,
            search_mode: str = "and"
    ) -> str:

        if not filters:
            query = '{service_name=~".+"}'
        else:
            label_selectors = []
            for key, value in filters.items():
                label_selectors.append(f'{key}="{value}"')
            query = "{" + ", ".join(label_selectors) + "}"

        if content_filters:
            for key, value in content_filters.items():
                query += f' | {key}=`{value}`'

        if search_text:
            if isinstance(search_text, str):
                query += f' |= "{search_text}"'
            elif isinstance(search_text, list) and search_text:
                if search_mode.lower() == "and":
                    for text in search_text:
                        query += f' |= "{text}"'
                elif search_mode.lower() == "or":
                    escaped_texts = [re.escape(text) for text in search_text]
                    regex_pattern = "|".join(escaped_texts)
                    query += f' |~ "({regex_pattern})"'
                else:
                    raise ValueError(f"Неподдерживаемый режим поиска: {search_mode}. Используйте 'and' или 'or'")

        return query

async def main() -> None:
    loki = LokiClient(
        "62.109.23.129",
        3100
    )
    logs = await loki.query_logs(
        filters={"service_name": "loom-tg-bot"},
        content_filters={"account_id": 52},
        search_text=["Service"],
    )
    print(logs, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
