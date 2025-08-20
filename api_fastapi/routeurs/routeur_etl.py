import os, asyncio, subprocess
from fastapi import APIRouter, HTTPException

# import engine_test
from etl_engine.src.dpe_enedis_ademe_etl_engine.pipelines import DataEnedisAdemeETL

router = APIRouter(tags=["ETL module"])

@router.get("/etl/v1/run")
async def execute_ETL(annee: int = 2023, code_departement: int = 95, batch_size_enedis: int = 10, nruns: int = 1):
    """
    Execute the ETL process for Enedis and Ademe data for small batches.
    param annee: The year for which the ETL starts from (enedis source) (default is 2023).
    param code_departement: The department code for which the ETL is run (default is 95).
    param batch_size_enedis: The batch size for Enedis data processing (default is 10).
    param nruns: The number of runs for the ETL process (default is 1).
    return: A message indicating the success of the ETL process.
    raises HTTPException: If the ETL process fails or does not complete successfully.
    """
    try:
        # flow_state = engine_test.etl_flow() # etl_flow must be async if so
        flow_state = DataEnedisAdemeETL(
            annee=annee, # avoid 2024 for now, as their format is not valid Enedis API (code departement is not filled and is used as a filter here)
            code_departement=code_departement, 
            batch_size=batch_size_enedis, # nb of enedis adresses per page (limit)
            return_state=True 
            # nruns=nruns # not used in this case, represents the number of pages to process (offset)
            # offset + limit < 10_000 (restrinction enedis API)
            # otherwise use input batch file 
        )
        if not flow_state.is_completed():
            raise HTTPException(status_code=500, detail="Flow did not complete successfully.")
        return {"message": "Flow executed successfully - next check database !"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while running flow : {e}")
    

@router.get("/etl/start-deployment")
async def start_etl():
    try:
        _path = os.path.join("etl_engine", "src", "dpe_enedis_ademe_etl_engine", "pipelines", "etl_app.py")
        subprocess.Popen(
            ["python", _path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return {"status": "ok"}
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error : {e.stderr}")