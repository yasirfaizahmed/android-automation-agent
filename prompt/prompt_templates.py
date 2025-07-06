import json
from typing import Any, Literal, Union
import os
from pydantic import BaseModel
from PIL import Image


GET_IMAGE_INFO_INSTRUCTION_JSON_STRING = json.dumps({
    "buttons": ["Login", "Signup", "Help"],
    "screen_description": "app login screen"
})

PREDICT_ACTION_INSTRUCTION_JSON_STRING = json.dumps({
    "label": "Start",
    "coordinates": [100, 200]
})

GUILINES_AND_INSTRUCTION_TEMPLATES = {
    "get_image_info": {
        "guidelines": """
You are an expert Android app interface analyzer.

Your task is to extract all visually interactive elements (buttons, toggles, tabs, etc.) from a given app screenshot.

Be thorough but precise — avoid listing decorative items.

Always assume the user is on a touchscreen smartphone in portrait mode.
        """,
        "instructions": f"""
Given the screenshot, extract all visually identifiable interactive elements.

Strictly find all elements on the GUI image and return a list of elements or buttons in this JSON format:

{GET_IMAGE_INFO_INSTRUCTION_JSON_STRING}
        """
    },

    "predict_action": {
        "guidelines": """
You are an expert Android tester.

Your goal is to select a button that allows the user to proceed forward in the app **without requiring login or account creation**.

❌ Strictly avoid buttons with labels that suggest:
- Login or sign in (e.g., "Login", "Log in", "Sign in", "I already have an account", "Continue with Google", "Continue with Email")
- Account creation or registration (e.g., "Sign up", "Create account")

✅ Prefer buttons that:
- Begin the experience (e.g., "Start", "Get Started", "Continue as Guest", "Skip")
- Take the user to the main app/dashboard or gameplay

Never select a button that requires authentication, registration, or linking accounts.

Assume the user wants to skip all login-related flows and jump straight into the app.
        """,
        "instructions": f"""
From the given list of buttons, choose the most appropriate one that lets the app proceed to the next usable screen.

Strictly return your decision in this JSON format:

{PREDICT_ACTION_INSTRUCTION_JSON_STRING}
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
