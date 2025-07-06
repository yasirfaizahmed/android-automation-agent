from PIL import Image
from pathlib import Path as p
import time
from datetime import date

from utilities.paths import IMAGES

LANDSCAPE_RESOLUTION = (1280, 720)
PORTRAIT_RESOLUTION = (720, 1280)


def pre_process_image(path: p) -> Image.Image:
  if isinstance(path, p) is False:
    path = p(path)
  if path.exists() is False:
    raise FileNotFoundError
  
  unprocessed_image = Image.open(path)
  width, height = unprocessed_image.size
  if width > height:
    return unprocessed_image.resize(LANDSCAPE_RESOLUTION)
  else:
    return unprocessed_image.resize(PORTRAIT_RESOLUTION)

def get_current_time() -> tuple:
  current_time = time.strftime("%H-%M-%S", time.localtime())
  current_date = date.today().strftime("%B-%d-%Y")
  return current_date, current_time

def get_new_image_path() -> str:
  if IMAGES.exists() is False:
    IMAGES.mkdir()

  current_date, current_time = get_current_time()
  image_name = f"{current_date}_{current_time}.png"
  image_path = IMAGES.joinpath(image_name)
  return image_path


if __name__ == "__main__":
  pre_process_image(path="/home/xd/Documents/ML_AI/android-automation-tester/images/Screenshot from 2025-07-04 20-57-21.png")