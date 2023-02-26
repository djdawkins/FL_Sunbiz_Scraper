import os
import re
import csv
import time
import string
from datetime import datetime
import itertools
import lxml.html

import scrapelib
from bs4 import BeautifulSoup

import settings


def fetch_entities(url):

    filename = url[-1]
    print("Getting", filename)
    # Get data and save locally
    with open(f"{settings.DATA_DIR}/{filename}.csv", "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=settings.OUTPUT_FIELDS, lineterminator = '\n')
        writer.writeheader()

        base_url = "https://search.sunbiz.org"
        sunbiz_url = url
        s = scrapelib.Scraper(retry_attempts=3, requests_per_minute=settings.REQUESTS_PER_MINUTE)
        page_num = 1
        
        while True:
            print("Getting page", str(page_num), " - ", sunbiz_url)
            page_num +=1
            try:
                entity_list_page = s.get(sunbiz_url)
            except scrapelib.HTTPError:
                continue
            except:
                continue
            else:
                page = lxml.html.fromstring(entity_list_page.text)

                entity_name = page.xpath('//*[@id="search-results"]/table/tbody/tr/td[@class="medium-width"]/text()')
                status = page.xpath('//*[@id="search-results"]/table/tbody/tr/td[@class="small-width"]/text()')
                active_link = page.xpath('//*[@id="search-results"]/table/tbody/tr/td[@class="large-width"]/a/@href')
                for name, stat, link in itertools.zip_longest(entity_name, status, active_link):
                    if stat == 'Active':
                        for d in get_entity_detail(base_url + link):
                            if d:
                                writer.writerow(d)

                # Find next page
                next_page_link = page.xpath("//a[@title='Next List']/@href")[0]
                sunbiz_url = base_url + next_page_link
                time.sleep(3)


def get_entity_detail(url):
    
    s = scrapelib.Scraper(
        retry_attempts=4, 
        requests_per_minute=settings.REQUESTS_PER_MINUTE
    )

    try:
        page = s.get(url)
    except:
        yield None

    else:
        soup = BeautifulSoup(page.content, 'html.parser')

        page_data = {
            "Document Number": "",
            "FEI/EIN Number": "",
            "Date Filed": "",
            "Effective Date": "",
            "State": "",
            "Status": ""
        } 

        # Parse name and company type 
        try:
            topline = soup.find('div', {'class','corporationName'}).find_all("p")
        except:
            yield None
        
        else:
            # topline = div_corpName.find_all("p")
            page_data['company_type'] = topline[0].get_text()
            page_data['company_name'] = topline[1].get_text()

            # Parse filing info
            filing_info = soup.find('div', {'class','filingInformation'}).find_all("span")[1]
            filing_info = dict(zip(
                [l.get_text() for l in filing_info.find('div').find_all('label')], 
                [t.get_text() for t in filing_info.find('div').find_all('span')]
                )
            )

            page_data["Document Number"] = filing_info.get("Document Number", "")
            page_data["FEI/EIN Number"] = filing_info.get("FEI/EIN Number", "")
            page_data["Date Filed"] = filing_info.get("Date Filed", "")
            page_data["Effective Date"] = filing_info.get("Effective Date", "")
            page_data["State"] = filing_info.get("State", "")
            page_data["Status"] = filing_info.get("Status", "")

            # Parse other detail sections
            for section in soup.find_all('div', {'class','detailSection'}):
                try:
                    section_head = section.find_all('span')[0].get_text()
                except:
                    section_head = ""

                if "Principal Address" in section_head:
                    page_data["address"] = strip_breaks(section.find_all('span')[1].find('div').get_text()).replace("\r", ", ")

                elif "Registered Agent Name & Address" in section_head:
                    agent = section.find_all('span')
                    page_data["agent"] = strip_breaks(agent[1].get_text())
                    try:
                        page_data["agent_address"] = strip_breaks(agent[2].get_text()).replace("\r", ", ")
                    except IndexError:
                        page_data["agent_address"] = ""


                elif "Authorized Person(s) Detail" in section_head:
                    parts = list(filter(None, section.get_text().split('\n')[3:]))
                    text = " ".join([strip_breaks(l) for l in parts])
                    page_data["authorized_persons"] = text.replace('Title\xa0', '| Title ')

                elif "Annual Reports" in section_head:
                    reports = []
                    table = section.find('table')

                    if table.get_text() == "No Annual Reports Filed":
                        reports.append("No Annual Reports Filed")
                    else:
                        for row in table.find_all("tr")[1:]:
                            reports.append(": ".join([c.get_text() for c in row.find_all('td')]))
                    page_data["annual_reports"] = " | ".join(reports)
                
                elif "Officer/Director Detail" in section_head:
                    officer_director_detail = section.find_all('span')
                    # page_data["officer_director_detail"] = strip_breaks(officer_director_detail[1].get_text())
                    try:
                        page_data["officer_director_detail"] = strip_breaks(section.get_text()).replace("\r", ", ")
                        # page_data["officer_director_detail"] = strip_breaks(officer_director_detail[2].get_text()).replace("\r", ", ")
                    except IndexError:
                        page_data["officer_director_detail"] = ""

            
            # Clean up active/inactive
            status_map = {
                'ACTIVE':'A',
                'INACTIVE':'I'
            }
            if page_data['Status']:
                try:
                    page_data['Status'] = status_map[page_data['Status']] 
                except:
                    pass

            yield page_data


def build_search_urls():
    """
    Builds a list of urls to get lists of entities by name. Sunbiz needs params 
    to list all entities by name, so build a list urls interpolated with all possible searches.
    """
    base = "https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults/EntityName/"
    url_list = []

    # URL search by entities that begin with each letter
    # for letter in string.ascii_lowercase[16:]:
    for letter in ["e", "j"]:
        url_list.append(base + f"{letter}/Page1?searchNameOrder={letter}")
    
    if settings.REVERSE_ORDER:
        url_list.reverse()

    # URL search by entities that begin with each number 0-9
    # for num in range(10):
    #     url_list.append(base + f"/{str(num)}/Page1")

    return url_list


def strip_breaks(text):
    text = text.replace("\n", "").replace("\t", "").replace("<br>", " ")
    text = re.sub(" +", " ", text)
    text = text.replace("  ", " ")
    text = text.strip()
    return text
