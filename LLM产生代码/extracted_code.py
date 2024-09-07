import pandas as pd
df = pd.read_csv('people_output.csv', encoding='utf-8')
def calculate_stats(row):
    avg = sum(row[1:]) / len(row[1:])
    max_pop = max(row[1:])
    min_pop = min(row[1:])
    return pd.Series([avg, max_pop, min_pop], index=['平均人口', '最大人口', '最小人口'])
df[['平均人口', '最大人口', '最小人口']] = df.apply(calculate_stats, axis=1)
df.to_csv('people_output_updated.csv', encoding='utf-8', index=False)