import time
from openai import OpenAI
client = OpenAI()

fileid = client.files.create(
  file=open("babbage-train.jsonl", "rb"),
  purpose="fine-tune"
)

print(fileid.id)

from openai import OpenAI
client = OpenAI()

job = client.fine_tuning.jobs.create(
  training_file=fileid.id, 
  #model="davinci-002",
  model="ft:davinci-002:personal:autoreply:97TOdVoJ",
  suffix="autoreply"
)

print(job)

job_id = job.id

# Define a loop to check the job's status
while True:
    # Fetch the current status of the job
    job_status = client.fine_tuning.jobs.retrieve(job_id)

    # Check if the job is completed (either succeeded or failed)
    if job_status.status in ['succeeded', 'failed']:
        print(f"Job {job_id} completed with status: {job_status.status}")
        if job_status.status == 'succeeded':
            # If the job succeeded, you can access the fine-tuned model ID
            print(f"Fine-tuned model ID: {job_status.fine_tuned_model}")
        break  # Exit the loop if the job is completed

    # If the job is not yet completed, wait for a bit before checking again
    print(f"Job {job_id} is still in progress. Current status: {job_status.status}. Waiting for 30 seconds before checking again.")
    time.sleep(30)  # Wait for 30 seconds before the next status check

print(job)