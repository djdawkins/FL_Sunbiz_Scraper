import os
import re
import csv
import time
import string
from datetime import datetime
import itertools
import lxml.html
import requests
import scrapelib
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import spacy
from spacy import displacy
from spacy.pipeline.ner import DEFAULT_NER_MODEL

ner = spacy.blank("en")

config = {
   "moves": None,
   "update_with_oracle_cut_size": 100,
   "model": DEFAULT_NER_MODEL,
   "incorrect_spans_key": "incorrect_spans",
}
ner.add_pipe("ner")


hc_relationship_df = pd.read_csv('hc_relationship_table.csv')
bio_details = hc_relationship_df[hc_relationship_df.i_header == "Biographical details"]

coach_career_data = bio_details.i_data

# coach_career[["org", "role_1", "role_2"]] = coach_career.i_data.str.split(r'\(', expand=True)

# coach_career["role"] = (coach_career.role_2).where(coach_career.role_2.notna(), coach_career.role_1)

bio_details["i_data"] = bio_details.i_data.str.replace('\n',' ', regex=True)
# bio_details[["a","num_date", "b", "str_date","x", "age", "y", "location"]] = bio_details.i_data.str.split('(|)', expand=True)

bio_details_born = bio_details[bio_details.i_label == "Born"]
bio_details_born[["drop_col","num_date", "str_date", "age", "location"]] = bio_details_born[bio_details_born.i_label == "Born"].i_data.str.split('\(|\)', expand=True)
bio_details_born.drop('drop_col', axis=1, inplace=True)

bio_details_born = bio_details_born.iloc[:, -6:]
bio_details_born["age"] = bio_details_born.age.str.replace('age', '').str.strip()

bio_details_born['location'] = bio_details_born['location'].str.replace(r"\[.*?\]","", regex=True)

# bio_details_born['id'] = bio_details_born['coach_name'] + "_" + bio_details_born['num_date']

bio_details_born.to_csv('bio_details_born.csv')

# print(bio_details[bio_details.i_label == "Born"].i_data.str.split('\(|\)', expand=True))

# coach_career["org"] = coach_career.org.str.replace(')','')
# coach_career["role_1"] = coach_career.role_1.str.replace(')','')
# coach_career["role_2"] = coach_career.role_2.str.replace(')','')
# coach_career["role"] = coach_career.role.str.replace(')','')

# coach_career["role"] = (coach_career.role).where(coach_career.role.notna(), "HC")
# coach_career["coach_role"] = coach_career.role.str.split("/",expand=False)

# coach_career["year"] = coach_career.i_label.str.split("–")

bio_details_alma_mater = bio_details[bio_details.i_label == "Alma mater"]
# bio_details_alma_mater = bio_details

bio_details_alma_mater.to_csv('test_df.csv')


