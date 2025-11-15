import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pyfk import get_logger, create_table
from routers import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app = FastAPI(
    title="Aura System",
    version="1.0.0",
    description="Aura System",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_router.router)
app.include_router(line_bot_router.router)

@app.exception_handler(Exception)
def app_exception_handler(request: Request, error: Exception):
    import traceback

    log = get_logger()
    error_message = (
        f"Failed to execute: {request.method}: {request.url}, detail: {repr(error)}"
    )
    tb = "".join(traceback.TracebackException.from_exception(error).format())
    log.error("%s\n%s" % (error_message, tb))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": error_message},
        headers={
            "content-type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Expose-Headers": "*",
        },
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
