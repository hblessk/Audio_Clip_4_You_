import pandas as pd
from konlpy.tag import Okt      # pip install konlpy
import re

df = pd.read_csv('./crawling_data/audio_clip_1_2470.csv')
df.info()
print(df.head())

df_stopwords = pd.read_csv('./stopwords.csv', index_col=0)
# stopwords = list(df_stopwords['stopword'])
# stopwords = stopwords + ['최대', '맞춰']     # 추천할때 필요없는 불용어 제거
okt = Okt()
df['clean_informs'] = None
count = 0

for idx, inform in enumerate(df.informs):
    count += 1
    if count % 10 == 0:     # 10개 마다 점찍기
        print('.', end='')
    if count % 1000 == 0:   # 100개 점(10*100) 찍히면 줄바꿈
        print()
    inform = re.sub('[^가-힣 ]', ' ', inform)
    df.loc[idx, 'clean_informs'] = inform
    token = okt.pos(inform, stem=True)     # pos == 형태소와 품사를 묶어서 줌/ stem=True 원형
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_token = df_token[(df_token['class']=='Noun') |
                       (df_token['class']=='Verb') |
                        (df_token['class'] == 'Adjective')] # 명사, 동사, 형용사만 남기기
    print(df_token.head(30))

    # 불용어 제거
    words = []
    for word in df_token.word:
        if len(word) > 1:
            if word not in list(df_stopwords.stopword):
                words.append(word)
    cleaned_sentence = ' '.join(words)
    df.loc[idx, 'clean_informs'] = cleaned_sentence     # clean_informs 컬럼에 넣기
print(df.head(30))
df.dropna(inplace=True)
df.to_csv('./crawling_data/cleaned_informs.csv', index=False)