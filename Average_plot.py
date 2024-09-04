#model: starcoder2-15b-instruct-v0.1-Q4_K_M
import requests
import pandas as pd
import re

# Step 1: Load the data to understand its structure (not strictly necessary, but helpful)
file_path = 'people_output_updated.csv'  # Replace with your actual CSV file path
df = pd.read_csv(file_path)

# Check the content of the CSV file (you may skip this step in the final script)
#print(df.head())

# Step 2: Create a prompt for the model to generate visualization code
prompt = f"""
You are an AI assistant that generates **Python code only**. I have a CSV file named "people_output_updated.csv" containing the population data for various regions in China over the last 10 years. The structure of the CSV file is as follows:

Column Headers: "地区,2023年,2022年,2021年,2020年,2019年,2018年,2017年,2016年,2015年,2014年,平均人口,最大人口,最小人口"
Sample Data:
北京市,2186,2184,2189,2189,2190,2192,2194,2195,2188,2171,2187.8,2195.0,2171.0
天津市,1364,1363,1373,1387,1385,1383,1410,1443,1439,1429,1397.6,1443.0,1363.0
河北省,7393,7420,7448,7464,7447,7426,7409,7375,7345,7323,7405.0,7464.0,7323.0

Each row after the header contains the population data for a specific region over the last 10 years, from 2023 to 2014.

**Generate Python code only** to perform the following tasks without any explanation or additional text:

1. Read and Load the CSV File using pandas.
   - Use pandas to read the CSV file named "people_output_updated.csv".

2. Compute Statistics:
   - For each region, compute the average, maximum, and minimum population over the last 10 years (from columns 2023 to 2014).
   - Ensure that the calculations are correct by verifying the results.

3. Create a Pie Chart:
   - Generate a pie chart using matplotlib to visualize the average population proportion of each region over the last 10 years.
   - Use `font = FontProperties(fname='C:\Windows\Fonts\simsunb.ttf')\n plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']\n plt.rcParams['axes.unicode_minus'] = False ` to set the font for Chinese characters in the plot to ensure labels and titles are displayed correctly.
   - Ensure that the labels for the pie chart slices contain both the region names and their percentage of the total average population.

4. Save and Display:
   - Save the updated DataFrame with the new columns back to a new CSV file named "people_output_updated.csv".
   - Display the pie chart with correctly labeled slices.

5. Ensure Proper Code Structure:
   - The code should use functions for different tasks (reading CSV, computing statistics, creating charts, and displaying results).
   - Make sure all necessary libraries are imported at the beginning of the code.

**Generate Python code only**, without any explanations, comments, or unnecessary text. The output must start immediately with Python code, and there should be no headers or explanations.
"""

# Step 3: Define the API endpoint and headers for KoboldCpp
api_url = "http://localhost:5001/api/v1/generate"  # Update this URL if your KoboldCpp API is running on a different port
headers = {"Content-Type": "application/json"}

# Define the payload for the request
payload = {
    "prompt": prompt,
    #"max_new_tokens": 300,  # Allow sufficient tokens for complete code output
    "temperature": 0,  # Lower temperature for more deterministic output
    "max_length": 1024,
    "rep_pen": 1.1,
}

# Step 4: Send the request to the KoboldCpp API
response = requests.post(api_url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Extract the generated Python code from the response
    raw_output = response.json()
    pie_code = raw_output.get("results", [{}])[0].get("text", "").strip()

    # Print the original output for reference
    print("Model Output:\n")
    print(pie_code)

    # Step 5: Clean the generated code to remove unnecessary text
    code_block = re.search(r'```python(.*?)```', pie_code, re.DOTALL)

    if code_block:
        extracted_code = code_block.group(1).strip()  # Extract and clean the code
        #print("Extracted Python code:\n")
        #print(extracted_code)
        
        # Step 5: Save the extracted code to a file
        with open("pie_plot.py", "w", encoding="utf-8") as file:
            file.write(extracted_code)
        
        # Step 6: Execute the extracted Python code
        exec(extracted_code)

    print("\nThe generated Python code has been saved to 'pie_plot.py'. You can run it to create the pie chart.")
else:
    print(f"Error: Unable to generate code. Status code {response.status_code}, Response: {response.text}")
