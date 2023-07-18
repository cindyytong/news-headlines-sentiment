import pandas as pd

df = pd.read_csv("headlines.csv")

df['headline'] = df['Headline'].replace(",", "", regex=True, inplace=True)
df['headline'] = df['Headline'].replace("'", "", regex=True, inplace=True)
df['headline'] = df['Headline'].replace('"', "", regex=True, inplace=True)


df['URL'] = df['URL'].replace(",", "", regex=True, inplace=True)
