import pandas as pd


class DataFrameData:

    def __init__(self, df):
        self.frame = df


class CsvFileDataFrameData:

    def __init__(self, path):
        self.frame = pd.read_csv(path)
