
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

url = 'https://content.codecademy.com/courses/beautifulsoup/cacao/index.html'
## Guide = http://flavorsofcacao.com/review_guide.html

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')


### Ratings

rate = soup.select('.Rating')


ratings = []

for rating in rate:
  a = rating.text
  ratings.append(a)

for i in range(1,len(ratings)):
  ratings[i] = float(ratings[i])


print(ratings)
ratings_nostr = ratings[1:len(ratings)]
plt.hist(ratings_nostr)
plt.show()

### Company names }


company_name_temp = soup.select('.Company')

company_name = []

for tag in company_name_temp:
  company_name.append(tag.text)
  
### Create Data Frame  


d = {"Company_name": company_name, "Rating": ratings}
df_choco= pd.DataFrame.from_dict(d)
df_choco.drop(labels=0, inplace=True)
df_choco['Rating'] = pd.to_numeric(df_choco['Rating'])
print(df_choco.dtypes)  

av_values = df_choco.groupby('Company_name')['Rating'].mean()

ten_best = av_values.nlargest(10)

## checking corelation with cocoa percentage

cocoa_percent_temp = soup.select('.CocoaPercent')

cocoa_percent = []

for element in cocoa_percent_temp:
    x = element.text.strip('%')
    cocoa_percent.append(x)

cocoa_percent = cocoa_percent[1:len(cocoa_percent)]

df_choco["CocoaPercentage"] = cocoa_percent
df_choco['CocoaPercentage'] = pd.to_numeric(df_choco['CocoaPercentage'])

print(df_choco.dtypes)    

plt.clf()
plt.scatter(df_choco['CocoaPercentage'], df_choco['Rating'])
z = np.polyfit(df_choco['CocoaPercentage'], df_choco['Rating'], 1)
line_function = np.poly1d(z)
plt.plot(df_choco['CocoaPercentage'], line_function(df_choco['CocoaPercentage']), "r--")
plt.show()

company_location_temp = soup.select('.CompanyLocation')
company_location = []
for item in company_location_temp:
    company_location.append(item.text)

company_location = company_location[1:len(company_location)]
df_choco["CompanyLocation"] = company_location

country_grouop = df_choco.groupby('CompanyLocation')['Rating','CocoaPercentage'].mean()

top_10_countries = country_grouop.nlargest(10 , columns='Rating')

print(top_10_countries)

