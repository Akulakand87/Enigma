import requests, json
model = 'llama2:7b'
context = [] 

def generate(prompt, context, top_k, top_p, temp):
    r = requests.post('http://localhost:11434/api/generate',#set local host ccordingly
                     json={
                         'model': model,
                         'prompt': prompt,
                         'context': context,
                         'options':{
                             'top_k': top_k,
                             'temperature':top_p,
                             'top_p': temp
                         }
                     },
                     stream=False)
    r.raise_for_status()
    response = ""  
    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        if 'error' in body:
            raise Exception(body['error'])
        response += response_part
        if body.get('done', False):
            context = body.get('context', [])
            return response, context

def chat(input, chat_history, top_k, top_p, temp):
    chat_history = chat_history or []
    global context
    output, context = generate(input, context, top_k, top_p, temp)
    chat_history.append((input, output))
    return chat_history, chat_history

user_query = input("What do you want to know? ")
chat_history, _ = chat(user_query, [], 5, 0.5, 0.5)
print(chat_history[-1][1])







query = query
speak('Searching...')
chat_history, _ = chat(query, [], 5, 0.5, 0.5)
print(chat_history[-1][1])
speak(chat_history[-1][1])