# %%
# ! pip install openai==0.25.0/

# %% Configure ########################################################################## 처음
import utils

import pandas as pd
import openai
import os

OPENAI_API_KEY = "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"

# %% Setting ############################################################################ 학습 준비
data_dir = "C:/Users/bhyoo/Desktop/Causual Analysis/Preprocessed/"
target_file = data_dir + "prepocessed.xlsx" 
prepocess_dir = "prepocess/"
# c_default = " 기타"
print(utils.xl2csv(target_file))
csv_file = target_file.split('.')[-2] + ".csv"

# %%
df = pd.read_csv(csv_file) [: 1_000] 
df.rename(columns = {"사고경위" : "prompt", "재해유형" : "completion"}, inplace = True)
df.head()

n_file = prepocess_dir + (csv_file.split('/')[-1]).split('.')[0]
n_json = f"{n_file}.jsonl"

df.to_json(n_json, orient='records', lines=True)

! openai tools fine_tunes.prepare_data -f "{n_json}" -q

# %% create ############################################################################## 학습 시작
n_t_json = f"{n_file}_prepared_train.jsonl"
n_v_json = f"{n_file}_prepared_valid.jsonl"

! openai -k "{OPENAI_API_KEY}" api fine_tunes.create -t "{n_t_json}" -v "{n_v_json}"
#  --compute_classification_metrics --classification_positive_class $c_default -m ada

# %% list ################################################################################ list 보기
"""
! openai -k $OPENAI_API_KEY api fine_tunes.list

"""
# %% cancel ############################################################################## list 지우기
"""
del_id = "9k5lZIbqVkGjpi89slGfyWOZ"

del_id = f"ft-{del_id}"
! openai -k $OPENAI_API_KEY api fine_tunes.cancel -i $del_id
"""
# %% follow ############################################################################## 이어서 학습
i_tmp = "8azYfmagmBJyg6j5z0sfkyYP"

n_it = f"ft-{i_tmp}"
! openai -k "{OPENAI_API_KEY}" api fine_tunes.follow -i "{n_it}"

"""
# %% ######################################################################################### 테스트
t_completion = "거푸집 동바리."

n_model = f"ada:{n_it}"
!openai  -k $OPENAI_API_KEY api completions.create -m n_model -p $t_completion
"""
# %% ########################################################################################  
openai.api_key = "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"

n_v_json = f"{n_file}_prepared_valid.jsonl"
test = pd.read_json(n_v_json, lines=True)
test.head()
# %%
ft_model = 'curie:ft-personal-2023-05-31-08-28-50'

t_idx = 0

res = openai.Completion.create(model=ft_model, prompt=test['prompt'][t_idx] + '\n\n###\n\n', max_tokens=1, temperature=0)
res['choices'][t_idx]['text']

res = openai.Completion.create(model=ft_model, prompt=test['prompt'][t_idx] + '\n\n###\n\n', max_tokens=1, temperature=0, logprobs=2)
res['choices'][t_idx]['logprobs']['top_logprobs'][0]
# %%
help(openai)
# %%
openai.api_key = "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"

ft_model = 'curie:ft-personal-2023-05-31-08-28-50'

t_idx = 0

sample = """개인 지병에 의한 병사이며2019.07.22. 월요일 오전 11시 30분경 설비 보온재 시공 근로자 OOO씨가 106동 지하1층 주차장에서이동식 틀비계를 끌어안고 있는 것을 동료 근로자 OOO씨가 발견하고 “왜그래? 왜그래?”라고 물으니OOO씨가 “기운이 없어”라고 답하며 주저 앉으려고 하자 조한월씨가 부축하여 바닥에 누인 다음119로 부천 카톨릭 성모병원으로 이송하였고부천 카톨릭 성모병원에서 뇌출혈 진단을 받고 2019.07.22 당일 수술 후 중환자실에 입원중2019.08.04 오전 07시 36분에 병사한 것임.날씨 맑음 기온 31℃ 습도 74%"""

res = openai.Completion.create(model=ft_model, prompt=sample + "\n\n###\n\n", max_tokens=1, temperature=0)
res['choices'][t_idx]['text']
# %%
res = openai.Completion.create(model=ft_model, prompt=sample + "\n\n###\n\n", max_tokens=1, temperature=0, logprobs=2)
res['choices'][t_idx]['logprobs']['top_logprobs'][0]
# %%
r_n_file = f"{n_file}_result.csv"
!openai  -k "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" api fine_tunes.results -i ft-UkodFZ72SoonHGvhYzvuktLr > $r_n_file

results = pd.read_csv(r_n_file)
results[results['training_token_accuracy'].notnull()].tail(1)
# %%
results[results['training_token_accuracy'].notnull()]['training_token_accuracy'].plot()
# %%
results[results['validation_token_accuracy'].notnull()]['validation_token_accuracy'].plot()

# %%
