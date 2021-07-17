"""
サーバルの発話データ

参考
https://qiita.com/mapps/items/c0d3f1b73bc9ef398790

https://qiita.com/shge/items/fbfce6b54d2e0cc1b382
"""

from janome.tokenizer import Tokenizer
import markovify
import pandas as pd

csv_data = pd.read_csv('kemohure.csv')
csv_data = csv_data.dropna()
#print(csv_data.head(10))

# print(csv_data[csv_data['charactor'] == 'サーバル'])
sabal_csv_data = csv_data[csv_data['charactor'] == 'サーバル'] # かばん # カバ
sabal_csv_data = sabal_csv_data.drop('charactor', axis=1)

print(sabal_csv_data)
# print(sabal_csv_data.values.tolist())

sabal_list_data = sabal_csv_data.values.tolist()

print(sabal_list_data)

text_file = open("../hatsugen.txt", "wt", encoding='UTF-8')
for word in sabal_list_data:
    text_file.write(word[0]+'\n')

text_file.close()