import os
import re
import json
import time
import yaml
import pickle
import logging

import numpy as np
import pandas as pd
from functools import lru_cache
from unidecode import unidecode
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def load_yaml(fpath, default_value=None):
    if not os.path.exists(fpath):
        logging.warning(f"File {fpath} does not exists !")
        return default_value
    return yaml.safe_load(open(fpath, 'r'))


def load_json(fpath, default_value=None):
    if not os.path.exists(fpath):
        logging.warning(f"File {fpath} does not exists !")
        return default_value
    return json.load(open(fpath, 'rb'))


def load_pickle(fpath, is_optional=False):
    if (not os.path.exists(fpath) and (not is_optional)):
        raise Exception(f"File {fpath} does not exist and is not optional !")
    with open(fpath, 'rb') as f:
        res = pickle.load(f)
    return res


def save_pickle(obj, fpath):
    """obj : serialisable obj"""
    if not os.path.exists(os.path.dirname(fpath)):
        os.makedirs(os.path.dirname(fpath))
    with open(fpath, 'wb') as f:
        pickle.dump(obj, f)
    print(f"Sauvegarde ok at : {fpath}")


@lru_cache(maxsize=1024)
def normalize_name(colname):
    pat1, pat2 = re.compile('[^0-9a-zA-Z]+'), re.compile('_+')
    return pat1.sub('_', pat2.sub('_', colname))


def normalize_colnames_list(list_colnames=[]):
    if list_colnames:
        return list(map(lambda c: normalize_name(unidecode(c)).lower(), list_colnames))
    return []

def sort_colnames(df):
    return df[sorted(df.columns)]

def normalize_df_colnames(df):
    return sort_colnames(df.rename(columns={c: normalize_name(unidecode(c)).lower() for c in df.columns}))


def get_today_date():
    return datetime.today().strftime('%Y_%m_%d')


def get_yesterday_date():
    return (datetime.today() - pd.Timedelta(days=1)).strftime('%Y_%m_%d')


def load_parquet_dataframe(_PATH):
    """TODO"""
    print(f"Loading parquet data from : {_PATH}..")
    try:
        return normalize_df_colnames(pd.read_parquet(_PATH))
    except Exception as e:
        print(f"Error while loading : {e}")


def load_json_config(path):
    return load_json(path, default_value={})


def load_yaml_config(fpath):
    return load_yaml(fpath, default_value={})


def set_config_as_env_var(dirpath='config/', filename=None, debug=False, bypass_env=False):
    """if value is dict use eval(dict) to return to it to dicrt instead of str"""
    if (os.getenv('ENV') == None) or (bypass_env): # si vrai les variables d'env sont probablement definies déja (mode nolocal)
        try:
            if debug: 
                logging.warning(f"Loading envs var from folder : {dirpath}")
            config = {}
            if filename is None:
                for filename in os.listdir(dirpath):
                    if filename.endswith('.yml'):
                        config.update(load_yaml_config(os.path.join(dirpath, filename)))
                    if filename.endswith('.json'):
                        config.update(load_json_config(os.path.join(dirpath, filename)))
            else:
                if filename.endswith('.yml'):
                    config.update(load_yaml_config(os.path.join(dirpath, filename)))
                if filename.endswith('.json'):
                    config.update(load_json_config(os.path.join(dirpath, filename)))
            appname, env = config.get('API-NAME'), config.get('ENV')
            if not bypass_env: 
                assert env in ['LOCAL', 'NOLOCAL'], f"Config error : ENV ({env}) is not valid. Choose between ['LOCAL', 'NOLOCAL']"
            logging.info(f"Application {appname} is running on env {env}")
            for key, value in config.items():
                if debug:
                    print(f"Setting config : {key} = {value}", end="\r", flush=True) # flush desactive le buffering du terminal et force affichage immediat
                    time.sleep(.1)
                os.environ[key] = str(value)
        except Exception as e:
            print(f"Excetion while setting config : {e}")
    else:
        print(f"Config already set from ENV var : {os.getenv('ENV')} - processing {dirpath}/{filename} bypassed.")
