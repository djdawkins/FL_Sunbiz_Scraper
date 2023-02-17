# FL Sunbiz scraper
A script to scrape businesses from sunbiz.org and output to CSV files.


## Installation
After setting up your preferred virtual environment, install requirements.txt
```
pip install -r requirements.txt
```

Or with poetry
```
poetry install
```

## Configuration
Parameters, including scraper tuning settings, can be set in `settings.py`.


## Runing the script
The main script is in `main.py`. Run the script with:
`python main.py`

## How it works
The scraper generates search urls in the sunbiz business name search for each letter in the alphabet. The script then requests each url and collects each business on every page.

Scraped data is output into a `data` in the project directory. The script will make this folder automatically if it doesn't exist already.

## Caveats
The state's site cannot handle lots of requests at once and can time out if the scraper is not throttled properly. The current settings have worked so far.