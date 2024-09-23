import fastapi
import contextlib
import fastapi.middleware.cors as cors


@contextlib.asynccontextmanager
async def lifespan(app_: fastapi.FastAPI):
    import api


    app_.include_router(api.router)

    import deps
    import models

    models.SQLModel.metadata.create_all(deps.sync_engine)

    yield


app = fastapi.FastAPI(lifespan=lifespan)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
