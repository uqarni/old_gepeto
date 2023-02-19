import openai

#openai credentials
apikey = "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"
openai.api_key = apikey

#create header and footer. initalize body. manually enter in one sample question and answer. 
sample_question = "Question?"
sample_response = "Answer from the above text."
header = "Convert the text above into prompt-response pairs of the form:\n\nUser: " + sample_question + "\n\nChatbot: " + sample_response + "\n\n\""
body = ""
footer = "\""
output = []

#determine max characters for the chunk prompt
max_prompt_tokens = 400
max_body_chars = max_prompt_tokens*3.5 - len(header + footer)
max_response_tokens = 400

# open text file, read lines, remove all lines with just \n. save as var list text
with open('weaknesses.txt') as f:
    contents = f.readlines()
    for line in contents:
        if len(body+line) <= max_body_chars:
            body = body + line
        else:
            #query openai
            prompt = header + body + footer
            response = openai.Completion.create(
                model= "text-davinci-003",
                prompt= prompt,
                max_tokens = max_response_tokens)
            print(response)
            body = ""

            

            






