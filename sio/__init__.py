import socketio

# mgr = socketio.AsyncRedisManager(url="redis://localhost:6379/0")
server = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="*", logger=True
)

__all__ = ["server"]
