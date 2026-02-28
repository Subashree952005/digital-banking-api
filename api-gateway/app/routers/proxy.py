import httpx
from fastapi import APIRouter, Request, Response

router = APIRouter(tags=["API Gateway"])

BANKING_SERVICE_URL = "http://api:8000"


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def proxy(path: str, request: Request):
    url = f"{BANKING_SERVICE_URL}/{path}"
    params = dict(request.query_params)
    headers = dict(request.headers)
    headers.pop("host", None)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            params=params,
            content=body,
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type"),
    )