from gensim.models import word2vec
from janome.tokenizer import Tokenizer
import json, random

# https://qiita.com/ssabcire/items/7244b2d434752f30ba0e

model_file = 'sabal_w2v_model.model'
markov_file = 'sabal_markov.json'

def tokenize(s):
    t = Tokenizer()
    tokens = t.tokenize(s)
    for token in tokens:
        base_form = token.base_form
        pos = token.part_of_speech
        pos = pos.split(',')[0]
        if pos in ['名詞','動詞','形容詞']:
            return base_form
    return '@'

def load_w2v(word):
    model = word2vec.Word2Vec.load(model_file)
    try:
        #similar_words = model.most_similar(positive=[word])
        similar_words = model.wv.most_similar(positive=[word])
        #print(similar_words)
        return random.choice([w[0] for w in similar_words])# ,weights=[10,9,8,7,6,5,4,3,2,1]
    except:
        #print('26-error!')
        return word

def make_sentence(reply):
    markov_dic = json.load(open(markov_file))
    if not reply == '':
        ret = []
        if not '@' in markov_dic:
            return 'no dict'
        # TODO ここを質問する。
        top = markov_dic['@']
        word1 = reply
        #print('36 '+word1)
        try:
            word2 = word_choice(top[word1])
        except:
            word1 = word_choice(top)
            word2 = word_choice(top[word1])
        #print('38 '+word2)
        if(word2 == '。'):
            word2 = '、'
        ret.append(word1)
        ret.append(word2)
        while True:
            word3 = word_choice(markov_dic[word1][word2])
            #print('54 '+word3)
            ret.append(word3)
            if word3 == '。':
                break
            if len(ret) >= 20:
                ret.append('。')
                break
            word1, word2 = word2, word3
        ret = [s for s in ret if not '\r' in s]
        #print(ret)
        return ''.join(ret)
    else:
        return ''

def word_choice(sel):
    keys = sel.keys()
    ran = random.choice(list(keys))
    return ran


def main():
    while True:
        s = input('you  :')
        #print('63 '+s)
        if s == 'quit':
            break
            exit(0)
        word = tokenize(s)
        #print('68 '+word)
        if not word == '@':
            reply = load_w2v(word)
        else:
            reply = ' '
        #print('73 '+reply)
        sentence = make_sentence(reply)
        print('サーバル:' + sentence.rstrip("。") + '！')

if __name__ == '__main__':
    main()