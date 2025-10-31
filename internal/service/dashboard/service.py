import re
from typing import Optional

from infrastructure.loki.loki import LokiClient
from internal import interface
from internal.common.methods_map import methods_map
from pkg.log_wrapper import auto_log
from pkg.trace_wrapper import traced_method


class DashboardService(interface.IDashboardService):
    def __init__(
            self,
            tel: interface.ITelemetry,
            loki: LokiClient,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.loki = loki

    @traced_method()
    @auto_log()
    async def get_user_movement_map(
            self,
            account_id: int,
    ) -> list[dict]:
        logs = await self.loki.query_logs(
            filters={
                "service_name": "loom-tg-bot",
            },
            content_filters={
                "account_id": account_id,
            },
            search_text=["Service"],
        )
        self.logger.info('loki', {"logs": logs})

        spans_map = {}
        for log in logs:
            span_id = log.get("span_id")
            if not span_id:
                continue

            message = log.get("message", "")
            parsed = self.parse_log_message(message)
            if not parsed:
                continue

            operation_type, service_name, method_name = parsed

            if span_id not in spans_map:
                spans_map[span_id] = {}

            spans_map[span_id][operation_type] = {
                "log": log,
                "service": service_name,
                "method": method_name,
            }

        movement_map = []
        for span_id, operations in spans_map.items():
            if "Начало" not in operations or "Завершение" not in operations:
                continue

            start_data = operations["Начало"]
            end_data = operations["Завершение"]

            start_log = start_data["log"]
            end_log = end_data["log"]

            # Извлекаем данные
            start_time = start_log.get("timestamp")
            end_time = end_log.get("timestamp")

            if not start_time or not end_time:
                continue

            duration_seconds = (end_time - start_time).total_seconds()

            service_ru, method_ru = self.get_russian_names(
                start_data["service"],
                start_data["method"]
            )

            movement_map.append({
                "account_id": start_log.get("account_id"),
                "telegram_username": start_log.get("telegram_user_username"),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration": self.format_duration(duration_seconds),
                "service": service_ru,
                "method": method_ru,
            })

        movement_map.sort(key=lambda x: x["start_time"])

        return movement_map

    def parse_log_message(self, message: str) -> Optional[tuple[str, str, str]]:
        """
        Парсит сообщение лога и извлекает тип операции (Начало/Завершение), сервис и метод.

        Пример: "loom-tg-bot | Начало MainMenuService.handle_go_to_personal_profile"
        Возвращает: ("Начало", "MainMenuService", "handle_go_to_personal_profile")
        """
        pattern = r"(Начало|Завершение)\s+(\w+)\.(\w+)"
        match = re.search(pattern, message)
        if match:
            return match.group(1), match.group(2), match.group(3)
        return None

    def format_duration(self, seconds: float) -> str:
        """
        Форматирует длительность в человеческий формат.

        Примеры:
        - 1.648 -> "1.65 сек"
        - 65.2 -> "1 мин 5 сек"
        - 3665 -> "1 ч 1 мин"
        """
        if seconds < 1:
            return f"{seconds * 1000:.0f} мс"
        elif seconds < 60:
            return f"{seconds:.2f} сек"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            if remaining_seconds > 0:
                return f"{minutes} мин {remaining_seconds} сек"
            return f"{minutes} мин"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            if minutes > 0:
                return f"{hours} ч {minutes} мин"
            return f"{hours} ч"

    def get_russian_names(self, service_name: str, method_name: str) -> tuple[str, str]:
        """
        Получает русские названия сервиса и метода из methods_map.

        Если название не найдено, возвращает оригинальное.
        """
        service_ru = service_name
        method_ru = method_name

        if service_name in methods_map:
            service_ru = methods_map[service_name].get("ru_name", service_name)
            methods = methods_map[service_name].get("methods", {})
            method_ru = methods.get(method_name, method_name)

        return service_ru, method_ru
