
import torch
import os
from typing import Union
import traceback
from core.device.device_interactor import Adb
from core.model.model_manager import ModelManager
from log.log_handler import logger


SERIAL = "emulator-5554"


def start(serial: str = SERIAL, model_path: Union[str, os.PathLike[str]] = "Hcompany/Holo1-7B"):
  adb = Adb(serial=serial)
  MM = ModelManager(pretrained_model_name_or_path=model_path)
  model = MM.model
  if not model:
    logger.error("could not load the model")
    exit(-1)
  
  


if __name__ == "__main__":
  start(serial="emulator-5554")
