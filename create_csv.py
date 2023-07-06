import os
from bs4 import BeautifulSoup
import pandas as pd
import time
dir_name = os.path.dirname(__file__)
file_list = os.listdir(dir_name+'pt/')
file_list = sorted([f for f in file_list if '.htm' in f])
verses_all = pd.DataFrame()
for f in file_list:
    with open(dir_name+'pt/'+f, 'rb') as fp:
        soup = BeautifulSoup(fp, 'html5lib', from_encoding='WINDOWS-1255')
    target = soup.find_all('b')
    b_list = []
    for text in target:
        b_list.append(text.text)
    num_list = [x for x in b_list if x.isdigit()]
    num_list = [int(x) for x in num_list]
    num_verses = max(num_list)
    verses = {
        'file': [],
        'verse': []
    }
    for v in range(num_verses):
        verses['file'].append(f)
        verses['verse'].append(v+1)
    verses = pd.DataFrame(verses)
    verses_all = verses_all.append(verses)
verses_all.to_csv(dir_name+'verses_directory.csv',index=False)
