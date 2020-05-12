import pandas as pd


class Tools:
    @staticmethod
    def read_csv(file, delim=';'):
        data = pd.read_csv(file, delimiter=delim)
        return data
