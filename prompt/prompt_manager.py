import prompt.prompt_templates as prompt_templates
from PIL import Image
from typing import Any, Union
import os
from copy import deepcopy
import json

from core.model.model_manager import ModelManager


class PromptManager:
  def __init__(self):
    self.__state_sequence = ["get_image_info", "predict_action"]
    self.__state_index = 0
    self.__screen_index = 0

    self.app_states = {}
  

  @property
  def state_index(self) -> int:
    return self.__state_index
  @state_index.setter
  def state_index(self, value: int):
    self.__state_index = value
  @property
  def state_sequence(self) -> list:
    return self.__state_sequence

  @property
  def screen_index(self) -> int:
    return self.__screen_index
  @screen_index.setter
  def screen_index(self, value: int):
    self.__screen_index = value

  def get_state(self):
    return self.state_sequence[self.state_index]

  def update_state(self):
    if self.state_index >= len(self.state_sequence):
      self.state_index = 0
    else:
      self.state_index += 1

  def build_prompt(self,
                   image: Union[Image.Image, os.PathLike[str]]):
    guidelines = prompt_templates.GUILINES_AND_INSTRUCTION_TEMPLATES[self.get_state()]["guidelines"]
    instructions = prompt_templates.GUILINES_AND_INSTRUCTION_TEMPLATES[self.get_state()]["instructions"]
    if isinstance(image, Image.Image) is False:
      image = Image.open(image)

    if self.get_state() == "predict_action":
      guidelines += json.dumps(self.app_states)

    return [
      {
        "role": "user",
        "content": [
          {
            "type": "image",      # image
            "image": image
          },
          {
            "type": "text",       # text prompt
            "text": f"{guidelines}\n{instructions}"
          }
        ]
      }
    ]
  
  def add_app_state(self, state: dict):
    new_state = deepcopy(prompt_templates.APP_STATE)
    new_state.update({
      "screen_index": self.screen_index,
      "buttons": state["buttons"],
      "screen_description": state["screen_description"]
    })
    self.app_states.update({
      f"screen_{self.screen_index}": new_state
    })
