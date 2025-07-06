import adbutils
from pathlib import Path as p
from PIL import Image
from log.log_handler import logger


class Adb(adbutils.AdbClient):
  def __init__(self, serial: str, **kwargs):
    super().__init__(**kwargs)
    self.serial = serial
    self.android_device = self.device(serial=serial)
    logger.info("initializing adb client")

  def run_cmd(self, command: str) -> str:
    output: str = self.shell(command=command, serial=self.serial)
    logger.info(f"running {command}")
    return output

  def screencap(self, local_path: p):
    screenshot: Image.Image = self.android_device.screenshot()
    logger.info(f"saving screenshot at {local_path}")
    screenshot.save(local_path)
  
  def get_main_activity(self, package_name: str) -> str:
    all_activities = self.run_cmd(command=f'dumpsys package | grep -i "{package_name}" | grep Activity')
    main_activity = all_activities.split("\n")[0].strip().split(" ")[1]
    logger.info(f"main activity for {package_name} is {main_activity}")
    return main_activity

  def launch_app(self, package_name: str) -> bool:
    main_activity = self.get_main_activity(package_name=package_name)
    self.run_cmd(command=f"am start -n {main_activity}")
    logger.info(f"launching app {package_name}")
    return True

  def click(self, x: int, y: int):
    self.run_cmd(command=f"input tap {x} {y}")
    logger.info(f"tap at {x} {y}")


if __name__ == "__main__":
  Adb("emulator-5554").get_main_activity("com.duolingo")