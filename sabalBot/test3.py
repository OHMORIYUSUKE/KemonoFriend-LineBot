from gensim.models import word2vec

# load_model_path = 'sabal_w2v_model.model'
# model = word2vec.Word2Vec.load(load_model_path)
# ##
# results = model.wv.most_similar(positive=['カバン'])
# print(results)



model_file = 'sabal_w2v_model.model'

model = word2vec.Word2Vec.load(model_file)
#調べたいワード
words = ['バス','パーク','PPP','友達']
for word in words:
    similar_words = model.wv.most_similar(positive=[word])
    print(word,':',[w[0] for w in similar_words])