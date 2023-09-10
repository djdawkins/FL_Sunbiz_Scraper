import scrapelib
from bs4 import BeautifulSoup
import settings
import pandas as pd

coach_url = "https://en.wikipedia.org/wiki/List_of_current_NCAA_Division_I_FBS_football_coaches"

s = scrapelib.Scraper(retry_attempts=3, requests_per_minute=settings.REQUESTS_PER_MINUTE)
page_num = 1
page = s.get(coach_url)

soup = BeautifulSoup(page.content, 'html.parser')

header_line = soup.find('table').find_all("th")
header_list = []
for i in header_line:
    header_list.append(i.get_text().replace("\n", ""))

nested_list = []
row_elms = soup.find('table').find_all("tr")

count = 0
for i in range(2, len(row_elms)):

    rowline = row_elms[i].find_all("td")
    row_list = []
    url_list = []
    
    # column header positons for school, team, oc, dc, sc url
    num_list = [0, 2, 10, 11, 12]

    for num in num_list:
        a_elm = rowline[num].find("a", href=True)
        if a_elm:
            url = a_elm['href']
            num_a_elm = rowline[num].find_all("a", href=True)

            itr_num = 1
            while len(num_a_elm) > itr_num:
                url += "|" + a_elm.findNext('a')['href']
                print(url)
                itr_num += 1
        
        else:
            url = ""
        
        url_list.append(url)

    for i in rowline:
        row_list.append(i.get_text().replace("\n", ""))

    header_url_list = header_list[:-4] + ['team_url', 'hc_url', 'oc_url', 'dc_url', 'sc_url']
    row_url_list = row_list + url_list
    
    nested_list.append(row_url_list)
print(count)
# creating DataFrame
df = pd.DataFrame(nested_list[2:], columns=header_url_list)

print(df.head())# displaying resultant DataFrame

df.to_csv("school_coach_table.csv", index=False)