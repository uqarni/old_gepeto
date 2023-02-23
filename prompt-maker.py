###architecture
#FUNCTION1: DATAFRAME WITH RAW TEXT (input: data file, cycles output: dataframe)
#FUNCTION2: DATAFRAME CLEANSER
#FUNCTION3: FINE-TUNE MODEL MAKER

import openai
import pandas as pd

def raw_promptr(file, cycles = 1):
    import openai
    import pandas as pd

    #openai credentials
    apikey = "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"
    openai.api_key = apikey

    #create header and footer. initalize body.
    topic = "talking about your weaknesses in a job interview"
    header = "The text below is an excerpt from a document on " + topic + ":\n\n"
    body = ""
    footer = "\n\nConvert the above text into prompt-completion pairs to train a chatbot in the format:\n\n"
    format = "{\"prompt:\" \"Question?\",\"completion:\" Answer to question from above text. ENDEND\"}\n\nProvide 3 prompt-completion pairs in this format."
   
    training_data = pd.DataFrame()
    training_data["raw text"] = ""

    #determine max characters for the body
    max_prompt_tokens = 400
    max_body_chars = max_prompt_tokens*3.5 - len(header + footer + format)
    max_response_tokens = 400

    # open text file, read lines, remove all lines with just \n. save as var list text
    with open(file) as f:
        contents = f.readlines()
        i = len(training_data.index)
        for cycle in range(0,cycles):
            for line in contents:
                if len(body+line) <= max_body_chars:
                    body = body + line
                else:
                    #query openai
                    prompt = header + body + footer + format

                    response = openai.Completion.create(
                        model= "text-davinci-003",
                        prompt= prompt,
                        max_tokens = max_response_tokens)
                    #extract prompts and responses
                    training_data.loc[i, "raw text"] = response["choices"][0]["text"]
                    i+=1
                    #reset body
                    body = ""
    return training_data

training_data_5 = raw_promptr("weaknesses.txt")
training_data_5.to_csv("training_data_5.csv")

def cleaner(df):
    import pandas
    #take df and return jsonl file
    jsonl_file = 'foo'

    return jsonl_file

def uploader(prompt_responses):
    #upload it to openai
    id = 'foo'
    return id

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
    

    
        










            

            

            






