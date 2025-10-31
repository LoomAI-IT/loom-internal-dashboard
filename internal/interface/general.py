from abc import abstractmethod
from datetime import datetime
from typing import Protocol, Sequence, Any

from fastapi import FastAPI

from opentelemetry.metrics import Meter
from opentelemetry.trace import Tracer


class IOtelLogger(Protocol):
    @abstractmethod
    def debug(self, message: str, fields: dict = None) -> None:
        pass

    @abstractmethod
    def info(self, message: str, fields: dict = None) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, fields: dict = None) -> None:
        pass

    @abstractmethod
    def error(self, message: str, fields: dict = None) -> None:
        pass


class ITelemetry(Protocol):
    @abstractmethod
    def tracer(self) -> Tracer:
        pass

    @abstractmethod
    def meter(self) -> Meter:
        pass

    @abstractmethod
    def logger(self) -> IOtelLogger:
        pass


class IHttpMiddleware(Protocol):
    @abstractmethod
    def trace_middleware01(self, app: FastAPI): pass

    @abstractmethod
    def logger_middleware02(self, app: FastAPI): pass

    @abstractmethod
    def authorization_middleware03(self, app: FastAPI): pass


class IRedis(Protocol):
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = None) -> bool: pass

    @abstractmethod
    async def get(self, key: str, default: Any = None) -> Any: pass

class ILokiClient(Protocol):
    @abstractmethod
    async def query_logs(
            self,
            filters: dict = None,
            content_filters: dict = None,
            search_text: str | list[str] = None,
            search_mode: str = "and",
            limit: int = 100,
            start_time: datetime = None,
            end_time: datetime = None,
            direction: str = "backward",
            parse_json: bool = True
    ) -> list[dict]: pass