from abc import abstractmethod
from fastapi.responses import JSONResponse
from typing import Protocol


class IDashboardController(Protocol):
    @abstractmethod
    async def get_user_movement_map(
            self,
            account_id: int,
    ) -> JSONResponse: pass


class IDashboardService(Protocol):
    @abstractmethod
    async def get_user_movement_map(
            self,
            account_id: int,
    ) -> list[dict]: pass
