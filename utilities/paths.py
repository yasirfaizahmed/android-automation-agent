from pathlib import Path as p


__here = p(__file__)

PROJECT_DIR = __here.parent.parent
CORE = p(PROJECT_DIR, "core")
CONFIG = p(PROJECT_DIR, "config")
UTILITIES = p(PROJECT_DIR, "utilities")
INFERENCE = p(PROJECT_DIR, "inference")
