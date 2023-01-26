import re
import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# <x_path 원본 모음>
# 0. 제목버튼            //*[@id="content"]/div/section/div/div/div[3]/div/div/div[1]/a/div[2]   => title_button_xpath  # 제목눌러서 상세로 들어가기
#                       //*[@id="content"]/div/section/div/div/div[3]/div/div/div[1]/a/div[2]/div[2] 추천
#                       //*[@id="content"]/div/section/div/div/div[3]/div/div/div[2]/a/div[2]/div[1]
#                       //*[@id="content"]/div/section/div/div/div[3]/div/div/div[3]/a/div[2]/div[2] 요약
# => 0. 링크클릭          //*[@id="content"]/div/section/div/div/div[3]/div/div/div[1]/a

# 1. 상세>제목             //*[@id="content"]/div/section/div[1]/div[2]/h3                          => title_xpath
# 2. 상세>저자             //*[@id="content"]/div/section/div[1]/div[3]/div[1]/span[1]/text()[1]    => author_xpath
# 3. 상세>오디오북 정보     //*[@id="audiobook"]/div[1]/p      #/text()                              => inform_xpath

# url = 'https://audioclip.naver.com/audiobook-categories/3/audiobooks'

options = webdriver.ChromeOptions()
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)

df_title = pd.DataFrame()
url = 'https://audioclip.naver.com/audiobook-categories/3/audiobooks'

driver.get(url)
time.sleep(0.1)
driver.maximize_window()
time.sleep(0.1)

titles = []  # 받아올 것 1 = 제목 : 소설 n개 긁어을 때마다 저장, 여기다 어펜드 시켜야하는
authors = []  # 받아올 것 2 = 저자
informs = []  # 받아올 것 3 = 오디오북 정보
clip_links = [] # 링크 받아올 빈리스트

prev_height = driver.execute_script("return document.body.scrollHeight")

while True:  # 무한스크롤 루프
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(0.3)  # 페이지가 완전히 내려갈때까지 대기 -> 페이지 길이가 길면 시간을 증가시킨다
    curr_height = driver.execute_script("return document.body.scrollHeight")
    if (curr_height == prev_height):
        break
    else:
        prev_height = driver.execute_script("return document.body.scrollHeight")


# for i in range(1, 2747):
for j in range(1, 101):  # 총 오디오북 2747권/ 1-900까지

    clip_link_xpath = '//*[@id="content"]/div/section/div/div/div[3]/div/div/div[{}]/a'.format(j)
    # title_button_xpath = '//*[@id="content"]/div/section/div/div/div[3]/div/div/div[{}]/a/div[2]'.format(j)  # 각각 제목 들어가는 버튼
    # '//*[@id="content"]/div/section/div/div/div[3]/div/div/div[{}]/a'

    try:
        clip_link = driver.find_element('xpath', clip_link_xpath).get_attribute('href') # 링크 정보(객체)를 받아오는 속성값(?)
        driver.find_element('xpath', clip_link_xpath).click()   # 클릭으로 링크 안으로 들어가기
        print(clip_link)
        time.sleep(3)

        title_xpath = '//*[@id="content"]/div/section/div[1]/div[2]/h3' # 제목
        title = driver.find_element('xpath', title_xpath).text  # title = drive--.text 빈리스트 인 title에 불러온 텍스트 저장할라고
        print(title)

        author_xpath = '//*[@id="audiobook"]/div[3]/dl[1]/dd[1]'  # 저자 이름
        # '//*[@id="content"]/div/section/div[1]/div[3]/div[1]/span[1]'
        author = driver.find_element('xpath', author_xpath).text
        print(author)

        inform_xpath = '//*[@id="audiobook"]/div[1]/p'  # 오디오북 정보
        inform = driver.find_element('xpath', inform_xpath).text
        print(inform)

        # one_sentence = title + author + inform
        # one_sentence = re.compile('[^가-힣 ]').sub(' ', title)
        # informs.append(one_sentence)

        titles.append(title)
        authors.append(author)
        informs.append(inform)
        clip_links.append(clip_link)


        driver.back()
        time.sleep(0.1)

        # except NoSuchElementException as e:
        # print('error', j)
        # category_xpath4 = '//*[@id="root"]/div/div[2]/div[2]/div[2]/div[3]/div[{}]/a'.format(j)
        # title = driver.find_element('xpath', category_xpath4).text
        # title = re.compile('[^가-힣]').sub(' ', title)
        # titles.append(title)

        if j % 10 == 0:  # 20 페이지마다 저장됨
            # df = pd.DataFrame({'titles': titles, 'authors': authors, 'informs':informs, 'clip_links':clip_links})
            # df.to_csv('./crawling_data_2_{}.csv'.format(j), index=False)  # index=False 인덱스 필요없음
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['authors'] = authors
            df_section_title['informs'] = informs
            df_section_title['clip_links'] = clip_links
            df_title = pd.concat([df_title, df_section_title], ignore_index=True)
            df_title.to_csv('./crawling_data_2/crawling_data_{}.csv'.format(j),
                            index=False)  # ex) crawling_data_{카테고리 정치}_{페이지 10마다 저장}

            # # 중복 제거하려고 빈리스트 다시 받기
            # titles = []  # 받아올 것 1 = 제목 : 소설 n개 긁어을 때마다 저장, 여기다 어펜드 시켜야하는
            # authors = []  # 받아올 것 2 = 저자
            # informs = []  # 받아올 것 3 = 오디오북 정보
            # clip_links = []

    except:
        print('error', j)



# print(df_title.head())
# print(df_title.category.value_counts())