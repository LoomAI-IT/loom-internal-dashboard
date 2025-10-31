import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class LokiClient:

    def __init__(self, url: str, timeout: int = 30):
        self.url = url.rstrip('/')
        self.timeout = timeout
        self.query_range_endpoint = f"{self.url}/loki/api/v1/query_range"
        self.query_endpoint = f"{self.url}/loki/api/v1/query"
        self.labels_endpoint = f"{self.url}/loki/api/v1/labels"

    def _build_logql_query(self, filters: Dict[str, str], search_text: Optional[str] = None) -> str:
        """
        Построение LogQL запроса из словаря фильтров

        Args:
            filters: Словарь с метками и их значениями
            search_text: Текст для поиска в логах (опционально)

        Returns:
            Строка LogQL запроса
        """
        if not filters:
            query = "{}"
        else:
            # Формируем селектор меток
            label_selectors = [f'{key}="{value}"' for key, value in filters.items()]
            query = "{" + ", ".join(label_selectors) + "}"

        # Добавляем фильтр по тексту, если указан
        if search_text:
            query += f' |= "{search_text}"'

        return query

    def query_logs(
            self,
            filters: Optional[Dict[str, str]] = None,
            search_text: Optional[str] = None,
            limit: int = 100,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            direction: str = "backward"
    ) -> List[Dict[str, Any]]:
        """
        Получение логов с фильтрацией

        Args:
            filters: Словарь с полями для фильтрации (например, {"service_name": "my-service"})
            search_text: Текст для поиска в логах
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
        query = self._build_logql_query(filters, search_text)

        # Параметры запроса
        params = {
            "query": query,
            "limit": limit,
            "start": int(start_time.timestamp() * 1e9),  # Nanoseconds
            "end": int(end_time.timestamp() * 1e9),
            "direction": direction
        }

        try:
            response = requests.get(
                self.query_range_endpoint,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()

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

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к Loki: {e}")
            return []

    def query_instant(
            self,
            filters: Optional[Dict[str, str]] = None,
            search_text: Optional[str] = None,
            limit: int = 100,
            time: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Мгновенный запрос логов (в определенный момент времени)

        Args:
            filters: Словарь с полями для фильтрации
            search_text: Текст для поиска в логах
            limit: Максимальное количество логов
            time: Момент времени для запроса (по умолчанию - сейчас)

        Returns:
            Список логов в виде словарей
        """
        if filters is None:
            filters = {}

        if time is None:
            time = datetime.now()

        query = self._build_logql_query(filters, search_text)

        params = {
            "query": query,
            "limit": limit,
            "time": int(time.timestamp() * 1e9)
        }

        try:
            response = requests.get(
                self.query_endpoint,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
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

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к Loki: {e}")
            return []

    def get_labels(self) -> List[str]:
        """
        Получение списка всех доступных меток (labels)

        Returns:
            Список названий меток
        """
        try:
            response = requests.get(
                self.labels_endpoint,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            if data.get("status") == "success":
                return data.get("data", [])
            return []

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении меток: {e}")
            return []

    def get_label_values(self, label: str) -> List[str]:
        """
        Получение всех значений для указанной метки

        Args:
            label: Название метки

        Returns:
            Список значений метки
        """
        try:
            response = requests.get(
                f"{self.labels_endpoint}/{label}/values",
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            if data.get("status") == "success":
                return data.get("data", [])
            return []

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении значений метки: {e}")
            return []


# Пример использования
if __name__ == "__main__":
    # Создаем клиент
    client = LokiClient("http://localhost:3100")

    # Пример 1: Получение логов с фильтрами
    print("=== Пример 1: Логи с фильтрами ===")
    logs = client.query_logs(
        filters={
            "service_name": "loom-tg-bot",
            "detected_level": "INFO"
        },
        limit=10,
        start_time=datetime.now() - timedelta(hours=2)
    )

    for log in logs[:3]:  # Показываем первые 3
        print(f"{log['timestamp']}: {log['message']}")
        print(f"  Labels: {log['labels']}")
        print()

    # Пример 2: Поиск по тексту
    print("=== Пример 2: Поиск по тексту ===")
    logs = client.query_logs(
        filters={
            "service_name": "loom-tg-bot"
        },
        search_text="OrganizationMenuService",
        limit=5
    )

    print(f"Найдено логов: {len(logs)}")

    # Пример 3: Логи определенного пользователя
    print("\n=== Пример 3: Логи пользователя ===")
    logs = client.query_logs(
        filters={
            "service_name": "loom-tg-bot",
            "telegram_user_username": "gommgo"
        },
        limit=5,
        start_time=datetime.now() - timedelta(hours=24)
    )

    print(f"Найдено логов пользователя: {len(logs)}")

    # Пример 4: Получение всех доступных меток
    print("\n=== Пример 4: Доступные метки ===")
    labels = client.get_labels()
    print(f"Доступные метки: {labels[:10]}...")  # Первые 10

    # Пример 5: Получение значений метки
    print("\n=== Пример 5: Значения метки service_name ===")
    values = client.get_label_values("service_name")
    print(f"Значения: {values}")