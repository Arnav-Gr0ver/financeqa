import pandas as pd
import requests
import json
import time
import os

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")
SAVE_PATH = "data/benchmark_answers.csv"

data = pd.read_csv('data/test.csv')
data = data[data["question_type"] == "assumption"].reset_index(drop=True)

def run_benchmark():
  responses = pd.DataFrame(columns=["question", "answer", "response", "time"])

  for index, row in data.iloc[2:4].iterrows():
    start_time = time.time()
    context = row["context"]
    question = row["question"]
      
    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",
      headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
      },
      data=json.dumps({
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
          { "role": "system",
            "content": "You are a helpful assistant. Provide concise answers."
          },
          {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:{question}\n \n Provide a concise answer."
          }
        ],
        
      })
    )
    end_time = time.time()
    output = response.json()

    entry = pd.DataFrame([{
        "question": row["question"], 
        "answer": row["answer"], 
        "response": output['choices'][0]['message']['content'], 
        "time": round(end_time - start_time, 3)
    }])

    responses = pd.concat([responses, entry], ignore_index=True)

  return responses

if __name__ == "__main__":
  responses = run_benchmark()
  responses.to_csv(SAVE_PATH)