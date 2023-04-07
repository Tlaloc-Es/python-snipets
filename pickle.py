import pickle


def save_pickle(**kwargs):
    for key, value in kwargs.items():
        with open(key, 'wb') as handle:
            pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_pickle(*args):
    values = []
    for key in args:
        with open(key, 'rb') as handle:
            values.append(pickle.load(handle))
    return values
