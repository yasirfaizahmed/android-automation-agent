
import torch
import os
from typing import Union
import traceback

from core.device.device_interactor import Adb
from core.model.model_manager import ModelManager
from log.log_handler import logger
from prompt.promt_manager import PromptManager
from utilities import utils


SERIAL = "emulator-5554"
PACKAGE_NAME = "com.duolingo"


def start(serial: str = SERIAL, model_path: Union[str, os.PathLike[str]] = "Hcompany/Holo1-7B"):
  adb = Adb(serial=serial)
  
  MM = ModelManager(pretrained_model_name_or_path=model_path)
  model = MM.model
  if not model:
    logger.error("could not load the model")
    exit(-1)
  
  adb.launch_app(package_name=PACKAGE_NAME)
  screenshot_path = utils.get_new_image_path()
  adb.screencap(local_path=screenshot_path)

  

if __name__ == "__main__":
  start(serial="emulator-5554")
