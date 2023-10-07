import pickle
import logging


async def load_pkl(path, mode, typeof):
    try:
        with open(path, mode) as file:
            pkl = pickle.load(file)
        return pkl
    except EOFError:
        if typeof == "list":
            return []
        if typeof == "dict":
            return {}


async def dump_pkl(path, mode, data):
    try:
        with open(path, mode) as file:
            pickle.dump(data, file)
        file.close()
    except Exception as e:
        logging.error(e)
