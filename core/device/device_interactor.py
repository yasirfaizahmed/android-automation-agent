import adbutils
from pathlib import Path as p
from PIL import Image


class Adb(adbutils.AdbClient):
  def __init__(self, serial: str, **kwargs):
    super().__init__(**kwargs)
    self.serial = serial
    self.android_device = self.device(serial=serial)

  def run_cmd(self, command: str) -> str:
    command = command.split(" ")
    output: str = self.shell(command=command, serial=self.serial)
    return output

  def screencap(self, local_path: p):
    screenshot: Image.Image = self.android_device.screenshot()
    screenshot.save(local_path)


if __name__ == "__main__":
  Adb("emulator-5554").screencap("/home/xd/Documents/ML_AI/android-automation-tester/images/tet3.png")