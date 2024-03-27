#from peft import get_peft_model, LoraConfig

#lora_config = LoraConfig.from_pretrained("./results")
#model = get_peft_model(lora_config)


#quit()




from transformers import AutoModelForCausalLM, AutoTokenizer

# Specify the path to your model's save directory
model_path = './results'  # Adjust this path to where your model is saved

model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

model.eval()  # Set the model to evaluation mode

# Prepare input text
input_text = "### Human: Reduce Narrative (sentiment, pacing, plotting): Sara's heart raced as she arrived at the airport, scanning the bustling crowd for a familiar face. Just as worry began to gnaw at her, she felt a tap on her shoulder. Turning around, tears welled up as she saw her best friend standing there, a wide smile breaking across her face.### "

# Tokenize input and create attention masks
inputs = tokenizer.encode_plus(
    input_text, 
    return_tensors="pt", 
    add_special_tokens=True, 
    max_length=512,  # Adjust based on your model's max length
    pad_to_max_length=True,  # Ensures all sequences are padded to the same length
    return_attention_mask=True  # Generates attention mask
)

input_ids = inputs["input_ids"]
attention_mask = inputs["attention_mask"]

input_ids.to("cuda")

# Generate text
# Adjust the parameters as needed (e.g., max_length, num_beams for beam search)
#output = model.generate(input_ids, max_length=50, num_beams=5, early_stopping=True, max_new_tokens=80)
# Generate text using the model and attention mask
output = model.generate(
    input_ids=input_ids, 
    attention_mask=attention_mask, 
    max_new_tokens=80, 
    num_beams=5, 
    early_stopping=True
)

# Decode the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
