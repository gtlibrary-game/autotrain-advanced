import glob

# Directory where the TXT files are stored
directory_path = "data"

# Use glob to find all non-zero byte .txt files in the specified directory
txt_files = glob.glob(f"{directory_path}/*.txt")

def parse_txt_files(file_paths):
    extracted_data = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
            
            generated_text, sentiment, pacing, plotting = "", "", "", ""
            for line in lines:
                if line.startswith("Generated Text:"):
                    generated_text = line.replace("Generated Text:", "").strip()
                elif line.startswith("Sentiment Classification:"):
                    sentiment = line.replace("Sentiment Classification:", "").strip()
                elif line.startswith("Pacing Assessment:"):
                    pacing = line.replace("Pacing Assessment:", "").strip()
                elif line.startswith("Plot Dynamics Classification:"):
                    plotting = line.replace("Plot Dynamics Classification:", "").strip()

            if generated_text and sentiment and pacing and plotting:
                extracted_data.append({
                    "prompt": "Reduce Narrative (sentiment, pacing, plotting): " + generated_text + "</end>",
                    "completion": f"Reduced Narrative: {sentiment}, {pacing}, {plotting}</s>{plotting}</s>{plotting}</s>"
                })            
    
    return extracted_data


# Parse the non-zero byte .txt files
extracted_data = parse_txt_files(txt_files)

import json

# Assuming extracted_data is populated with the data structure from the updated parse_txt_files function
with open("babbage-train.jsonl", 'w', encoding='utf-8') as f:
    f.write(open("babbage-train-plus-plus.jsonl", "r").read())
    
    for data in extracted_data:
        # Convert dictionary to JSON string and write it to the file
        f.write(json.dumps(data) + '\n')

        