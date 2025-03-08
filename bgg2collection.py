try:
    import pandas as pd
except ImportError as e:
    print("Error: Pandas library is not installed.")
    raise e

PARAM = "avgweight"
DIMENSION_COLUMN = "comment"
LENGTH_NAME = "Length: "
HEIGHT_NAME = "Heigth: "
CATEGORY_NAME = "Category: "
BY_WEIGHT = False

path = "collection.csv"

try:
    df = pd.read_csv(path)
except FileNotFoundError as e:
    print(f"Error: The file {path} does not exist.")
    raise e

columns = ["objectname", "own", DIMENSION_COLUMN]
if not BY_WEIGHT:
    columns.append(PARAM)
df = df[columns]
df = df[df["own"] == 1].drop(columns="own")
df = df[df[DIMENSION_COLUMN].str.contains("Length:|Heigth:|Category:").fillna(False)]
comment = df[DIMENSION_COLUMN].str.split("\n", expand=True)

df["category"] = comment.apply(lambda x: next((s.replace(CATEGORY_NAME, "") for s in x if s and CATEGORY_NAME in s), None), axis=1)
df["height"] = comment.apply(lambda x: next((s.replace(HEIGHT_NAME, "").replace(",", ".") for s in x if s and HEIGHT_NAME in s), None), axis=1).astype(float)
df["length"] = comment.apply(lambda x: next((s.replace(LENGTH_NAME, "").replace(",", ".") for s in x if s and LENGTH_NAME in s), None), axis=1).astype(float)

df.drop(inplace=True, columns=DIMENSION_COLUMN)
df["length"].dropna(inplace=True)
df.to_csv("mod_" + path, index=False, sep=";")
