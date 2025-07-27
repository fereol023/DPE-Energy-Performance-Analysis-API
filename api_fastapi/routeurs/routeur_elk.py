from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from api_utils.commons import get_env_variable

router = APIRouter()
_elk_tag = ["ELK logger module"]

@router.get("/logger", tags=_elk_tag)
async def redirect_logger_kibana():
    """redirects to kibana page"""
    KIBANA_HOST = get_env_variable('KIBANA_HOST', compulsory=True)
    KIBANA_PORT = get_env_variable('KIBANA_PORT', compulsory=True, cast_to_type=int)

    url = f"http://{KIBANA_HOST}:{KIBANA_PORT}"
    return RedirectResponse(f"{url}")