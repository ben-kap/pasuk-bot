#!/usr/bin/python3

import os
import pandas as pd
from random import randint
from bs4 import BeautifulSoup
import re
from pathlib import Path
from mastodon import Mastodon

def gem_convert(num_in):
    gem_ones = ['','א','ב','ג','ד','ה','ו','ז','ח','ט']
    gem_tens = ['','י','כ','ל','מ','נ','ס','ע','פ','צ']
    gem_hunds = ['','ק','ר','ש','ת']
    gems = [gem_ones,gem_tens,gem_hunds]
    heb_out = ''
    n = 0
    for dig in range(len(num_in)-1,-1,-1):
        heb_out = heb_out + gems[dig][int(num_in[n])]
        n += 1
    heb_out = heb_out.replace('יה','טו').replace('יו','טז')
    return heb_out

dir_name = os.path.dirname(__file__)
verses_all = pd.read_csv(dir_name+'/verses_directory.csv')
num_verses = verses_all.shape[0]
verse_num = randint(1,num_verses)
file_name = verses_all.at[verse_num,'file']
num_verse = verses_all.at[verse_num,'verse']
# file_name = 'pt08a01.htm'
# num_verse = 1
with open(dir_name+'/pt/'+file_name, 'rb') as fp:
    soup = BeautifulSoup(fp, 'html5lib', from_encoding='WINDOWS-1255')
target = soup.find_all('b')
b_list = []
for text in target:
    b_list.append(text.text)
verse_num = str(num_verse)
pasuk_num = gem_convert(verse_num)
verse_ind = b_list.index(verse_num)
verse = ''
for sib in target[verse_ind].next_siblings:
    verse = verse+str(sib)
verse = target[verse_ind].next_sibling
pasuk_ind = b_list.index(pasuk_num)
pasuk = ''
for sib in target[pasuk_ind].next_siblings:
    pasuk = pasuk+str(sib)
cleaner1 = re.compile('<.*?>')
cleaner2 = re.compile('{.*?}')
verse = re.sub(cleaner1, '', verse)
verse = re.sub(cleaner2, '', verse).strip()
verse = ' '.join(verse.split())
pasuk = re.sub(cleaner1, '', pasuk)
pasuk = re.sub(cleaner2, '', pasuk).strip()
pasuk = ' '.join(pasuk.split())
book_heb = soup.find('span').text
page_title = soup.title.text.split('/')[0].strip().split(' ')
book_eng = ' '.join(page_title[0:-1])
chapter_num = page_title[-1]
perek_num = gem_convert(chapter_num)
title_eng = book_eng + ' ' + chapter_num + ':' + verse_num
title_heb = book_heb + ' ' + perek_num + ':' + pasuk_num

access_token = Path(dir_name+'/access_token.txt').read_text().strip()
mastodon = Mastodon(
    access_token = access_token,
    api_base_url = 'https://kiddush.social/'
)
heb_post = mastodon.status_post(title_heb + '\n\n' + pasuk, visibility='public')
eng_post = mastodon.status_post(title_eng + '\n\n' + verse, in_reply_to_id=heb_post.id, visibility='public')
