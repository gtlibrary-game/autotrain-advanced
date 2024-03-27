# Criteria lists
sentiments = ['Positive', 'Neutral', 'Negative']
pacings = ['Fast', 'Moderate', 'Slow']
conflicts = ['Conflict Rising', 'Conflict Resolving']


import json

def clean_and_filter_dataset(file_path):
    # Store the cleaned data
    cleaned_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # Parse JSON line
                entry = json.loads(line)

                # Extract the completion text
                completion_text = entry.get('completion', '').lower()

                # Check if the completion text matches the criteria
                if any(sentiment.lower() in completion_text for sentiment in sentiments) and \
                   any(pacing.lower() in completion_text for pacing in pacings) and \
                   any(conflict.lower() in completion_text for conflict in conflicts):
                    # Create the structured label
                    structured_label = "Reduced Narrative: " + \
                                       next((sentiment for sentiment in sentiments if sentiment.lower() in completion_text), 'Unknown') + ", " + \
                                       next((pacing for pacing in pacings if pacing.lower() in completion_text), 'Unknown') + ", " + \
                                       next((conflict for conflict in conflicts if conflict.lower() in completion_text), 'Unknown') + "</s>" + \
                                       next((conflict for conflict in conflicts if conflict.lower() in completion_text), 'Unknown') + "</s>" + \
                                    next((conflict for conflict in conflicts if conflict.lower() in completion_text), 'Unknown') + "</s>"
                    
                    # Append to cleaned data
                    cleaned_data.append({
                        "prompt": entry['prompt'],
                        "completion": structured_label
                    })
            except json.JSONDecodeError:
                print(f"Error decoding JSON from line: {line}")
                continue

    return cleaned_data


def save_cleaned_data(cleaned_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for entry in cleaned_data:
            json.dump(entry, file)
            file.write('\n')



file_path = 'babbage-train-plus.jsonl'
output_path = 'babbage-train-plus-plus.jsonl'

# Load, filter, and clean the dataset
cleaned_data = clean_and_filter_dataset(file_path)

# Save the cleaned data to a new file
save_cleaned_data(cleaned_data, output_path)
