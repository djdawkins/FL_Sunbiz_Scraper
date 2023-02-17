# Number of threads to run for multithreading
MAX_THREADS = 4

# Controls the amount of url requests per minute
REQUESTS_PER_MINUTE = 30

# Output directory
DATA_DIR = "data"

# Fieldnames to output in CSV files
OUTPUT_FIELDS = ["Document Number","FEI/EIN Number","Date Filed","Effective Date","State","Status",
'company_type','company_name','address','agent','agent_address',
'authorized_persons','annual_reports', 'officer_director_detail']

# If True, scraper will go from Z-A in business name searches
REVERSE_ORDER = False