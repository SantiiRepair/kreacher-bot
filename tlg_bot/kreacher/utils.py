import sys
import logging
import importlib
from pathlib import Path
from termcolor import colored


def load_plugins(plugin_name):
    path = Path(f"kreacher/plugins/{plugin_name}.py")
    name = "kreacher.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["kreacher.plugins." + plugin_name] = load
    print(f'{colored("[INFO]", "blue")}: Bot has started {colored(plugin_name, "yellow")}')
