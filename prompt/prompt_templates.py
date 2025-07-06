import json
from typing import Any, Literal, Union
import os
from pydantic import BaseModel
from PIL import Image


GUILINES_AND_INSTRUCTION_TEMPLATES = {
  "get_image_info": {
    "guidelines": """
        You are an expert Android application tester.

        You are tasked with analyzing screenshots of Android apps and identifying all actionable UI elements, such as buttons, text inputs, toggles, icons, and clickable areas.

        Be accurate. Do not include decorative or non-interactive elements.
        Screen may contain in-game UI, menus, or system dialogs.

        If the screen is unclear or unreadable, return an empty list without guessing.
    """,
    "instructions": """
        Given the screenshot, extract all visually identifiable interactive elements.
        strictly find all element on the GUI image and return a list of elements or buttons in this JSON format:
        {
          "buttons": [
            {
              "label": "Start",
              "coordinates": [100, 200]
            },
            {
              "label": "Settings",
              "coordinates": [300, 500]
            }
          ]
        }
    """
  },

  "predict_action": {
    "guidelines": """
        You are an intelligent Android test agent.

        Your goal is to autonomously navigate Android apps and games by selecting the most appropriate UI element (button/tap area) that leads to the app progressing forward naturally — like starting gameplay, continuing a session, or moving to the next screen.

        Avoid buttons or actions that:
        - Exit the app
        - Redirect to login, ads, rating pages, or app stores
        - Open settings or social media
        - Loop back to the same screen

        Use knowledge of past app states and screen transitions to make the best decision.
    """,
    "instructions": """
        Using the current app state and past states, select the most logical UI element to tap next.

        Return your decision in this format:

        {
          "click": {
            "label": "Start",
            "coordinates": [100, 200]
          }
        }
    """
  }
}


def get_localization_prompt(image, instruction: str) -> list[dict[str, Any]]:
  guidelines: str = "Localize an element on the GUI image according to my instructions and output a click position as Click(x, y) with x num pixels from the left edge and y num pixels from the top edge. The x, y must be exactly in the center of the GUI element."

  return [
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "image": image,
        },
        {"type": "text", "text": f"{guidelines}\n{instruction}"},
      ],
    }
  ]


def build_prompt(image: Union[Image.Image, os.PathLike[str]], guidelines: str, instructions: str):
  if isinstance(image, Image.Image) is False:
    image = Image.open(image)

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


class ClickAction(BaseModel):
  """Click at specific coordinates on the screen."""

  action: Literal["click"] = "click"
  x: int
  """The x coordinate, number of pixels from the left edge."""
  y: int
  """The y coordinate, number of pixels from the top edge."""


def get_localization_prompt_structured_output(image, instruction: str) -> list[dict[str, Any]]:
  guidelines: str = "Localize an element on the GUI image according to my instructions and output a click position as Click(x, y) with x num pixels from the left edge and y num pixels from the top edge. The x, y must be exactly in the center of the GUI element."

  return [
    {
      "role": "system",
      "content": json.dumps([ClickAction.model_json_schema()]),
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "image": image,
        },
        {"type": "text", "text": f"{guidelines}\n{instruction}"},
      ],
    },
  ]
