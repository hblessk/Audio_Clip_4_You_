import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc
from PIL import Image
import matplotlib as mpl


font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)

df = pd.read_csv('./crawling_data/cleaned_informs.csv')
words = df[df['titles']=='어린 왕자 (GOT7 진영 낭독)']['clean_informs']
print(words.iloc[0])
words = words.iloc[0].split()
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(background_color='white', max_words=2000,
                          font_path=font_path).generate_from_frequencies(worddict)
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img)
plt.axis('off')

words = df[df['titles']=='82년생 김지영']['clean_informs']
words = words.iloc[0].split()
worddict = collections.Counter(words)
worddict = dict(worddict)
wordcloud_img = WordCloud(background_color='white', max_words=2000,
                          font_path=font_path).generate_from_frequencies(worddict)
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img)
plt.axis('off')
plt.show()






















