import pandas as pd
from sklearn.preprocessing import StandardScaler


def clean(filename):
    rawData = pd.ExcelFile(filename)

    try:
        df = (rawData.parse("Data behind Table 2.1 WHR 2017", header=0))

        numeric_data = df.iloc[:, 2:]
        string_data = df.iloc[:, 0:1]

        fillNA = numeric_data.apply(lambda x: x.fillna(x.mean()), axis=0)
        standard = StandardScaler().fit(fillNA).transform(fillNA)
        standard = pd.DataFrame(standard, columns=numeric_data.columns)

        afterClean = pd.concat([string_data, standard], axis=1)

        # afterClean.groupby(by=afterClean['country'], axis=0).mean();
        return True, afterClean.groupby(by=afterClean['country'], axis=0, as_index=False).mean()

    except Exception:
        return False, False
