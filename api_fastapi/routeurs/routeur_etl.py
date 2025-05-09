import os, asyncio
from fastapi import APIRouter, HTTPException

import engine_test
from etl_engine.src.pipelines.etl_app import etl_flow

router = APIRouter()
_etl_tag = ["ETL module"]

@router.get("/etl/v1/run", tags=_etl_tag)
async def execute_ETL():
    try:
        # await engine_test.etl_flow() # etl_flow must be async if so
        flow_state = etl_flow(return_state=True)
        if not flow_state.is_completed():
            raise HTTPException(status_code=500, detail="Flow did not complete successfully.")
        return {"message": "Flow executed successfully - next check database !"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while running flow : {e}")