# LLM-Assignment2

数据处理：设计合适的 prompt，指示 LLM 生成输出，读取文本文件，去除表头表尾，另存为一个新CSV 文件：generate_csv.py

数据分析：读取预处理后的 CSV 文件，设计合适的 prompt，指示 LLM 生成 Python 代码，对单个 CSV 文件进行增删改查以及数据可视化。

1. 计算近 10 年各地区的人口均值、最大值和最小值，按列添加到表的最后：data_processing.py
2. 以饼状图的形式，可视化近 10 年各地区的平均人口比例：Average_plot.py
3. 以折线图的形式，可视化近 10 年浙江省的人口变化趋势: TODO

使用方法：

1. koboldcpp启动本地模型，具体哪个模型参见python文件第一行; 
2. 将输入文件和代码文件放在同一目录，直接运行代码即可。
