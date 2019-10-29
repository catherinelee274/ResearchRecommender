#scrapes arxiv

import arxivscraper
import pandas as pd

#orig was 2018- 5/27
scraper = arxivscraper.Scraper(category='cs',date_from='2019-5-01',date_until='2019-10-26',t=1, filters={'categories':['cs.lg']})

output = scraper.scrape()

cols = ('id', 'title', 'categories', 'abstract', 'doi', 'created', 'updated', 'authors')
df = pd.DataFrame(output,columns=cols)

#save to a file
df.to_csv('path2.csv') # this is good