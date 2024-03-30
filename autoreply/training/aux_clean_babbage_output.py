import json

# New criteria lists
categories = {
    "clarity_of_expression": ["Clear", "Unclear"],
    "appropriateness_of_diction": ["Appropriate", "Inappropriate"],
    "engagement_and_interest": ["Engaging", "Disengaging"],
    "use_of_cliché": ["Original", "Clichéd"],  # Adjusted key name for consistency
    "narrative_flow": ["Smooth", "Jarring"],
    "stylistic_elegance": ["Elegant", "Inelegant"],
    "aesthetic_appeal": ["Beautiful", "Mundane"]
}

def find_category_value(text, category_values):
    for value in category_values:
        if value.lower() in text:
            return value
    return "Unknown"  # Fallback value if none of the categories match

def clean_and_filter_dataset(file_path):
    cleaned_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                entry = json.loads(line)
                completion_text = entry.get('completion', '').lower()

                # Check and extract category values from the completion text
                category_values = {}
                for category, values in categories.items():
                    category_values[category] = find_category_value(completion_text, values)

                # Only include entries that do not have 'Unknown' as a category value
                if all(value != "Unknown" for value in category_values.values()):
                    structured_label = "Reduced Narrative: " + ", ".join(category_values.values()) + "</s>"
                    
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

file_path = 'aux-babbage-train-plus.jsonl'
output_path = 'aux-babbage-train-plus-plus.jsonl'

# Load, filter, and clean the dataset
cleaned_data = clean_and_filter_dataset(file_path)

# Save the cleaned data to a new file
save_cleaned_data(cleaned_data, output_path)
