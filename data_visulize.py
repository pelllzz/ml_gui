import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.preprocessing import LabelEncoder

class data_:
    def read_file(self, filepath):
        return pd.read_csv(str(filepath))

    def get_column_list(self, df):
        column_list = []
        for i in df.columns:
            column_list.append(i)

        return column_list