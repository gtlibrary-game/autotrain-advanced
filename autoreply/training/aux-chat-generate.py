import openai
import os
import time
from openai import AssistantEventHandler
from typing_extensions import override
import random
import tempfile
import argparse

data_dir = "aux-chat-data"

# Setup OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
# Ensure the API key is available
if openai.api_key is None:
    raise ValueError("OpenAI API key not found in environment variables")

client = openai.OpenAI()

# Load instructions from a file
instructions_path = "aux-chat-instructions.txt"
if not os.path.exists(instructions_path):
    raise FileNotFoundError(f"{instructions_path} not found")
with open(instructions_path, 'r') as file:
    instructions = file.read()

# Create an Assistant
assistant = client.beta.assistants.create(
  name="Data Generator",
  instructions=instructions,
   tools=[],
  model="gpt-3.5-turbo",
)

# Function to generate a message based on the given options
def generate_message():
    clarity_of_expression = ["Clear", "Unclear"]
    appropriateness_of_diction = ["Appropriate", "Inappropriate"]
    engagement_and_interest = ["Engaging", "Disengaging"]
    use_of_clichés = ["Original", "Clichéd"]
    narrative_flow = ["Smooth", "Jarring"]
    stylistic_elegance = ["Elegant", "Inelegant"]
    aesthetic_appeal = ["Beautiful", "Mundane"]
    
    # Randomly select one option from each analysis criteria
    selected_clarity = random.choice(clarity_of_expression)
    selected_diction = random.choice(appropriateness_of_diction)
    selected_engagement = random.choice(engagement_and_interest)
    selected_clichés = random.choice(use_of_clichés)
    selected_flow = random.choice(narrative_flow)
    selected_elegance = random.choice(stylistic_elegance)
    selected_appeal = random.choice(aesthetic_appeal)
    
    # Combine the selections into a single analysis message
    analysis_message = (
        f"Clarity of Expression: {selected_clarity}, "
        f"Appropriateness of Diction: {selected_diction}, "
        f"Engagement and Interest: {selected_engagement}, "
        f"Use of Clichés: {selected_clichés}, "
        f"Narrative Flow: {selected_flow}, "
        f"Stylistic Elegance: {selected_elegance}, "
        f"Aesthetic Appeal: {selected_appeal}"
    )
    return analysis_message

class EventHandler(AssistantEventHandler):
  #def __init__(self, file_handle):
  #  self.file_handle = file_handle   

  def myinit(self, content, file_handle):
     self.content = content
     self.file_handle = file_handle
     return self 

  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
    self.file_handle.write(self.content + "\n---\n")
    #self.file_handle.write("\nassistant > ")
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
    self.file_handle.write(delta.value)

  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)


# Ensure the data directory exists

os.makedirs(data_dir, exist_ok=True)

def from_file_digest(digest_file):
    try:
        return digest_file.read(200 * 8);
    except:
        print("File ran out. We are done. Exiting.")
        quit()

def handle_conversation(i, file_handle, digest_file):
    # Create a Thread
    thread = client.beta.threads.create()
        
    #mock_content = generate_message()
    mock_content = from_file_digest(digest_file)

    print(mock_content)

    # Add a Message to the Thread
    message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=mock_content
    )

    with client.beta.threads.runs.create_and_stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            #instructions="Start with: Generated Text:",
            event_handler=EventHandler().myinit(mock_content, file_handle),
    ) as stream:
            stream.until_done()


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


# Setup argument parser
parser = argparse.ArgumentParser(description='Generate conversations and write responses to individual files.')
parser.add_argument('--count', type=int, default=10, help='Number of conversations to generate (default: 10)')

# Parse arguments
args = parser.parse_args()

import json
import re

pattern = re.compile(r": (\d+)\. ")

# Main execution
if __name__ == "__main__":
    # Parse command line arguments for the count
    digest_file = open("aux-narrative.txt", "r", encoding='utf-8', errors='replace')

    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=data_dir, prefix="chat", suffix=".special") as temp_base:

        for i in range(args.count):
            with open(temp_base.name + "---" + str(i) + ".txt", "w") as temp_file:
                print(f"Generating conversation {i+1}, writing to: {temp_file.name}")
                try: 
                    handle_conversation(i, temp_file, digest_file)
                except Exception as e:
                    print("Prompt failed: " + e + "\nContinuing...")             

                temp_file_path = temp_file.name

            with open(temp_base.name + "---" + str(i) + ".txt", "r", encoding='utf-8', errors='replace') as temp_file:
                lines = temp_file.readlines()

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
                                
                                #metrics[metric] = find_category_value(line, values)
                                #metrics[metric] ~= line.match(/: {\d+}\. /).group(1 or 0, the matching digit(s)) #FIXME Make this code work matching the 3 in: ""...: 3."
                                match = pattern.search(line)

                                # Check if we found a match and extract the first group (the digits)
                                if match:
                                    metrics[metric] = int(match.group(1))  # This extracts the matching digits
                                else:
                                    metrics[metric] = 5  # Or some default/fallback value

                #print(file_path + ": " + str(narrative_collected))
                #print(metrics.values())
                                
                if narrative_collected and all(value != "" for value in metrics.values()):
                    metrics_values = ", ".join([f"{value}" for value in metrics.values()])
                    temp_base.write(
                        json.dumps({
                            "prompt": "Reduce Narrative (" + ", ".join([key for key in metrics.keys()]) + "): " + " ".join(generated_narrative) + "</end>",
                            "completion": f"Reduced Narrative: {metrics_values}</s>"
                        }) + "\n"
                    )          
               
               
            print(f"Completed. Responses for conversation {i+1} written to {temp_file_path}.")
