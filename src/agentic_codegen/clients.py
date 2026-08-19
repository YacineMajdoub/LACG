import os
from dotenv import load_dotenv
from openai import OpenAI
from together import Together

load_dotenv()

tg_client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

def call_llm_open_router(question: str) -> str:
    response = openrouter_client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[
            {"role": "user", "content": question}
        ],
    )
    return response.choices[0].message.content

def call_llm_openai (question : str):
    response = openai_client.responses.create(
        model="gpt-5",
        input=question,
        reasoning={ "effort": "low" },
        text={ "verbosity": "low" },
    )

    return response.output_text

def call_llm_together(question: str) -> str:
    response = tg_client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


def call_llm(question: str)-> str:
    return call_llm_openai(question)
