import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.router import router


def create_app():
    app = FastAPI(
        title="Bitpapa API",
        description="Provides RestAPI for Bitpapa bot",
        version="0.0.1",
        docs_url="/api/v1/docs/",
        redoc_url="/api/v1/redoc/",
        openapi_url="/api/v1/openapi.json",
        swagger_ui_parameters={
            "displayRequestDuration": True
        }
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(router)
    return app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8002)
