from gensim.models import word2vec

def save_word2vec_model(load_path, save_path):
    # 分かち書きしたテキストデータからコーパスを作成
    sentences = word2vec.LineSentence(load_path)

    # ベクトル化
    # TODO データ量によってパラメータをカエルべき？
    model = word2vec.Word2Vec(
        sentences,
        sg=1,
        vector_size=100,
        min_count=2,
        window=30,
        hs=1
    )

    model.save(save_path)
    # 作成したモデルをファイルに保存


if __name__ == "__main__":
    load_path = 'wakati.txt'
    save_model_path = 'sabal_w2v_model.model'

    save_word2vec_model(load_path, save_model_path)

# test2.pyを実行