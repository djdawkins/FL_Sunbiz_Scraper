import os

import concurrent.futures
import logging

import settings
from scrape import fetch_entities, build_search_urls

# Set up local logfile
logging.basicConfig(filename="sunbiz.log",
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)


def run():
    urls = build_search_urls() # needs to return list wiki school-coach-list
    print(urls)
    # # Initiate multi-thread scrape of urls
    # threads = min(settings.MAX_THREADS, len(urls))
    # with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    #     for r in executor.map(fetch_entities, urls):
    #        return r



if __name__ == "__main__":
    
    # Create output folder if it doesnt already exist.
    if not os.path.exists('data'):
        os.makedirs('data')

    print("Getting data...")
    run()