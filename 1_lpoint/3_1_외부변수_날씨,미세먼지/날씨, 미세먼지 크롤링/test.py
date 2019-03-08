import pandas as pd
a = pd.read_csv('ctg3_2.csv')

print(a.head())

for i in range(5):
    print(str(a['id'].iloc[i]))