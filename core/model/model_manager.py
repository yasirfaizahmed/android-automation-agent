import traceback
from transformers import AutoModelForImageTextToText, AutoProcessor
import torch
import os
from typing import Union, Any
from PIL import Image


class ModelManager:
  def __init__(self, pretrained_model_name_or_path: Union[str, os.PathLike[str]]):
    self.pretrained_model_name_or_path = pretrained_model_name_or_path
    self.model = self.load_model()
    self.processor = AutoProcessor.from_pretrained(pretrained_model_name_or_path)

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
  
  # Helper function to run inference
  def run_inference(self,
                    image: Union[Image.Image, os.PathLike[str]],
                    messages: list[dict[str, Any]]) -> str:

    if isinstance(image, Image.Image) is False:
      image = Image.open(image)

    # Preparation for inference
    text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = self.processor(
      text=[text],
      images=image,
      padding=True,
      return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    generated_ids = self.model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
    return self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)