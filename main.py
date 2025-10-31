from contextvars import ContextVar

import uvicorn

from infrastructure.loki.loki import LokiClient
from infrastructure.telemetry.telemetry import Telemetry, AlertManager

from pkg.client.internal.loom_authorization.client import LoomAuthorizationClient
from internal.controller.http.middlerware.middleware import HttpMiddleware
from internal.controller.http.handler.dashboard.handler import DashboardController

from internal.service.dashboard.service import DashboardService

from internal.app.http.app import NewHTTP
from internal.config.config import Config

cfg = Config()

log_context: ContextVar[dict] = ContextVar('log_context', default={})

alert_manager = AlertManager(
    cfg.alert_tg_bot_token,
    cfg.service_name,
    cfg.alert_tg_chat_id,
    cfg.alert_tg_chat_thread_id,
    cfg.grafana_url,
    cfg.monitoring_redis_host,
    cfg.monitoring_redis_port,
    cfg.monitoring_redis_db,
    cfg.monitoring_redis_password,
)


tel = Telemetry(
    cfg.log_level,
    cfg.root_path,
    cfg.environment,
    cfg.service_name,
    cfg.service_version,
    cfg.otlp_host,
    cfg.otlp_port,
    log_context,
    alert_manager
)

# Инициализация внешних клиентов
loom_authorization_client = LoomAuthorizationClient(
    tel=tel,
    host=cfg.loom_authorization_host,
    port=cfg.loom_authorization_port,
    log_context=log_context
)

loki = LokiClient(
    cfg.loki_host,
    cfg.loki_port,
)

# Инициализация сервисов
dashboard_service = DashboardService(
    tel=tel,
    loki=loki
)

# Инициализация контроллеров
dashboard_controller = DashboardController(tel, dashboard_service)

# Инициализация middleware
http_middleware = HttpMiddleware(tel, loom_authorization_client, cfg.prefix, log_context)

app = NewHTTP(
    dashboard_controller=dashboard_controller,
    http_middleware=http_middleware,
    prefix=cfg.prefix,
)

if __name__ == "__main__":
    if cfg.environment == "prod":
        workers = 2
    else:
        workers = 1

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(cfg.http_port),
        workers=workers,
        loop="uvloop",
        access_log=False,
    )
