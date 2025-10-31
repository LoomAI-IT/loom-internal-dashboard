from fastapi import FastAPI

from internal import interface


def NewHTTP(
        dashboard_controller: interface.IDashboardController,
        http_middleware: interface.IHttpMiddleware,
        prefix: str
):
    app = FastAPI(
        openapi_url=prefix + "/openapi.json",
        docs_url=prefix + "/docs",
        redoc_url=prefix + "/redoc",
    )
    include_middleware(app, http_middleware)
    include_dashboard_handlers(app, dashboard_controller, prefix)

    return app


def include_middleware(
        app: FastAPI,
        http_middleware: interface.IHttpMiddleware,
):
    http_middleware.authorization_middleware03(app)
    http_middleware.logger_middleware02(app)
    http_middleware.trace_middleware01(app)


def include_dashboard_handlers(
        app: FastAPI,
        dashboard_controller: interface.IDashboardController,
        prefix: str
):
    app.add_api_route(
        prefix + "/user-movement-map/{account_id}/{hours}",
        dashboard_controller.get_user_movement_map,
        methods=["GET"],
        tags=["Dashboard"],
    )


def heath_check_handler():
    async def heath_check():
        return "ok"

    return heath_check