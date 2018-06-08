import pandas as pd
from sklearn.preprocessing import StandardScaler


def clean(filename):
    df = pd.read_excel(filename)

    try:
        numeric_data = df.iloc[:, 2:]
        string_data = df.iloc[:, 0:1]

        fillNA = numeric_data.apply(lambda x: x.fillna(x.mean()), axis=0)
        standard = StandardScaler().fit(fillNA).transform(fillNA)
        standard = pd.DataFrame(standard, columns=numeric_data.columns)

        afterClean = pd.concat([string_data, standard], axis=1)

        return True, afterClean.groupby(by=afterClean['country'], axis=0, as_index=False).mean()

    except Exception:
        return False, False
