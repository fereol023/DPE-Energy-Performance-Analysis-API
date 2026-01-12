import os
import sys
import click
import yappi
import uvicorn
import pathlib
import logging

# ajouter le module engine pour qu'il soit importé par le routeur qui execute le flow
CURRENT_DIRPATH = pathlib.Path(__file__).parent
ENGINE_DIRPATH = CURRENT_DIRPATH.parent
logging.warning(f"- Listening to engine to path : {ENGINE_DIRPATH}")
sys.path.append(ENGINE_DIRPATH)


def _configurate_server(local, no_prefect):
    """
    Entrypoint for backend server api starting
    local: python main.py --local 
    nolocal (image): python main.py 
    """
    # le profiler de fonctions 
    yappi.start(builtins=False, profile_threads=True)
    if local:
        print("=== Running in local mode ===".center(os.get_terminal_size().columns))
        from api_utils.fonctions import set_config_as_env_var as set_config
        set_config(dirpath=os.path.join(ENGINE_DIRPATH, "api", "config"), filename="secrets.json", debug=True)
        set_config(dirpath=os.path.join(ENGINE_DIRPATH, "config"), filename="paths.yml", debug=True, bypass_env=True)
    else:
        print("=== Running in no local mode ===")

    if no_prefect:
        os.environ['DPE_API_PREFECT_WORKER'] = '0'


def _init_api_logger(API_NAME: str):
    """initialize api logger with stream handler to reuse later with getLogger as it is a singleton"""
    logger = logging.getLogger(API_NAME)
    logger.setLevel(logging.INFO)
    #formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
    ##console_handler = logging.StreamHandler()
    #console_handler.setFormatter(formatter)
    #logger.addHandler(console_handler)
    logger.info(f"✅ Logger for {API_NAME} initialized")
    logger.propagate = False
    return logger


@click.command()
@click.option("--local", is_flag=True, help="run server locally and in deployment mode else")
@click.option("--no-prefect", is_flag=True, help="disable prefect worker launch beside api server")
def start_server(local, no_prefect):

    _configurate_server(local, no_prefect)
    _init_api_logger(API_NAME=os.getenv("API_NAME", default="DPE-ENEDIS-ADEME-API-SERVER"))

    from api_utils.commons import get_env_variable
    uvicorn.run(
        "api_fastapi.main:app",
        host=get_env_variable("API_HOST", default_value="0.0.0.0", compulsory=True),
        port=int(get_env_variable("API_PORT")),
        reload=True
    )


if __name__=="__main__":
    start_server()
