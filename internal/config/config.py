import os


class Config:
    def __init__(self):
        # Service configuration
        self.environment = os.getenv("ENVIRONMENT", "dev")
        self.service_name = os.getenv("LOOM_INTERNAL_DASHBOARD_CONTAINER_NAME", "loom-employee")
        self.http_port = os.getenv("LOOM_INTERNAL_DASHBOARD_PORT", "8000")
        self.service_version = os.getenv("SERVICE_VERSION", "1.0.0")
        self.root_path = os.getenv("ROOT_PATH", "/")
        self.prefix = os.getenv("LOOM_INTERNAL_DASHBOARD_PREFIX", "/api/internal-dashboard")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        self.interserver_secret_key = os.getenv("LOOM_INTERSERVER_SECRET_KEY")

        # Настройки телеметрии
        self.alert_tg_bot_token = os.getenv("LOOM_ALERT_TG_BOT_TOKEN", "")
        self.alert_tg_chat_id = int(os.getenv("LOOM_ALERT_TG_CHAT_ID", "0"))
        self.alert_tg_chat_thread_id = int(os.getenv("LOOM_ALERT_TG_CHAT_THREAD_ID", "0"))
        self.grafana_url = os.getenv("LOOM_GRAFANA_URL", "")

        self.monitoring_redis_host = os.getenv("LOOM_MONITORING_REDIS_CONTAINER_NAME", "localhost")
        self.monitoring_redis_port = int(os.getenv("LOOM_MONITORING_REDIS_PORT", "6379"))
        self.monitoring_redis_db = int(os.getenv("LOOM_MONITORING_DEDUPLICATE_ERROR_ALERT_REDIS_DB", "0"))
        self.monitoring_redis_password = os.getenv("LOOM_MONITORING_REDIS_PASSWORD", "")

        # Настройки OpenTelemetry
        self.otlp_host = os.getenv("LOOM_OTEL_COLLECTOR_CONTAINER_NAME", "loom-otel-collector")
        self.otlp_port = int(os.getenv("LOOM_OTEL_COLLECTOR_GRPC_PORT", "4317"))

        # External services configuration
        self.loom_authorization_host = os.getenv("LOOM_AUTHORIZATION_CONTAINER_NAME", "localhost")
        self.loom_authorization_port = int(os.getenv("LOOM_AUTHORIZATION_PORT", "8081"))