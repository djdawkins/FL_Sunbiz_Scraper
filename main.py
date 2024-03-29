import os

import concurrent.futures
import logging

import settings
from scrape import fetch_entities, build_search_urls
from dotenv import load_dotenv
load_dotenv()
import boto3

#Creating Session With Boto3.
# Add additional code here as needed
s3_obj = boto3.client('s3', region_name=settings.AWS_REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
bucket_name = "fl-sunbiz-bucket"
bucket_key = r"data/"

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

def write_csv_to_s3():
    # assign directory
    directory = f"{settings.DATA_DIR}"
    
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            s3_obj.upload_file(f, bucket_name, bucket_key+filename)


if __name__ == "__main__":
    
    # Create output folder if it doesnt already exist.
    if not os.path.exists('data'):
        os.makedirs('data')

    print("Getting data...")
    run()
    # write_csv_to_s3()
