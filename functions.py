import pandas as pd
import jsonlines
import openai
apikey = "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"
openai.api_key = apikey

#DONE input is dataframe and output is a list of strings
def cleaner(df):
    #take df and return jsonl file
    jsonlz = []
    for index,row in df.iterrows():
        raw_data = row["raw text"]

        for index,i in enumerate(raw_data):
            if i == "{":
                start = index
            elif i == "}":
                end = index
                content = raw_data[start:(end+1)]

                jsonlz.append(raw_data[start:(end+1)])
                              
    return jsonlz




#DONE input is a list of strings and output is an ID of the file in openai's databasee
def uploader(list_of_strings):
    import jsonlines
    import json
    import openai

    with open('output.jsonl', 'w') as f:
    # iterate over the list of strings
        for s in list_of_strings:
            try: 
                # convert string to dictionary
                d = json.loads(s)
                # write dictionary to file
                json.dump(d, f)
                # add newline character to separate dictionaries
                f.write('\n')
            except ValueError:
                pass

    apikey = "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"
    openai.api_key = apikey

    #upload it to openai
    send = openai.File.create(
        file=open("fine_tune_file_2.jsonl", "rb"),
        purpose='fine-tune'
    )

    return send["id"]


#file-mPNvw5BZK8leRai3eajrD38o for first fine tune attempt
def fine_tuner(file_id, model="davinci"):
    import openai
    apikey = "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"
    openai.api_key = apikey

    send = openai.FineTune.create(
        training_file= file_id, 
        model = model, 
        suffix = "weaknesses_1")
    output = {
        "fine-tuning id": send["id"],
        "status": send["events"][0]["message"]
    }
    print(output)
    return output
    
def model_status(ft_id):
    send = openai.FineTune.retrieve(ft_id)
    output = {
        "model": send["model"],
        "fine_tuned_model": send["fine_tuned_model"],
        "status": send["status"]
    }
    print(output)
    return output

test = model_status(ft_id)

def query_model(model_id, prompt, tokens = 200):
    send = openai.Completion.create(
        model = model_id,
        prompt = prompt,
        max_tokens = tokens)
    
    output = send["choices"][0]["text"]
    print(output)
    return output
    

test = query_model(model_id = "davinci:ft-personal:weaknesses-1-2023-02-25-21-28-09", prompt = "What do I say if I'm too old?", tokens = 50)
