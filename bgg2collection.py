import pandas as pd

PARAM = "avgweight"
DIMENSION_COLUMN = "comment"
LENGTH_NAME = "Length: "
HEIGHT_NAME = "Heigth: "
BY_WEIGHT = False

path = "collection.csv"

df = pd.read_csv(path)
columns = ["objectname", "own", DIMENSION_COLUMN]
if not BY_WEIGHT:
    columns.append(PARAM)
df = df[columns]
df = df[df["own"] == 1].drop(columns="own")
df = df[df[DIMENSION_COLUMN].str.contains("Length:").fillna(False)]
comment = df[DIMENSION_COLUMN].str.split("\n", expand=True)

if BY_WEIGHT:
    df["height"] = comment[1].str.replace(HEIGHT_NAME, "").str.replace(",", ".").astype(float)
df["length"] = comment[0].str.replace(LENGTH_NAME, "").str.replace(",", ".").astype(float)
df.drop(inplace=True, columns=DIMENSION_COLUMN)
df.to_csv("mod_" + path, index=False, sep=";")
