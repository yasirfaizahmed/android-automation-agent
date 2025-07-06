import prompt.localization as localization
from PIL import Image
from typing import Any

from core.model.model_manager import ModelManager

class PromptManager:
  def __init__(self):
    pass

  def form_prompt(self, image: Image.Image, instruction) -> dict:
    prompt = localization.get_localization_prompt()

  # Helper function to run inference
  def run_inference(self,
                    model_manager: ModelManager,
                    image: Image.Image,
                    messages: list[dict[str, Any]]) -> str:
      model = model_manager.model
      processor = model_manager.processor

      # Preparation for inference
      text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
      inputs = processor(
          text=[text],
          images=image,
          padding=True,
          return_tensors="pt",
      )
      inputs = inputs.to("cuda")

      generated_ids = model.generate(**inputs, max_new_tokens=128)
      generated_ids_trimmed = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
      return processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)