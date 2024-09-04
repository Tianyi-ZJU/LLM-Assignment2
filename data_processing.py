#model: starcoder2-15b-instruct-v0.1-Q4_K_M
import requests
import pandas as pd
import re

# Step 1: Read the CSV file
file_name = "people_output.csv"
df = pd.read_csv(file_name)

# Step 2: Generate a prompt for the model based on the actual CSV file content
prompt = """
You are an AI assistant that generates **Python code only**. I have a CSV file named "people_output.csv" containing the population data for various regions in China over the last 10 years. The structure of the CSV file is as follows:

Column Headers: "地区,2023年,2022年,2021年,2020年,2019年,2018年,2017年,2016年,2015年,2014年"
Sample Data:
北京市,2186,2184,2189,2189,2190,2192,2194,2195,2188,2171
天津市,1364,1363,1373,1387,1385,1383,1410,1443,1439,1429
河北省,7393,7420,7448,7464,7447,7426,7409,7375,7345,7323
山西省,3466,3481,3480,3490,3497,3502,3510,3514,3519,3528
内蒙古自治区,2396,2401,2400,2403,2415,2422,2433,2436,2440,2449

Each row after the header contains the population data for a specific region over the last 10 years, from 2023 to 2014.

**Generate Python code only** to perform the following tasks without any explanation or additional text:

1. Read and Load the CSV File using pandas.
   - Use pandas to read the CSV file named "people_output.csv".

2. Compute Statistics:
   - For each region (row in the DataFrame), compute the average, maximum, and minimum population over the last 10 years (from columns 2023 to 2014).
   - Ensure that the calculations are performed **for each row (region)** and **not for each column**.
   - Add three new columns to the DataFrame with these values: "平均人口" (average population), "最大人口" (maximum population), and "最小人口" (minimum population).

3. Save the Updated CSV File:
   - Save the updated DataFrame with the new columns back to a new CSV file named "people_output_updated.csv".

**Output only Python code** without any explanations, comments, or unnecessary text. The output must start immediately with Python code, and there should be no headers or explanations.
"""


# Step 3: Define the API endpoint and headers for KoboldCpp
api_url = "http://localhost:5001/api/v1/generate"  # Update this URL if your KoboldCpp API is running on a different port
headers = {"Content-Type": "application/json"}

# Define the payload for the request
payload = {
    "prompt": prompt,
    #"max_new_tokens": 2000,  # Increased to ensure enough tokens for complete output
    "temperature": 0,      # Lowered for more deterministic output
    "max_length": 250,
    "top_p": 0.8,
    "rep_pen": 1.1,
}

# Step 4: Send the request to the KoboldCpp API
response = requests.post(api_url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Extract the generated Python code from the response
    raw_output = response.json()
    print(raw_output)
    generated_code1 = response.json()["results"][0]["text"]
    
    # Use regex to find Python code blocks
    code_block = re.search(r'```python(.*?)```', generated_code1, re.DOTALL)
    
    if code_block:
        extracted_code = code_block.group(1).strip()  # Extract and clean the code
        #print("Extracted Python code:\n")
        #print(extracted_code)
        
        # Step 5: Save the extracted code to a file
        with open("extracted_code.py", "w", encoding="utf-8") as file:
            file.write(extracted_code)
        
        # Step 6: Execute the extracted Python code
        exec(extracted_code)
        
        print("The code has been executed successfully, and the updated CSV file has been saved.")
    else:
        print("No Python code block found in the generated content.")
else:
    print(f"Error: Unable to generate code. Status code {response.status_code}")
