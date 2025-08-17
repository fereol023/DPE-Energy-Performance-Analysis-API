import click, uvicorn, os, sys

# ajouter le module engine pour qu'il soit 
# importé par le routeur qui exec le flow
CURRENT_DIRPATH = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIRPATH = os.path.join(CURRENT_DIRPATH, "etl_engine")
assert os.path.exists(ENGINE_DIRPATH), f"Le path de l'engine n'existe pas : {ENGINE_DIRPATH}"
sys.path.append(ENGINE_DIRPATH)

@click.command()
@click.option("--local", is_flag=True, help="run server locally and in deployment mode else")
def start_server(local):
    """
    Entrypoint for backend server api starting
    local: python main.py --local
    nolocal (image): python main.py 
    """
    if local:
        print("=== Running in local mode ===".center(os.get_terminal_size().columns))
        from api_utils.fonctions import set_config_as_env_var as set_config
        set_config(dirpath="config", filename="secrets.json", debug=True)
        set_config(dirpath="config", filename="paths.json", debug=True)
    else:
        print("=== Running in no local mode ===".center(os.get_terminal_size().columns))

    from api_utils.commons import get_env_variable
    uvicorn.run(
        "api_fastapi.main:app",
        host=get_env_variable("API_HOST"),
        port=int(get_env_variable("API_PORT")),
        reload=True
    )

if __name__=="__main__":
    start_server()
