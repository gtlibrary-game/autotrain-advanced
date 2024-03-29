import json
import csv

# Define the categories with their associated classes and corresponding numbers
categories = {
    "speed": {
        "Fast": 1,
        "Moderate": 0,
        "Slow": -1
    },
    "sentiment": {
        "Positive": 1,
        "Neutral": 0,
        "Negative": -1
    },
    "conflict": {
        "Conflict Rising": 1,
        "Conflict Resolving": -1
    }
}

def parse_completion(completion):
    # Initialize the results with default values
    results = {"sent": 0, "speed": 0, "conflict": 0}

    # Check for each keyword in the completion string and update results
    for category, options in categories.items():
        for option, value in options.items():
            if option in completion:
                if category == "speed":
                    results["speed"] = value
                elif category == "sentiment":
                    results["sent"] = value
                elif category == "conflict":
                    results["conflict"] = value
                break  # Stop searching after the first match in each category

    return results

def process_jsonl_file_to_csv(jsonl_filepath, csv_filepath):
    with open(jsonl_filepath, 'r') as jsonl_file, open(csv_filepath, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header
        csv_writer.writerow(["sent", "speed", "conflict"])
        
        for line in jsonl_file:
            data = json.loads(line)
            completion = data.get("completion", "")
            # Parse the completion value to categorize and assign numbers
            results = parse_completion(completion)
            # Write the parsed data to the CSV file
            csv_writer.writerow([results["sent"], results["speed"], results["conflict"]])

if __name__ == "__main__":
    jsonl_filepath = "babbage-train-plus.jsonl"  # Update this with the path to your .jsonl file
    csv_filepath = "babbage.csv"  # Name and path for the output CSV file
    process_jsonl_file_to_csv(jsonl_filepath, csv_filepath)
