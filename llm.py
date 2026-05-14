import requests
import traceback
from apikey import OPENAI_API_KEY

LLAMA_API_URL = "https://api.openai.com/v1/chat/completions"
 # Replace with your actual endpoint

def talkToLLM(context, max_tokens=250, temperature=0.7, top_p=1.0, repetition_penalty=1.0, top_k=50, model="gpt-3.5-turbo"):
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {

        "model": model,
        "messages": [
            {"role": "user", "content": context}
        ],
        ##"prompt": context,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        ##"repetition_penalty": repetition_penalty,
        ##"top_k": top_k,
    }

    try:
    
        ## response = requests.post(LLAMA_API_URL, json=payload)
        response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()

        ##return response_json.get("response", "")
        return response_json["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print("RequestException occurred:", e)
        if e.response is not None:
            print("Response content:", e.response.text)
        traceback.print_exc()
        return {"error": "Failed to generate response", "detail": str(e)}
