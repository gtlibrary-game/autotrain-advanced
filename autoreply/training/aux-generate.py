import openai
import os
import time
from openai import AssistantEventHandler
from typing_extensions import override
import random
import tempfile
import argparse

data_dir = "aux-data"

# Setup OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
# Ensure the API key is available
if openai.api_key is None:
    raise ValueError("OpenAI API key not found in environment variables")

client = openai.OpenAI()

# Load instructions from a file
instructions_path = "aux-instructions.txt"
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

  def myinit(self, file_handle):
     self.file_handle = file_handle
     return self 

  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
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

def handle_conversation(i, file_handle):
    # Create a Thread
    thread = client.beta.threads.create()
        
    mock_content = generate_message()
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
            event_handler=EventHandler().myinit(file_handle),
    ) as stream:
            stream.until_done()


# Setup argument parser
parser = argparse.ArgumentParser(description='Generate conversations and write responses to individual files.')
parser.add_argument('--count', type=int, default=10, help='Number of conversations to generate (default: 10)')

# Parse arguments
args = parser.parse_args()

# Main execution
if __name__ == "__main__":
    # Parse command line arguments for the count
    for i in range(args.count):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=data_dir, prefix="chat", suffix=".txt") as temp_file:
            print(f"Generating conversation {i+1}, writing to: {temp_file.name}")
            handle_conversation(i, temp_file)
            temp_file_path = temp_file.name
        print(f"Completed. Responses for conversation {i+1} written to {temp_file_path}.")
