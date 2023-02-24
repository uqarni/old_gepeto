import pandas as pd
import jsonlines

#input is dataframe and output is a list of strings
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




#input is a list of strings and output is an ID of the file in openai's databasee
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

test = uploader(cleaner(pd.read_csv("training_data_6.csv")))
print(test)
    

def file_status(file_id):
    status = 'foo'
    return status


#file-mPNvw5BZK8leRai3eajrD38o for first fine tune attempt
def fine_tuner(file_id, model="davinci"):
    import openai
    openai.FineTune.create(
        training_file= file_id, 
        model = "davinci", 
        suffix = "weaknesses_1")
    return task_id

def model_status(task_id):
    model_id = "foo"
    return model_id

def query_model(model_id, prompt, tokens = 200):
    return 0
