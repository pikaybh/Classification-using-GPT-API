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
    def __init__(self, _API_key : str, model_name : str, class_list : list):
        """_API_key : openai api key, model_name : model, class_list : list"""
        self.api_key = _API_key
        self.model = model_name
        self.cls_list = class_list
        self.num_cls = len(class_list)

        openai.api_key = self.api_key


    def run(self, prompt : str, max_tokens=50, temperature=0.2) -> tuple:
        res = openai.Completion.create(model=self.model, prompt=prompt, max_tokens=max_tokens, temperature=temperature, logprobs=self.num_cls)
        ob = res['choices'][0]['text'].lstrip(' ').split(' ')[0]
        for idx, cls in enumerate(self.cls_list):
            if cls in ob or cls.startswith(ob):
                ob = cls
                break
            elif idx+1 >= len(self.cls_list):
                print(f"[error] {ob}")

        probs = .0
        for v in dict(res['choices'][0]['logprobs']['top_logprobs'][0]).values():
            tmp = exp(v)
            probs = tmp if probs <= tmp else probs

        return ob, probs


def sample_loader(df : pd.DataFrame, num : int) -> tuple:
    sample_data = df.iloc[num]
    sample_prompt = sample_data['prompt'] + "\n\n###\n\n"
    sample_completion = sample_data['completion']

    return sample_prompt, sample_completion