
import torch
import os
from typing import Union
import traceback
from device_interactor import Adb
from model_manager import ModelManager

SERIAL = "emulator-5554"


def start(serial: str = SERIAL, model_path: Union[str, os.PathLike[str]] = "Hcompany/Holo1-7B"):
  Adb = Adb(serial=serial)
  MM = ModelManager(pretrained_model_name_or_path=model_path)
  model = MM.model
  if not model:
    print("could not load the model")
    exit(-1)
  
  


if __name__ == "__main__":
  start(serial="emulator-5554")
