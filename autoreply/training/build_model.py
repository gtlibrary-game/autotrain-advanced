from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "huawei-noah/TinyBERT_General_4L_312D"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3) # Assuming 3 labels for sentiment, pacing, plotting
tokenizer = AutoTokenizer.from_pretrained(model_name)

from datasets import load_dataset

# Load the dataset
dataset = load_dataset('csv', data_files='training.csv')

# Access the 'train' split for operations like iteration
train_dataset = dataset['train']

# Example: Iterating over the train dataset
for example in train_dataset:
    print(example)  # This will print out each example in the train dataset

######## Train@@@@@@@@@!!!!!!!!!!########@!#$!!!!!!@################

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,  # make sure your model is defined
    args=training_args,
    train_dataset=train_dataset,  # Here's where you specify the correct dataset split
    # eval_dataset=dataset['validation'] if 'validation' in dataset else None,
)

trainer.train()

