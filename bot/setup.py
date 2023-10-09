import os
import sys
import logging
import importlib
from glob import glob
from pathlib import Path
from termcolor import colored


async def setup_db():
    _metadata = db.MetaData()

    Student = db.Table(
        "Student",
        _metadata,
        db.Column("Id", db.Integer(), primary_key=True),
        db.Column("Name", db.String(255), nullable=False),
        db.Column("Major", db.String(255), default="Math"),
        db.Column("Pass", db.Boolean(), default=True),
    )

    metadata.create_all(engine)


async def setup_plugins():
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
