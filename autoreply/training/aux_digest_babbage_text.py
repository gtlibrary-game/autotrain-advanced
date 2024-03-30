from openai import OpenAI
import pickle

client = OpenAI()


narrative_path = 'aux-narrative.txt'
with open(narrative_path, 'r', encoding='utf-8') as file:
    narrative_content = file.read()

#FIXME: Digest the text in a loop based on x number of characters
# FIXME: Digest the text in a loop based on x number of characters
# Define the maximum number of characters per segment. Adjust based on your requirements.
max_chars_per_segment = 200 * 8  # Example value is 200 ~ 50 words

segments = [narrative_content[i:i+max_chars_per_segment] for i in range(0, len(narrative_content), max_chars_per_segment)]

#FIXME: Pass in the new prompt with the boilerplate

boilerplate = "Reduce Narrative (clarity_of_expression, appropriateness_of_diction, engagement_and_interest, use_of_clich, narrative_flow, stylistic_elegance, aesthetic_appeal): "
responses = []
boilerbutt = "</end>"

import json

# Assuming extracted_data is populated with the data structure from the updated parse_txt_files function
with open("aux-babbage-train-plus.jsonl", 'a', encoding='utf-8') as jsonl_file:
    for segment in segments:
        prompt = boilerplate + segment + boilerbutt
        completion = client.completions.create(
            model="ft:davinci-002:the-great-library:autoaux:98Eitlq1",
            prompt=prompt,
            max_tokens=70,
            stop=["</s>", "\n"],
            temperature=0
        )
        # Extract the text from the first (and presumably only) choice.
        #print(completion)
        text = completion.choices[0].text.strip()
        responses.append(text)
        print(json.dumps(
            {
                "prompt": prompt,
                "completion": text
            }        
        ) + '\n')

        jsonl_file.write(json.dumps(
            {
                "prompt": prompt,
                "completion": text
            }        
        ) + '\n')
