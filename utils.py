# %%
import pandas as pd
from typing import Union
from datetime import datetime


def getTime(slice_='second', char='-'):
	r"""
	인자 설명
	slice_ : 어디까지 표현할 것인지(day, hour, minute, second, all)
		(기본(미 설정시) : second)
	char : 구분 문자 설정, 사용불가 문자 :(\ / : * ? " < > |)
		(기본(미 설정시) : -)
	"""
	if char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
		raise ValueError("char must not be in ['\\', '/', ':', '*', '?', '\"', '<', '>', '|']")
	time = str(datetime.now())
	if slice_ == 'day':
		time = time[:time.index(' ')]
	elif slice_ == 'hour':
		time = time[:time.index(':')]
	elif slice_ == 'minute':
		index_ = time.index(':')
		index_ += time[index_+1:].index(':') + 1
		time = time[:index_]
	elif slice_ == 'second':
		time = time[:time.index('.')]
	elif slice_ == 'all':
		pass
	else :
		raise ValueError("slice_ must be in ['day', 'hour', 'minute', 'second', 'all']")
	time = time.replace(':', '-')
	if char != '-':
		time = time.replace('-', char)
	return time

files = ["result"]

def xl2csv_helper(file : str) -> str:
    if '.' in file and './' not in file:
        file = file.split('.')[-2]

    elif '.' in file and './' in file:
        file = '.' + file.split('.')[-2]

    elif '.' in file and '../' in file:
        file = '..' + file.split('.')[-2]

    # xlsx 파일 읽기
    df = pd.read_excel(f'{file}.xlsx')

    # CSV 파일로 저장
    result_csv_file = f'{file} {getTime()}.csv'
    df.to_csv(result_csv_file, index=False)

    return result_csv_file

def xl2csv(files : Union[list, str]) -> str:
    if isinstance(files, list):
        L = []

        for file in files:
            L.append(xl2csv_helper(file))

        return str("└{f}\n" if i + 1 >= len(L) else "├{f}\n" for i, f in enumerate(L))

    elif isinstance(files, str):
        return xl2csv_helper(files)


if __name__ == "__main__":
    print(getTime())
    print(xl2csv(files))
# %%
