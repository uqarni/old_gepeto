import pandas as pd

def cleaner(df):
    #take df and return jsonl file
    jsonlz = ""
    for index,row in df.iterrows():
        raw_data = row["raw text"]

        for index,i in enumerate(raw_data):
            if i == "{":
                start = index
            elif i == "}":
                end = index
                jsonlz = jsonlz + raw_data[start:(end+1)]
                jsonlz = jsonlz + "\n"

    return jsonlz

# df = pd.read_csv('training_data_5.csv')
# only_jsonls = cleaner(df)
# final_training_data = open("cleansed_training_data_2.jsonl", "x")
# final_training_data.write(only_jsonls)
# print(final_training_data.read())


def uploader(prompt_responses_file_path):
    #upload it to openai
    file_name = prompt_responses_file_path
    import openai

    apikey = ""
    openai.api_key = apikey

    send = openai.File.create(
        file=open(file_name, "rb"),
        purpose='fine-tune'
    )

    return send["id"]

test = uploader("cleansed_training_data_2.jsonl")
    

def file_status(file_id):
    status = 'foo'
    return status

def fine_tuner(file_id, model):
    task_id = "foo"
    return task_id

def model_status(task_id):
    model_id = "foo"
    return model_id

def query_model(model_id, prompt, tokens = 200):
    return 0
