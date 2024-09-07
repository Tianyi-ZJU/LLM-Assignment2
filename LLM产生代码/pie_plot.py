import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

def read_and_load_csv():
    df = pd.read_csv('people_output_updated.csv', encoding='utf-8')
    return df

def compute_statistics(df):
    df['平均人口'] = df.iloc[:, 1:11].mean(axis=1)
    df['最大人口'] = df.iloc[:, 1:11].max(axis=1)
    df['最小人口'] = df.iloc[:, 1:11].min(axis=1)
    return df

def create_pie_chart(df):
    font = FontProperties(fname='C:\Windows\Fonts\simsunb.ttf')
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    average_population = df['平均人口'].sum()
    region_proportions = df['平均人口'] / average_population
    labels = [f'{region} ({proportion:.2%})' for region, proportion in zip(df['地区'], region_proportions)]
    plt.pie(region_proportions, labels=labels, autopct='%1.1f%%')
    plt.title('Average Population Proportion by Region (2023-2014)')
    plt.show()

def save_and_display(df):
    df.to_csv('people_output_updated.csv', index=False)
    create_pie_chart(df)

if __name__ == '__main__':
    df = read_and_load_csv()
    df = compute_statistics(df)
    save_and_display(df)