import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

df = pd.read_csv('people_output_updated.csv', encoding='utf-8')
zhejiang_data = df[df['地区'] == '浙江省']
years = [str(year) + '年' for year in range(2014, 2024)]
population = zhejiang_data[years].values.flatten()
font = FontProperties(fname='C:\Windows\Fonts\simsunb.ttf')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.plot(years, population)
plt.xlabel('Year')
plt.ylabel('Population')
plt.title('Population Trend of Zhejiang Province (2014-2023)')
plt.show()