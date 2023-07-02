import openai
import pandas as pd
from math import exp


"""
class_names = {"기타" : ["기타"],
                "끼임, 깔림" : [],
                "넘어짐" : [],
                "떨어짐" : [],
                "물체" : [],
                "부딪힘" : [],
                "불균형 및 무리한 동작" : [],
                "절단, 베임, 찔림" : []}
"""


class FineTuneModel:
    def __init__(self, _API_key : str, model_name : str):
        """_API_key : openai api key, model_name : model"""
        self.api_key = _API_key
        self.model = model_name

        openai.api_key = self.api_key


    def run(self, prompt : str, max_tokens=50, temperature=0.2, num_class=8) -> tuple:
        res = openai.Completion.create(model=self.model, prompt=prompt, max_tokens=max_tokens, temperature=temperature, logprobs=num_class)
        ob = res['choices'][0]['text'].lstrip(' ').split(' ')[0]
        if "기타" in ob:
            ob = "기타"
        elif "끼임" in ob or "깔림" in ob:
            ob = "끼임, 깔림"
        elif "넘어짐" in ob:
            ob = "넘어짐"
        elif "떨어짐" in ob:
            ob = "떨어짐"
        elif "물체" in ob or "맞음" in ob:
            ob = "물체에 맞음"
        elif "부딪" in ob:
            ob = "부딪힘"
        elif "불균형" in ob or "무리한" in ob:
            ob = "불균형 및 무리한 동작"
        elif "절단" in ob or "베임" in ob or "찔림" in ob:
            ob = "절단, 베임, 찔림"
        else:
            print(f"[error] {ob}")

        probs = top_logprobs = res['choices'][0]['logprobs']['top_logprobs'][0]

        return ob, probs


def sample_loader(df : pd.DataFrame, num : int) -> tuple:
    sample_data = df.iloc[num]
    sample_prompt = sample_data['prompt'] + "\n\n###\n\n"
    sample_completion = sample_data['completion']

    return sample_prompt, sample_completion