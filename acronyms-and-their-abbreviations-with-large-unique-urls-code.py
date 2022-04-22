import pandas as pd
import matplotlib.pyplot as plt
import random
import matplotlib.colors as mcolors
import numpy as np
import csv

# data example
# [http://news.okezone.com/read/2011/03/03/339/430981/mahfud-tolak-tanggapi-ancaman-recall-lily-wahid, JCC=>Jakarta Convention Center, 0.952380952380952]
# format data
# [URL, pasangan akronim=>kepanjangannya, skor
dataa = pd.read_csv('baru.txt', sep=",", header=None, names=["url", "akronim", "skor"])

# print(dataa[dataa['skor'].isnull()])
dataa['skor'] = pd.to_numeric(dataa['skor'], errors='coerce')
dataa = dataa.dropna(subset=['skor'])
dataa['skor'] = dataa['skor'].astype(float)

dataa = dataa.where(dataa['skor'] >= 0.92)
# dropping null value columns to avoid errors 
dataa.dropna(inplace = True) 

# buat nyari ada akronim duplikat
dataa = pd.concat(g for _, g in dataa.groupby("akronim") if len(g) > 1)

# dropping ALL duplicte values 
dataa.drop_duplicates(subset =["akronim", "url"], 
                     keep = 'first', inplace = True) 

# count url
dataa['count'] = dataa.groupby(['akronim', 'skor'])['url'].transform('count')

# gabungin url
df = dataa.groupby(['akronim','skor','count'],as_index=False)['url'].apply('::'.join).reset_index()

# sorting value
df = df.sort_values(by=['count'], ascending=False)

print(df)
# export file
export_file = df.to_csv (r'hasil.txt', index = None, header=None)

#nampilin berapa yang mau ditampilin
df1=df[:15] 

 # Create a list of colors (from iWantHue)
colors = random.choices(list(mcolors.CSS4_COLORS.values()),k = 15)

# Create a pie chart
plt.pie(
    # using data total)arrests
    df1['count'],
    # with the labels being officer names
    labels=df1['akronim'],
    # with no shadows
    shadow=False,
    # with colors
    colors=colors,
    # with the start angle at 90%
    startangle=90,
    # with the percent listed as a fraction
    autopct='%1.1f%%',
    # change font size
    textprops={'fontsize': 9}
    )

# View the plot drop above
plt.axis('equal')

# View the plot
plt.tight_layout()
plt.title("Top 15 Akronim")
plt.show()

