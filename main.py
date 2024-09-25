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

    import sio
    import socketio

    sio_app = socketio.ASGIApp(socketio_server=sio.server, other_asgi_app=app_)
    app.add_route("/socket.io/", route=sio_app, methods=["GET", "POST"])
    app.add_websocket_route("/socket.io/", sio_app)

    # @app.get("/hello")
    # async def root():
    #     await sio.server.emit("response", "hello everyone")
    #     return {"message": "hello"}

    yield


app = fastapi.FastAPI(lifespan=lifespan)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
