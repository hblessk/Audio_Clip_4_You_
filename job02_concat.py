import pandas as pd
import glob

data_paths = glob.glob('./crawling_data/*')

df = pd.DataFrame()
for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)             # nan값 제거
    df_temp.drop_duplicates(inplace=True)    # 중복제거
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
print(len(df.titles.value_counts()))
df.to_csv('./crawling_data/audio_clip_1_2470.csv', index=False)

# 크롤링데이터 1 ~ 2747개(2740) 컨캣파일명  => audio_clip_1_2470