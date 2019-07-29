import context
from rltrader import data as rldata
import os


def test_read_csv_data_frame():
    data = rldata.CsvFileDataFrameData(os.path.dirname(
        os.path.realpath(__file__))+"/data/test.csv")

    assert len(data.frame) == 2
