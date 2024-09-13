import pandas as pd

df = pd.read_csv("C:\\Users\\User\\Desktop\\Get_n_mark_data\\task4\\extracted_data.csv")
mask = df['Age'] > 42
print(df[mask])