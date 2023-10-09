import os
import sys
import logging
import importlib
from glob import glob
from pathlib import Path
from termcolor import colored

from bot import db_metadata, engine


def setup_db():
    db_metadata.create_all(engine)


def setup_plugins():
    cwd = os.path.dirname(os.path.abspath(__file__))
    folders = ["callbacks", "tasks"]
    folders.extend(glob(f"{cwd}/plugins/*", recursive=True))
    for e in glob(f"{cwd}/plugins/*", recursive=True):
        folders.append(e.split("/", 3)[3])
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
                f'{colored("[INFO]", "blue")}: Bot has started {colored(module_name.replace("/", "."), "yellow")}'
            )
