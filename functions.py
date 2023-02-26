import pandas as pd
import jsonlines
import openai
apikey = ""
openai.api_key = apikey

#input is a txt file and output a data frame with one column titled 'raw text'
def raw_pr(file, cycles = 5):
    import openai
    import pandas as pd

    #openai credentials
    apikey = ""
    openai.api_key = apikey

    #create header and footer. initalize body.
    topic = "talking about your weaknesses in a job interview"
    header = "The text below is an excerpt from a document on " + topic + ":\n\n\""
    body = ""
    footer = "\"\n\nConvert the above text into prompt-completion pairs to train a chatbot in JSONL format:\n\n"
    format = "{\"prompt\": \"Question?\",\"completion\": Answer to question from above text. ENDEND\"}\n\nProvide 3 prompt-completion pairs in this format on consecutive lines."
   
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
        print("a data frame with one column, titled 'raw text', that has strings")
        return training_data

      
#input is dataframe and output is a list of strings
def pr_cleaner(df):
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
def pr_uploader(list_of_strings):
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

    apikey = ""
    openai.api_key = apikey

    #upload it to openai
    send = openai.File.create(
        file=open("fine_tune_file_2.jsonl", "rb"),
        purpose='fine-tune'
    )
    print(send["id"])
    return send["id"]

  
#input is openAI file ID and model, output is dictionary with keys: fine-tuning id and status
def fine_tuner(file_id, model="davinci"):
    import openai
    apikey = ""
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

  
#input is openAI model ID, output is dictionary with keys: model, fine-tune model, and status     
def model_status(ft_id):
    send = openai.FineTune.retrieve(ft_id)
    output = {
        "model": send["model"],
        "fine_tuned_model": send["fine_tuned_model"],
        "status": send["status"]
    }
    print(output)
    return output

  
#input is fine-tune model id, prompt as string, and # of tokens
def query_model(model_id, prompt, tokens = 200):
    send = openai.Completion.create(
        model = model_id,
        prompt = prompt,
        max_tokens = tokens)
    
    output = send["choices"][0]["text"]
    print(output)
    return output
    
