import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pkg.client.client import AsyncHTTPClient
import re


class LokiClient:

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
            filters: Optional[Dict[str, str]] = None,
            search_text: Optional[str | List[str]] = None,
            search_mode: str = "and",  # "and" или "or"
            limit: int = 100,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            direction: str = "backward"
    ) -> List[Dict[str, Any]]:
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

        Returns:
            Список логов в виде словарей
        """
        if filters is None:
            filters = {}

        # Устанавливаем временной диапазон по умолчанию
        if end_time is None:
            end_time = datetime.now()
        if start_time is None:
            start_time = end_time - timedelta(hours=1)

        # Формируем LogQL запрос
        query = self._build_logql_query(filters, search_text, search_mode)

        # Параметры запроса
        params = {
            "query": query,
            "limit": limit,
            "start": int(start_time.timestamp() * 1e9),  # Nanoseconds
            "end": int(end_time.timestamp() * 1e9),
            "direction": direction
        }

        try:
            response = await self.client.get(
                "/query_range",
                params=params,
            )

            data = response.json()

            # Парсим результаты
            logs = []
            if data.get("status") == "success":
                results = data.get("data", {}).get("result", [])

                for stream in results:
                    labels = stream.get("labels", {})
                    values = stream.get("values", [])

                    for value in values:
                        timestamp_ns, log_line = value
                        log_entry = {
                            "timestamp": datetime.fromtimestamp(int(timestamp_ns) / 1e9),
                            "timestamp_ns": timestamp_ns,
                            "message": log_line,
                            "labels": labels
                        }
                        logs.append(log_entry)

            return logs

        except Exception as e:
            raise e

    def _build_logql_query(
            self,
            filters: Dict[str, str],
            search_text: Optional[str | List[str]] = None,
            search_mode: str = "and"
    ) -> str:
        """
        Формирует LogQL запрос

        Args:
            filters: Фильтры по меткам
            search_text: Текст для поиска (строка или список)
            search_mode: Режим поиска ("and" или "or")

        Returns:
            Строка LogQL запроса
        """
        if not filters:
            query = "{}"
        else:
            # Формируем селектор меток
            label_selectors = [f'{key}="{value}"' for key, value in filters.items()]
            query = "{" + ", ".join(label_selectors) + "}"

        # Добавляем фильтр по тексту
        if search_text:
            if isinstance(search_text, str):
                # Один текст
                query += f' |= "{search_text}"'
            elif isinstance(search_text, list) and search_text:
                # Несколько текстов
                if search_mode.lower() == "and":
                    # AND логика: все строки должны присутствовать
                    for text in search_text:
                        query += f' |= "{text}"'
                elif search_mode.lower() == "or":
                    # OR логика: хотя бы одна строка (через regex)
                    # Экранируем специальные символы regex
                    escaped_texts = [re.escape(text) for text in search_text]
                    regex_pattern = "|".join(escaped_texts)
                    query += f' |~ "({regex_pattern})"'
                else:
                    raise ValueError(f"Неподдерживаемый режим поиска: {search_mode}. Используйте 'and' или 'or'")

        return query