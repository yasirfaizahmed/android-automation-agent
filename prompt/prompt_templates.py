import json
from typing import Any, Literal, Union
import os
from pydantic import BaseModel
from PIL import Image

GET_IMAGE_INFO_INSTRUCTION_JSON_STRING = json.dumps({
          "buttons": ["Login", "Signup", "help"],
          "screen_description": "app login screen"
        })

GUILINES_AND_INSTRUCTION_TEMPLATES = {
  "get_image_info": {
    "guidelines": """
        You are an expert Android application tester.

        You are tasked with analyzing screenshots of Android apps and identifying all actionable UI elements, such as buttons, text inputs, toggles, icons, and clickable areas.

        Be accurate. Do not include decorative or non-interactive elements.
        Screen may contain in-game UI, menus, or system dialogs.

        If the screen is unclear or unreadable, return an empty list without guessing.
    """,
    "instructions": f"""
        Given the screenshot, extract all visually identifiable interactive elements.
        strictly find all element on the GUI image and return a list of elements or buttons in this JSON format:
        {GET_IMAGE_INFO_INSTRUCTION_JSON_STRING}
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
        - Tries to login or sign up

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

APP_STATE = {
  "screen_index": 0,
  "buttons": [],
  "screen_description": ""
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
