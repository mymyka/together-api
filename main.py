import fastapi
import contextlib


@contextlib.asynccontextmanager
async def lifespan(app_: fastapi.FastAPI):
    import api

    app_.include_router(api.router)

    import deps
    import models

    models.SQLModel.metadata.drop_all(deps.sync_engine)
    models.SQLModel.metadata.create_all(deps.sync_engine)

    yield


app = fastapi.FastAPI(lifespan=lifespan)
