from typing import Tuple
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import json
import os

MODELS = {'gemini-2.0-flash':'google/gemini-2.0-flash-lite-preview-02-05:free','qwen-qwq': 'qwen/qwq-32b:free', 'gemini-2.0-pro':'google/gemini-2.0-pro-exp-02-05:free', 'deepseek': 'deepseek/deepseek-r1-zero:free'}

def load_env_vars() -> str:
  load_dotenv()
  API_KEY = os.getenv("API_KEY")
  return API_KEY

def load_client(API_KEY) -> OpenAI:
  CLIENT = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
  )
  return CLIENT

def load_dataset() -> Tuple[pd.DataFrame, int]:
  CSV_DATA = '../data/Dataset-v1.csv'
  DF = pd.read_csv(CSV_DATA)
  MAX_ROW = DF.shape[0]
  return DF, MAX_ROW

def get_row(DF: pd.DataFrame, index: int) -> dict[str, str]:
  try:
    row = DF.iloc[index]
    return {
      "Question": row["Question"],
      "CoT": row["CoT"],
      "Response": row["Response"]
    }
  except IndexError:
    raise Exception('Index not found')

def rephrase_question_cot(CLIENT: OpenAI, Question:str, CoT:str, model_sig:str) -> Tuple[str,str]:
  completion = CLIENT.chat.completions.create(
    model = model_sig,
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
  augmented_data = completion.choices[0].message.content.replace('```json', '').replace('```', '')
  try:
    cleaned_data = augmented_data
    if (model_sig == 'deepseek/deepseek-r1-zero:free'): 
      cleaned_data = augmented_data.replace('\\boxed{','').replace('}','') + "}"
    elif (model_sig == 'google/gemini-2.0-flash-lite-preview-02-05:free'):
      cleaned_data = cleaned_data + "}" if cleaned_data.endswith('"') else cleaned_data
    parsed_augmented_data = json.loads(cleaned_data)
  except json.JSONDecodeError as e:
    raise Exception(f'Not possible to parse: {augmented_data}. Error: {str(e)}')
  question = parsed_augmented_data['Question']
  cot = parsed_augmented_data['CoT']
  return question, cot

def perform_data_augmentation(CLIENT: OpenAI, DF:pd.DataFrame, MAX_ROW:int) -> None:
  df_per_model = []
  for model_name, model_sig in MODELS.items():
    df_model = pd.DataFrame()
    for index in range(0, MAX_ROW):
      row = get_row(DF, index)
      if row:
        try:
          new_question, new_CoT = rephrase_question_cot(CLIENT, row["Question"], row["CoT"], model_sig)
          new_row = pd.DataFrame({'Question': [new_question], 'CoT': [new_CoT], 'Response': [row['Response']]})
          df_model = pd.concat([df_model, new_row], ignore_index=True)
          print(f'The row {index} has been correctly processed and appended to the dataframe by the model {model_name}')
        except Exception as e:
          print(f'Error processing row {index} with model {model_name}: {str(e)}')
          continue
    df_model.to_csv(f'../data/Dataset-v4-augmented-{model_name}.csv', index=False)
    df_per_model.append(df_model)
  DF = pd.concat([DF, *df_per_model], ignore_index=True)
  DF.to_csv(f'../data/Dataset-v4-augmented.csv', index=False) 
  print(f'The dataframe has been saved as a csv in /data/Dataset-v4-augmented-{model_name}.csv')

def run():
  API_KEY = load_env_vars()
  CLIENT = load_client(API_KEY)
  DF, MAX_ROW = load_dataset()
  perform_data_augmentation(CLIENT, DF, MAX_ROW)


if __name__ == '__main__':
  run()