import pandas as pd
from sklearn.cluster import KMeans

def cluster(df, nClust, nRuns):

    try:
        # running the KMeans model, using sklearn function
        model = KMeans(n_clusters=int(nClust), n_init=int(nRuns)).fit(
            df.iloc[:, 1:])
        # add the labeled data to the dataframe
        df['Clustering'] = model.labels_

        return True, df
    except Exception:
        return False, False