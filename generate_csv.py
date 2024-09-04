#model: llava-llama-3-8b-v1_1-int4
import requests
import csv

file_path = '年末常住人口.txt'  # Replace with your file path
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

#data_lines = lines[4:-2]  # Keep only the data part, skip the description

# Combine the core data
input_text = "".join(lines).strip()

prompt = f"""
The following is the population data of Chinese provinces over the past 10 years. Please output the data in CSV format. 
The first row should be "地区,2023年,2022年,2021年,2020年,2019年,2018年,2017年,2016年,2015年,2014年".

Data:
{input_text}

Output the data in CSV format with one line per province, including the province name and the population data for each year.Be careful to remove invalid information from the header and footer.
"""

payload = {
    "prompt": prompt,
    #"max_new_tokens": 2000,  # Increased to ensure enough tokens for complete output
    "temperature": 0,      # Lowered for more deterministic output
    "max_length": 1500,
    #"top_p": 1.0,            # Higher value to include more diverse tokens
}

api_url = "http://localhost:5001/api/v1/generate"

response = requests.post(api_url, json=payload)

if response.status_code == 200:
    raw_output = response.json()
    print(raw_output)
    # Extract generated text from the response
    generated_text = response.json().get('results')[0]['text'].strip()

    if generated_text.startswith("```") and generated_text.endswith("```"):
        generated_text = generated_text[3:-3].strip()  # Remove the starting and ending ```

    # Further clean up any lines that are not CSV formatted
    lines = generated_text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip() and ',' in line]  # Keep only valid CSV lines

    output_file_path = 'people_output.csv'
    with open(output_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Split the generated text by line and comma, and write to CSV
        for line in generated_text.splitlines():
            writer.writerow(line.split(','))  # Assuming generated text is already in CSV format

    print(f"CSV file has been saved to: {output_file_path}")
else:
    print(f"Error: {response.status_code} - {response.text}")
