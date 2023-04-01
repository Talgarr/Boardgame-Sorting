import pandas as pd

PARAM = "avgweight"
LENGTH_COLUMN = "comment"
LENGTH_NAME = "Length: "

df = pd.read_csv("collection.csv")
columns = ["objectname", "own", PARAM, LENGTH_COLUMN]
df = df[columns]
df = df[df["own"] == 1].drop(columns="own")
df = df[df[LENGTH_COLUMN].str.contains("Length:").fillna(False)]
df["length"] = df[LENGTH_COLUMN].str.replace("Length: ", "").astype(int)
df.drop(inplace=True, columns=LENGTH_COLUMN)
df.to_csv("collection_mod.csv", index=False, sep=";")
