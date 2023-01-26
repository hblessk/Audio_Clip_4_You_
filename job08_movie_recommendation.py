# 유사한 문장을 가진 영화 추천

import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1]))   # 인덱스를 먼저 줘서 제목 순서를 주고, 첫번째 영화에 0, 그다음부터 1,2.. / cosin_sim[-1] 0을 줘도 되는데 앞에 다른 게 붙을 수가 있어서 -1로 해서 인덱싱을 뽑아줌
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)    #enumerate 없이 sorted하면 인덱스 없이 리뷰만 보여줘서 알길이 없어서 인덱스 붙인 뒤에 정렬 /reverse=True 내림차순 정렬(1에 가까운 순서대로)
    simScore = simScore[:11]    # 11개 하는 이유는 첫번째 나오는게 그영화 이기 때문에 그영화를 빼고 10개 보려고
    audiobook_idx = [i[0] for i in simScore]    # 영화의 인덱스 뽑았다
    recAudioClipList = df_informs.iloc[audiobook_idx, 0]    # 영화 11개, 0 타이틀
    return recAudioClipList

df_informs = pd.read_csv('./crawling_data/cleaned_informs.csv')
tfidf_matrix = mmread('./models/tfidf_audio_clip_inform.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    tfidf = pickle.load(f)


# # 오디오북 제목 이용
# audiobook_idx = df_informs[df_informs['titles']=='오리엔트 특급 살인'].index[0]     # 겨울왕국과 비슷한 영화를 추천
# print(audiobook_idx)
# cosin_sim = linear_kernel(tfidf_matrix[audiobook_idx], tfidf_matrix)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation[1:11]) # 0번은 그영화라서 그거빼고 1번부터 10번까지
# # linear_kernel 코싸인 값이 1에 가까워지면 (0도) 같은 방향/ -1에 가까워지면 (180도) 반대방향/ 0에 가까워지면 (90도) = 서로 연관이 없다



# key word 키워드 이용
embedding_model = Word2Vec.load('./models/word2vec_audio_clip_inform.model')
key_word = '크리스마스'
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
words = [key_word]      # 인위적으로 반복 늘리기(리뷰에서 나온 단어를 가지고 해야하는데 수가 적을 수 있어서)
for word, _ in sim_word:
    words.append(word)
print(words)
sentence = []
count = 11    # 유사한 문장으로 만들기
for word in words:
    sentence = sentence + [word] * count
    count -= 1  # count 에서 1을 뺀 값 /
sentence = ' '.join(sentence)
print(sentence)
sentence_vec = tfidf.transform([sentence])
cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
recommendation = getRecommendation(cosin_sim)
print(recommendation)   # 가장 유사한게 자기 자신이 아님



# # 문장으로 추천
# sentence = '살인마한테 쫓기는 스릴러 넘치는 책'    # 이 문장도 전처리 해야함
# inform = re.sub('[^가-힣]', ' ', sentence)
# okt = Okt()
# token = okt.pos(inform, stem=True)
# df_token = pd.DataFrame(token, columns=['word', 'class'])
# df_token = df_token[(df_token['class']=='Noun') |
#                     (df_token['class']=='Verb') |
#                     (df_token['class']=='Adjective')]
# words = []
# for word in df_token.word:
#     if 1 < len(word):
#         words.append(word)
# cleaned_sentence = ' '.join(words)
# print(cleaned_sentence)
# sentence_vec = tfidf.transform([cleaned_sentence])
# cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation)
#

