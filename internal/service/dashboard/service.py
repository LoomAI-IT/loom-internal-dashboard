from internal import interface
from pkg.trace_wrapper import traced_method


class DashboardService(interface.IDashboardService):
    def __init__(
            self,
            tel: interface.ITelemetry,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()

    @traced_method()
    async def get_user_movement_map(
            self,
            account_id: int,
    ) -> int:
        pass