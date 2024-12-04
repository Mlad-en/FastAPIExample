import sys

from fastapi import Request
from loguru import logger
from starlette.concurrency import iterate_in_threadpool


def serialize(record):
    subset = {
        "timestamp": record["time"].isoformat(),
        "message": record["message"],
        "status": record["extra"]["response_code"],
        "response_body": record["extra"]["response_body"],
        "request_url": record["extra"]["request_url"],
        "request_headers": record["extra"]["request_headers"],
        "request_params": record["extra"]["request_params"],
    }
    return subset


def patching(record):
    record["extra"]["serialized"] = serialize(record)


logger = logger.patch(patching)
logger.add(sys.stderr, format="{extra[serialized]}")


async def log_error_response(request: Request, call_next):
    response = await call_next(request)

    if response.status_code >= 400:
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        logger.bind(
            response_code=response.status_code,
            response_body=response_body[0].decode(),
            request_url=str(request.url),
            request_params=dict(request.query_params),
            request_headers=dict(request.headers),
        ).error("Request failed")

    return response
