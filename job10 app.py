import sys
from PyQt5.QtWidgets import *       # pip install pyqt5
from PyQt5 import uic       # pip install pyqt5-tools
from PyQt5.QtCore import QStringListModel   # 자동완성 기능
import pandas as pd
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import linear_kernel
import re
from konlpy.tag import Okt


form_window = uic.loadUiType('./novel_1.ui')[0]      # (저장 경로)

class Exam(QWidget, form_window):
    def __init__(self):         # self로 받아서 각각 적용되게 함
        super().__init__()
        self.setupUi(self)

        self.tfidf_matrix = mmread('./models/tfidf_audio_clip_inform_new.mtx').tocsr()
        with open('./models/tfidf_new.pickle', 'rb')as f:
            self.tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_audio_clip_inform_new.model')

        self.df_informs = pd.read_csv('./crawling_data_2/cleaned_informs_new.csv')
        # self.titles = self.df_informs['titles']
        # self.titles = sorted(self.titles)
        self.titles = list(self.df_informs['titles'])
        self.titles.sort() # 제목 순서 정렬
        for title in self.titles:
            self.combo_box.addItem(title)

        # 자동완성 기능
        model = QStringListModel()
        model.setStringList(self.titles)    # 리스트로 들어가야함
        completer = QCompleter()
        completer.setModel(model)
        self.line_edit.setCompleter(completer)

        self.combo_box.currentIndexChanged.connect(self.combobox_slot)   # 인덱스가 바뀌면 적용됨
        self.btn_recommend.clicked.connect(self.btn_slot)

        # 반복되서 함수로 만들어줌
    def recommendation_by_audio_clip_title(self, title):
        Audio_clip_idx = self.df_informs[self.df_informs['titles'] == title].index[0]
        cosin_sim = linear_kernel(self.tfidf_matrix[Audio_clip_idx], self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)

        result = [None] * 10
        for i in range(1, 11):

            # recommendation = list(recommendation)
            result[i-1] = '<a href="{}">{}</a><br>'.format(recommendation.iloc[i, 1], recommendation.iloc[i, 0])
            # print('rec 0', result[i])

        result_str = '\n'.join(list(result))
        # print('recommendation', recommendation)
        self.lbl_recommend.setText(result_str)
        self.lbl_recommend.setOpenExternalLinks(True)


    def recommendation_by_key_word(self, key_word):
        sim_word = self.embedding_model.wv.most_similar(key_word, topn=10)
        words = [key_word]  # 인위적으로 반복 늘리기(리뷰에서 나온 단어를 가지고 해야하는데 수가 적을 수 있어서)
        for word, _ in sim_word:
            words.append(word)
        print(words)
        sentence = []
        count = 11  # 유사한 문장으로 만들기
        for word in words:
            sentence = sentence + [word] * count
            count -= 1  # count 에서 1을 뺀 값 /
        sentence = ' '.join(sentence)
        print(sentence)
        sentence_vec = self.tfidf.transform([sentence])
        cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        recommendation = '\n'.join(list(recommendation[:10]))
        self.lbl_recommend.setText(recommendation)


    def recommendation_by_sentence(self, key_word):
        sentence = key_word
        clean_informs = re.sub('[^가-힣]', ' ', key_word)
        okt = Okt()
        token = okt.pos(clean_informs, stem=True)
        df_token = pd.DataFrame(token, columns=['word', 'class'])
        df_token = df_token[(df_token['class']=='Noun') |
                            (df_token['class']=='Verb') |
                            (df_token['class']=='Adjective')]
        words = []
        for word in df_token.word:
            if 1 < len(word):
                words.append(word)
        cleaned_sentence = ' '.join(words)
        print(cleaned_sentence)
        sentence_vec = self.tfidf.transform([cleaned_sentence])
        cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        recommendation = '\n'.join(list(recommendation[:10]))
        self.lbl_recommend.setText(recommendation)



        # 라인테스트에서 제목을 입력해서 추천 버튼 누를때
    def btn_slot(self):
        key_word = self.line_edit.text()   # 제목 읽어오기
        if key_word in self.titles: # 키워드가 영화 제목에 있으면 추천
            self.recommendation_by_audio_clip_title(key_word)

            # 리스트 안에 키워드가 있으면 키워드 기반으로 제목 추천
        elif key_word in list(self.embedding_model.wv.index_to_key):    # 임베딩모델에 키워드 단어가 있으면 유사단어로 문장 만들어서 추천
            self.recommendation_by_key_word(key_word)

            # embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
            # sim_word = embedding_model.wv.most_similar(key_word, topn=10)
            # words = [key_word]      # 인위적으로 반복 늘리기(리뷰에서 나온 단어를 가지고 해야하는데 수가 적을 수 있어서)
            # for word, _ in sim_word:
            #     words.append(word)
            # print(words)
            # sentence = []
            # count = 11      # 유사한 문장으로 만들기
            # for word in words:
            #     sentence = sentence + [word] * count
            #     count -= 1      # count 에서 1을 뺀 값 /
            # sentence = ' '.join(sentence)
            # print(sentence)
            # sentence_vec = self.tfidf.transform([sentence])
            # cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
            # recommendation = self.getRecommendation(cosin_sim)
            # recommendation = self.getRecommendation(cosin_sim)
            # recommendation = '\n'.join(list(recommendation[:10]))
            # self.lbl_recommend.setText(recommendation)
        else:
            self.recommendation_by_sentence(key_word)


        # 콤보박스에서 제목/키워드로 찾았을 때 추천
    def combobox_slot(self):
        title = self.combo_box.currentText()    # 현재 텍스트 읽어오기
        # movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        # cosin_sim = linear_kernel(self.tfidf_matrix[movie_idx], self.tfidf_matrix)
        # recommendation = self.getRecommendation(cosin_sim)
        # recommendation = '\n'.join(list(recommendation[1:]))
        # print('recommendation', recommendation)
        # self.lbl_recommend.setText(recommendation)
        self.recommendation_by_audio_clip_title(title)

    def getRecommendation(self, cosin_sim):
        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        Audio_clip_idx = [i[0] for i in simScore]  # 영화의 인덱스 뽑았다
        recAudioClipList = self.df_informs.iloc[Audio_clip_idx, [0, 3]]  # 영화 11개, 0 타이틀
        print(recAudioClipList)
        return recAudioClipList


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()     #입력하라
    mainWindow.show()       #실행하라
    sys.exit(app.exec_())
