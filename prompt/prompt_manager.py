import prompt.prompt_templates as prompt_templates
from PIL import Image
from typing import Any

from core.model.model_manager import ModelManager


class PromptManager:
  def __init__(self):
    self.__state_sequence = ["get_image_info", "update_state", "predict_action"]
    self.__state_index = 0

    self.build_prompt = prompt_templates.build_prompt

  @property
  def state_index(self) -> int:
    return self.__state_index

  @state_index.setter
  def state_index(self, value: int):
    self.__state_index = value

  @property
  def state_sequence(self) -> list:
    return self.__state_sequence

  def get_state(self):
    return self.state_sequence[self.state_index]

  def update_state(self):
    if self.state_index >= len(self.state_sequence):
      self.state_index = 0
    else:
      self.state_index += 1

  