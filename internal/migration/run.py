import asyncio
import sys
from contextvars import ContextVar
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent.parent))

from infrastructure.telemetry.telemetry import Telemetry
from internal.config.config import Config
from internal.migration.manager import MigrationManager


async def main():
    pass


if __name__ == "__main__":
    asyncio.run(main())