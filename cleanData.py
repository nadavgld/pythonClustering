import pandas as pd
from sklearn.preprocessing import StandardScaler


def clean(filename):
    #read the given file to dataframe
    df = pd.read_excel(filename)

    try:
        #split file by string and numeric values. The file structur is known
        numeric_data = df.iloc[:, 2:]
        string_data = df.iloc[:, 0:1]

        #fill all missing numbers by the mean of the col
        fillNA = numeric_data.apply(lambda x: x.fillna(x.mean()), axis=0)

        #standart normelize by col, using sklearn function
        standard = StandardScaler().fit_transform(fillNA)
        standard = pd.DataFrame(standard, columns=numeric_data.columns)

        #concat the original string values and the normelized numeric values
        afterClean = pd.concat([string_data, standard], axis=1)

        #return the data after group by country and mean of each col
        return True, afterClean.groupby(by=afterClean['country'], axis=0, as_index=False).mean()

    except Exception:
        return False, False
