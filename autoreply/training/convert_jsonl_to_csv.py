file_path = 'babbage-train.jsonl'  # Replace with your JSONL file path


import json

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return data

jsonl_data = load_jsonl(file_path)
#print(jsonl_data)  # This will print the loaded data to verify it's loaded correctly

results = []

for item in jsonl_data:
    prompt = item.get('prompt', '')
    completion = item.get('completion', '')
    results.append([prompt, prompt, completion, completion])

#print(results)


import csv

def write_results_to_csv(results, output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['text', 'text', 'label', 'target'])  # Write the header row
        writer.writerows(results)

output_csv_path = 'training-from-jsonl.csv'  # Name of the CSV file to write to
write_results_to_csv(results, output_csv_path)

    