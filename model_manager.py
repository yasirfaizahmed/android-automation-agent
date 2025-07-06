import traceback
from transformers import AutoModelForImageTextToText, AutoProcessor
import torch
import os
from typing import Union


class ModelManager:
  def __init__(self, pretrained_model_name_or_path: Union[str, os.PathLike[str]]):
    self.pretrained_model_name_or_path = pretrained_model_name_or_path
    self.model = self.load_model()
    self.processor = AutoProcessor.from_pretrained()

  def load_model(self) -> bool:
    model = False
    try:
      model = AutoModelForImageTextToText.from_pretrained(
        pretrained_model_name_or_path=self.pretrained_model_name_or_path,
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2",
        device_map="auto",
      )
    except Exception:
      print(traceback.format_exc())
    return model