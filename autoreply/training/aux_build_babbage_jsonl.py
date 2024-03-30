import glob

# Directory where the TXT files are stored
directory_path = "aux-data"

# Use glob to find all non-zero byte .txt files in the specified directory
txt_files = glob.glob(f"{directory_path}/*.txt")

# Predefined categories for each metric
categories = {
    "clarity_of_expression": ["Clear", "Unclear"],
    "appropriateness_of_diction": ["Appropriate", "Inappropriate"],
    "engagement_and_interest": ["Engaging", "Disengaging"],
    "use_of_clich": ["Original", "Clich"],
    "narrative_flow": ["Smooth", "Jarring"],
    "stylistic_elegance": ["Elegant", "Inelegant"],
    "aesthetic_appeal": ["Beautiful", "Mundane"]
}

def find_category_value(line, category_values):
    for value in category_values:
        if value in line:
            return value
    return "Unknown"  # Fallback value if none of the categories match

def parse_txt_files(file_paths):
    extracted_data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()

            # Initialize the narrative collection
            narrative_collected = False
            generated_narrative = []
            metrics = {key: "" for key in categories.keys()}

            for line in lines:
                if line.strip() == "---":  # Check for the delimiter to stop narrative collection
                    narrative_collected = True
                    continue

                if not narrative_collected:
                    generated_narrative.append(line.strip())
                else:
                    for metric, values in categories.items():

                        if metric.replace("_", " ") in line.lower():
                            
                            metrics[metric] = find_category_value(line, values)

            #print(file_path + ": " + str(narrative_collected))
            #print(metrics.values())
                            
            if narrative_collected and all(value != "" for value in metrics.values()):
                metrics_values = ", ".join([f"{value}" for value in metrics.values()])
                extracted_data.append({
                    "prompt": "Reduce Narrative (" + ", ".join([key for key in metrics.keys()]) + "): " + " ".join(generated_narrative) + "</end>",
                    "completion": f"Reduced Narrative: {metrics_values}</s>"
                })            

    return extracted_data

# Parse the non-zero byte .txt files
extracted_data = parse_txt_files(txt_files)

import json

# Assuming extracted_data is populated with the data structure from the updated parse_txt_files function
with open("aux-babbage-train.jsonl", 'w', encoding='utf-8') as f:
    f.write(open("aux-babbage-train-plus-plus.jsonl", "r").read())
    
    for data in extracted_data:
        # Convert dictionary to JSON string and write it to the file
        f.write(json.dumps(data) + '\n')
