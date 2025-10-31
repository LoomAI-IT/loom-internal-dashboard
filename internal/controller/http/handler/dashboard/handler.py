from fastapi.responses import JSONResponse

from internal import interface
from pkg.log_wrapper import auto_log

from pkg.trace_wrapper import traced_method


class DashboardController(interface.IDashboardController):
    def __init__(
            self,
            tel: interface.ITelemetry,
            dashboard_service: interface.IDashboardService,
    ):
        self.tracer = tel.tracer()
        self.logger = tel.logger()
        self.dashboard_service = dashboard_service
    
    @auto_log()
    @traced_method()
    async def get_user_movement_map(
            self,
            account_id: int,
    ) -> JSONResponse:
        user_movement_map = await self.dashboard_service.get_user_movement_map(
            account_id=account_id,
        )

        return JSONResponse(
            status_code=201,
            content=user_movement_map
        )
