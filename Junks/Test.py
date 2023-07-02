# %%
import openai


# 개인 api key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

ft_model = 'curie:ft-personal-2023-06-11-18-10-30'
# %%
"""Prompt 작성"""
sample_prompt = '''개인 지병에 의한 병사이며2019.07.22. 월요일 오전 11시 30분경 설비 보온재 시공 근로자 OOO씨가 106동 지하1층 주차장에서이동식 틀비계를 끌어안고 있는 것을 동료 근로자 OOO씨가 발견하고 “왜그래? 왜그래?”라고 물으니OOO씨가 “기운이 없어”라고 답하며 주저 앉으려고 하자 조한월씨가 부축하여 바닥에 누인 다음119로 부천 카톨릭 성모병원으로 이송하였고부천 카톨릭 성모병원에서 뇌출혈 진단을 받고 2019.07.22 당일 수술 후 중환자실에 입원중2019.08.04 오전 07시 36분에 병사한 것임.날씨 맑음 기온 31℃ 습도 74%'''
# 정답 : 기타
# %%
"""답만 보는 코드"""
res = openai.Completion.create(model=ft_model, prompt=sample_prompt, max_tokens=30, temperature=0.2)
res['choices'][0]['text'].lstrip(' ').split(' ')[0]
# %%
"""JSON"""
res
# %%
