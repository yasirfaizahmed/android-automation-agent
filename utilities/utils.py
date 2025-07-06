from PIL import Image
from pathlib import Path as p

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

# def load_image()


if __name__ == "__main__":
  pre_process_image(path="/home/xd/Documents/ML_AI/android-automation-tester/images/Screenshot from 2025-07-04 20-57-21.png")