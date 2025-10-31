from abc import abstractmethod
from fastapi.responses import JSONResponse
from typing import Protocol


class IDashboardController(Protocol):
    @abstractmethod
    async def get_user_movement_map(
            self,
            account_id: int,
            hours: int = 24,
    ) -> JSONResponse: pass


class IDashboardService(Protocol):
    @abstractmethod
    async def get_user_movement_map(
            self,
            account_id: int,
            hours: int = 24,
    ) -> list[dict]: pass
