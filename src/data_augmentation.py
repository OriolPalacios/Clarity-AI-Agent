from typing import Tuple
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import json
import os

def load_env_vars() -> str:
  load_dotenv()
  API_KEY = os.getenv("API_KEY")
  return API_KEY

def load_client(API_KEY) -> None:
  global CLIENT
  CLIENT = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
  )

def load_dataset() -> Tuple[str, str]:
  CSV_DATA = '../data/Dataset-v1.csv'
  DF = pd.read_csv(CSV_DATA)
  MAX_ROW = DF.shape[0]
  return DF, MAX_ROW

def get_row(DF: pd.DataFrame, index: int):
  try:
    row = DF.iloc[index]
    return {
      "Question": row["Question"],
      "CoT": row["CoT"],
      "Response": row["Response"]
    }
  except IndexError:
    raise Exception('Index not found')

def rephrase_question_cot(Question:str, CoT:str) -> Tuple[str,str]:
  completion = CLIENT.chat.completions.create(
    model="qwen/qwq-32b:free",
    messages=[
      {
        "role": "system",
        "content": """Paraphrase the following Question and Chain of Thought (CoT) while preserving their meaning.                   
                      You MUST return ONLY valid JSON in the exact format shown below:
                      {
                        "Question": "your rephrased question here",
                        "CoT": "your rephrased chain of thought here"
                      }
                      Do not include explanations, markdown formatting, or any text outside the JSON object."""
      },
      {
        "role": "user",
        "content": f"Question: {Question}\n\nCoT: {CoT}"
      }
    ]
  )
  augmented_data = completion.choices[0].message.content
  try:
    cleaned_data = augmented_data.strip('`').replace('```json', '').replace('```', '')
    parsed_augmented_data = json.loads(cleaned_data)
  except json.JSONDecodeError as e:
    raise Exception(f'Not possible to parse: {augmented_data}. Error: {str(e)}')
  question = parsed_augmented_data['Question']
  cot = parsed_augmented_data['CoT']
  return question, cot

def perform_data_augmentation(DF:pd.DataFrame, MAX_ROW:int) -> None:
  for index in range(0, MAX_ROW):
    row = get_row(DF, index)
    if row:
      try:
        new_question, new_CoT = rephrase_question_cot(row["Question"], row["CoT"])
        new_row = pd.DataFrame({'Question': [new_question], 'CoT': [new_CoT], 'Response': [row['Response']]})
        DF = pd.concat([DF, new_row], ignore_index=True)
        print(f'The row {index} has been correctly processed and appended to the dataframe')
      except:
        DF.to_csv(f'../data/Dataset-v1-augmented-log-{index}')
        return None
  DF.to_csv(f'../data/Dataset-v1-augmented.csv')
  return 'The dataframe has been saved as a csv in folder /data/'


def run():
  API_KEY = load_env_vars()
  load_client(API_KEY)
  DF, MAX_ROW = load_dataset()
  perform_data_augmentation(DF, MAX_ROW)


if __name__ == '__main__':
  run()