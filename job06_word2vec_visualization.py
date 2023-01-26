import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl

font_path ='./malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name )

embedding_model = Word2Vec.load('./models/word2vec_audio_clip_inform.model') # 학습된 모델 안에 있는 단어를 보여줌
key_word = '우연'
sim_words = embedding_model.wv.most_similar(key_word, topn=10)   # topn=10 10개 단어만/ 여름이라는 단어와 비슷한 단어가 있는지
print(sim_words)     # most_similar 의미공간 사이에 비슷한 위치에 있는 단어 출력

vectors = []
labels = []

for label, _ in sim_words:
    labels.append(label)
    vectors.append(embedding_model.wv[label])
print(vectors[0])
print(len(vectors[0]))

df_vector = pd.DataFrame(vectors)
print(df_vector)

tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500)
new_value = tsne_model.fit_transform(df_vector)
df_xy = pd.DataFrame({'words':labels, 'x':new_value[:, 0], 'y':new_value[:, 1]})
df_xy.loc[len(df_xy)] = (key_word, 0, 0)    #
print(df_xy)

plt.figure(figsize=(8, 8))
plt.scatter(0, 0, s=500, marker='*')
plt.scatter(df_xy['x'], df_xy['y'])

for i in range(len(df_xy)):
    a = df_xy.loc[[i, 10]]
    plt.plot(a.x, a.y, '-D', linewidth=1)
    plt.annotate(df_xy.words[i], xytext=(1, 1), xy=(df_xy.x[i], df_xy.y[i]),
                 textcoords='offset points', ha='right', va='bottom')

plt.show()