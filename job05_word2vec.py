import pandas as pd
from gensim.models import Word2Vec

inform_word = pd.read_csv('./crawling_data/cleaned_informs.csv')
inform_word.info()

one_sentence_informs = list(inform_word['clean_informs'])        #컬럼명 #정제한 정보로 이렇게 만들겠다.
cleaned_tokens = []
for sentence in one_sentence_informs:
    token = sentence.split()
    cleaned_tokens.append(token)

embedding_model = Word2Vec(cleaned_tokens, vector_size=100,
                           window=4, min_count=7,
                           workers=4, epochs=100, sg=1)
embedding_model.save('./models/word2vec_audio_clip_inform.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))

# http://w.elnn.kr/search/

#유사한 단어들이 비슷한 리뷰들을 찾아서, 그 영화들을 추천해준다.
#워드트백 > 단어를 백터화해주는 모델. 뉴스 카테고리 분류할 때, 맨 첫번째 레이어로 임베딩 레이어 줬었는데,

#춥다의 의미가 클수록 큰값, 작을수록 작은값.
#말뭉치 안에있는 단어의 의미에 대한 차원을 만들고, 각 단어들의 좌표를 만드는 벡터..? 그래서 백터의 사이즈를 100으로 줄이겠다
#window=4개는, 4개 단어로 잘라서 학습하겠다~. 컴브레이에서 쓰는 커널하고 비슷.
#workers는 cpu를 몇개쓸거냐. 논리프로세서가 몇개냐. 작업관리자에서 볼 수 있다. 다 안주고 반만줘도 됨. 현재 컴퓨터에는 8개.
#에폭스는 반복학습.
#최소 스무번은 나와야한다. min_count. 데이터가 작으면 더 작아도 됨.
#방향과 크기가 있는게 벡터
# sg는 알고리즘 지칭. 백터가 하는 알고리즘을???? (내일 다시 시작)
#단어가 많기 때문에 100에폭 학습해야 한다.
