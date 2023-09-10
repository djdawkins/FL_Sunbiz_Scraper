import re
from datetime import datetime
import scrapelib
from bs4 import BeautifulSoup
import settings
import pandas as pd
import numpy as np

coach_url = "https://en.wikipedia.org/wiki/List_of_current_NCAA_Division_I_FBS_football_coaches"

s = scrapelib.Scraper(retry_attempts=3, requests_per_minute=settings.REQUESTS_PER_MINUTE)
page_num = 1

coach_url_df = pd.read_csv('school_coach_table.csv')
# coach_url_df = coach_url_df[coach_url_df["Head coach"] == "Kalani Sitake"]

team_coach_urls = coach_url_df["team_url"]

hc_coach_urls = coach_url_df["hc_url"]
hc = coach_url_df["Head coach"]

hc_df = coach_url_df[["Head coach", "hc_url"]]


oc_coach_urls = coach_url_df["oc_url"]
dc_coach_urls = coach_url_df["dc_url"]
sc_coach_urls = coach_url_df["sc_url"]

df_list = []

for i in hc_df.index:
# for i in hc_coach_urls:
# for i in range(3, 4):
    page = s.get("https://en.wikipedia.org" + hc_df["hc_url"][i])
    soup = BeautifulSoup(page.content, 'html.parser')

    page_id = soup.find("a", {"class": "wbc-editpage"}, href=True)['href']
    page_id = re.search(r'Q\d*', page_id).group()
    table_elm = soup.find('table', {"class": "infobox vcard"})
    if not table_elm:
        table_elm = soup.find('table', {"class": "infobox biography vcard"})
        print(hc_df["Head coach"][i])

    tr_list = table_elm.find_all("tr")

    tuple_list = []
    i_header_text = ""
    for tr in tr_list:
        
        i_image = tr.find("td", {"class": "infobox-image"})
        if i_image:
            continue
            
        i_header = tr.find("th", {"class": "infobox-header"})

        if i_header:
            i_header_text = i_header.get_text()
            continue
        
        i_label = tr.find("th", {"class": "infobox-label"})
        i_data = tr.find("td", {"class": "infobox-data"})

        if i_label:

            i_label_text = i_label.get_text()
            i_data_text = i_data.get_text()
            school_href = ""
            position_href = ""

            school_a = i_data.find_all("a", href=True)
            
            school_href = school_a[0]["href"] if len(school_a) == 1 else ""
            school_href = school_a[0]["href"] if len(school_a) == 2 else ""
            school_title = school_a[0]["title"] if len(school_a) == 2 else ""

            idx = 0
            title_list = []
            link_list = []
            while idx < len(school_a):
                a_tag_title = school_a[idx].get("title")
                a_tag_link = school_a[idx]["href"]

                # if not a_tag_title:
                #     title_list.append(a_tag_title)
                #     link_list.append("https://en.wikipedia.org" + school_a[i]["href"])
                #     print(title_list,'\t' , link_list)

                header_label_data_tuple = (i_header_text, i_label_text, i_data_text, a_tag_title, a_tag_link)
                tuple_list.append(header_label_data_tuple)

                idx += 1
            
            if len(school_a) == 0:
                # print(i_data_text)
                header_label_data_tuple = (i_header_text, i_label_text, i_data_text, np.nan, np.nan)
                tuple_list.append(header_label_data_tuple)
            # header_label_data_tuple = (i_header_text, i_label_text, i_data_text, title_list, link_list)
            # tuple_list.append(header_label_data_tuple)


    info_box_df = pd.DataFrame.from_records(tuple_list, columns =['i_header', 'i_label', 'i_data', 'title', 'link'])

    info_box_df["coach_name"] = hc_df["Head coach"][i]
    info_box_df["id"] = page_id

    df_list.append(info_box_df)
 
df = pd.concat(df_list)
unq_before = list(df.i_header.unique())

i_header_keep_list = ["Career information", "Coaching career", "Coaching career (HC unless noted)",\
                  "Playing career", "Biographical details", "Administrative career (AD unless noted)",\
                    "Personal information", "Baseball", "Football", "Basketball"]

df_filt = df[df.i_header.isin(i_header_keep_list)]
df_filt = df_filt[~((df_filt.i_header == "Personal information") & (df_filt.i_label != "Born:"))]

unq_after = list(df_filt.i_header.unique())

temp3 = [x for x in unq_before if x not in set(unq_after)]

# print("Unique i_header: \n",unq_after)
# print("Diff: \n",temp3)

# print(df_filt.head())
df_filt.to_csv('hc_relationship_table.csv')
