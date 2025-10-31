from infrastructure.loki.loki import LokiClient
from internal import interface
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
    async def get_user_movement_map(
            self,
            account_id: int,
    ) -> list[dict]:
        logs = await self.loki.query_logs(
            filters={
                "service_name": "loom-tg-bot",
                "account_id": account_id,
            },
            search_text=["Начало", "Service"],
        )

        return logs
