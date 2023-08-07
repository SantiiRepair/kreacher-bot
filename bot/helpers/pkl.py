import os
import pickle


def load_pkl(path, mode, type):
    try:
        with open(path, mode) as file:
            pkl = pickle.load(file)
        return pkl
    except EOFError:
        if type is "list":
            return []
        if type is "dict":
            return {}


def dump_pkl(path, mode, data):
    try:
        with open(path, mode) as file:
            pickle.dump(data, file)
        file.close()
    except Exception as e:
        print(e)
