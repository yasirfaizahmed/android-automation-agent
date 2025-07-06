
import torch
import os
from typing import Union
import traceback
import json
import time
from json_repair import repair_json

from core.device.device_interactor import Adb
from core.model.model_manager import ModelManager
from log.log_handler import logger
from prompt import prompt_manager, prompt_templates
from utilities import utils


SERIAL = "emulator-5554"
PACKAGE_NAME = "com.duolingo"


def start(serial: str = SERIAL, model_path: Union[str, os.PathLike[str]] = "Hcompany/Holo1-3B"):
  adb = Adb(serial=serial)
  
  MM = ModelManager(pretrained_model_name_or_path=model_path)
  model = MM.model
  if not model:
    logger.error("could not load the model")
    exit(-1)
  
  PM = prompt_manager.PromptManager()

  adb.launch_app(package_name=PACKAGE_NAME)

  while True:
    state = PM.get_state()

    screenshot_path = utils.get_new_image_path()
    adb.screencap(local_path=screenshot_path)
    
    prompt = PM.build_prompt(image=screenshot_path)
    response: str = MM.run_inference(image=screenshot_path, messages=prompt)
    fixed_json = json.loads(repair_json(response[0]))   # TODO: validate this json before adding to app states
    
    if state == "get_image_info":
      app_state = fixed_json
      PM.add_app_state(app_state)

    PM.update_state()

    time.sleep(5)
    

if __name__ == "__main__":
  start(serial="emulator-5554")
