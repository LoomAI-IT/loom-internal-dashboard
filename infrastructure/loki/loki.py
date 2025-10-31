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
            search_text: str | list[str] = None,
            search_mode: str = "and",
            limit: int = 100,
            start_time: datetime = None,
            end_time: datetime = None,
            direction: str = "backward",
            parse_json: bool = True
    ) -> list[dict]:
        """
        Получение логов с фильтрацией

        Args:
            filters: Словарь с полями для фильтрации (например, {"service_name": "my-service"})
            search_text: Текст для поиска в логах (строка или список строк)
            search_mode: Режим поиска - "and" (все строки должны присутствовать) или "or" (хотя бы одна)
            limit: Максимальное количество логов (по умолчанию 100)
            start_time: Начало временного диапазона (по умолчанию - 1 час назад)
            end_time: Конец временного диапазона (по умолчанию - сейчас)
            direction: Направление сортировки ("backward" или "forward")
            parse_json: Автоматически парсить JSON из message (по умолчанию True)

        Returns:
            Список логов в виде словарей
        """
        if filters is None:
            filters = {}

        if end_time is None:
            end_time = datetime.now()
        if start_time is None:
            start_time = end_time - timedelta(hours=1)

        query = self._build_logql_query(filters, search_text, search_mode)

        params = {
            "query": query,
            "limit": limit,
            "start": int(start_time.timestamp() * 1e9),
            "end": int(end_time.timestamp() * 1e9),
            "direction": direction
        }

        try:
            response = await self.client.get(
                "/query_range",
                params=params,
            )

            data = response.json()

            logs = []
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

                        logs.append(log_entry)

            return logs

        except Exception as e:
            raise e

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
            search_text: Optional[str | List[str]] = None,
            search_mode: str = "and"
    ) -> str:

        if not filters:
            query = "{}"
        else:
            label_selectors = [f'{key}="{value}"' for key, value in filters.items()]
            query = "{" + ", ".join(label_selectors) + "}"

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
        search_text=["Service"],
    )
    print(logs, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
