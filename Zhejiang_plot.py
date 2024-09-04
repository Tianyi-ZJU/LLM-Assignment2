import requests
import json
import re

# 定义要发送给KoboldCpp的Prompt
prompt = """
You are an AI assistant that generates **Python code only**. I have a CSV file named "people_output_updated.csv" containing the population data for various regions in China over the last 10 years. The structure of the CSV file is as follows:

Column Headers: "地区,2023年,2022年,2021年,2020年,2019年,2018年,2017年,2016年,2015年,2014年,平均人口,最大人口,最小人口"  
Sample Data:  
北京市,2186,2184,2189,2189,2190,2192,2194,2195,2188,2171,2187.8,2195,2171
天津市,1364,1363,1373,1387,1385,1383,1410,1443,1439,1429,1397.6,1443,1363

Each row after the header contains the population data for a specific region over the last 10 years, from 2023 to 2014.

**Generate Python code only** to perform the following tasks without any explanation or additional text:

1. Use pandas to read the CSV file named "people_output_updated.csv".

2. Filter the data to include only the row corresponding to Zhejiang Province.

3. Use `matplotlib` to create a line chart that visualizes the population change trend of Zhejiang Province over the last 10 years (from 2014 to 2023).

4. Display the Line Chart:
   - Set appropriate labels for the X-axis (years) and Y-axis (population).
   - Add a title for the chart: "Population Trend of Zhejiang Province (2014-2023)".
   - Extract the population data for Zhejiang Province in ascending order of years (from 2014 to 2023) to ensure the bar chart displays data from left (2014) to right (2023) correctly.
   - - Use `font = FontProperties(fname='C:\Windows\Fonts\simsunb.ttf')\n plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']\n plt.rcParams['axes.unicode_minus'] = False ` to set the font for Chinese characters in the plot to ensure labels and titles are displayed correctly.

Generate Python code only, without any explanations, comments, or unnecessary text.
"""

# 设置API请求的负载
payload = {
    "prompt": prompt,
    #"max_new_tokens": 300,  # Allow sufficient tokens for complete code output
    "temperature": 0,  # Lower temperature for more deterministic output
    "max_length": 1024,
    "rep_pen": 1.1,
}

# 设置KoboldCpp API的URL
api_url = "http://localhost:5001/api/v1/generate"

# 发送请求到KoboldCpp API
response = requests.post(api_url, json=payload)

# 检查请求的响应
if response.status_code == 200:
    # Extract the generated Python code from the response
    raw_output = response.json()
    line_code = raw_output.get("results", [{}])[0].get("text", "").strip()

    # Print the original output for reference
    print("Model Output:\n")
    print(line_code)

    # Step 5: Clean the generated code to remove unnecessary text
    code_block = re.search(r'```python(.*?)```', line_code, re.DOTALL)

    if code_block:
        extracted_code = code_block.group(1).strip()  # Extract and clean the code
        #print("Extracted Python code:\n")
        #print(extracted_code)
        
        # Step 5: Save the extracted code to a file
        with open("line_plot.py", "w", encoding="utf-8") as file:
            file.write(extracted_code)
        
        # Step 6: Execute the extracted Python code
        exec(extracted_code)

    print("\nThe generated Python code has been saved to 'line_plot.py'. You can run it to create the line chart.")
else:
    print(f"Error: Unable to generate code. Status code {response.status_code}, Response: {response.text}")
