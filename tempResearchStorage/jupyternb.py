#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import pandas

#%%
#@title Testing
df = pandas.read_csv('path.csv')
#print(df.head(5))
#print(df['abstract'])

#%%
i = 0
for index, row in df.iterrows():
    print(row['abstract'])
    i+=1
    if i == 2:
        break

