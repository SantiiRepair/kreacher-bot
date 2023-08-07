import sys
import logging
import importlib
from pathlib import Path
from termcolor import colored


def loader(name):
    folders = ["callbacks", "plugins", "tasks"]

    for folder in folders:
        folder_path = Path(f"bot/{folder}")
        for file in folder_path.glob("*.py"):
            module_name = f"bot.{folder}.{file.stem}"

            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            module.logger = logging.getLogger(module_name)

            spec.loader.exec_module(module)

            sys.modules[module_name] = module

            print(
                f'{colored("[INFO]", "blue")}: Bot has started {colored(module_name, "yellow")}'
            )
