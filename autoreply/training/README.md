Two ways of thinking:

Gernerate 10 (or more) training data using: python3 generate.py --count 10


Or you can set the "narrative.txt" and run the following command:
$ python3 digest_babbage_text.py

Note: This will add dirty output to the "babbage-train-plus.jsonl" file

Clean "babbage-train-plus.jsonl" for training:
$ python3 clean_babbage_output.py

Note: Running clean will overwrite the babbage-train-plus-plus.jsonl 

Now rebuild the training data
$ python3 build_babbage_jsonl.py

Now you are ready to fine tune:
$ python3 tune-babbage.py

Note: You will get a new model outputted. Replace the model in: "digest_babbage_text.py" with it before calling digest