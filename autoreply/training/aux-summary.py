import json
import csv

def parse_completion(completion):
    # Split the completion string into numbers, removing "Reduced Narrative: " and "</s>"\\
    completion = completion.replace("</s>", "")
    numbers = completion.replace("Reduced Narrative: ", "").split(", ")
    # Convert each number from string to int
    #print(completion)

    #numbers = [5,5,5,5,5,5,5]
    #try:
    numbers = [int(num) for num in numbers]
    #
    #except:
    #    return numbers
    
    return numbers

def process_jsonl_file_to_csv(jsonl_filepath, csv_filepath):
    with open(jsonl_filepath, 'r') as jsonl_file, open(csv_filepath, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Define the headers based on the metrics we are evaluating
        headers = ["clarity_of_expression", "appropriateness_of_diction", "engagement_and_interest", "use_of_clich", "narrative_flow", "stylistic_elegance", "aesthetic_appeal"]
        # Write the header
        csv_writer.writerow(headers)
        
        for line in jsonl_file:
            data = json.loads(line)
            completion = data.get("completion", "")
            #print(completion)
            # Parse the completion value to extract numbers
            numbers = parse_completion(completion)
            # Write the parsed numbers to the CSV file
            csv_writer.writerow(numbers)

if __name__ == "__main__":
    jsonl_filepath = "aux-babbage-train-plus.jsonl"  # Update this with the path to your .jsonl file
    csv_filepath = "aux-babbage.csv"  # Output CSV file name changed as per requirement
    process_jsonl_file_to_csv(jsonl_filepath, csv_filepath)
