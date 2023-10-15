import os.path
import sys
import dill
import numpy as np
import yaml

from source.exception import BackOrderException
from source.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise BackOrderException(e, sys) from e