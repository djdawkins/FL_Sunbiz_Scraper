import pandas as pd
import spacy
from spacy import displacy
from spacy.pipeline.ner import DEFAULT_NER_MODEL
pd.set_option('mode.chained_assignment', None)

ner = spacy.blank("en")

config = {
   "moves": None,
   "update_with_oracle_cut_size": 100,
   "model": DEFAULT_NER_MODEL,
   "incorrect_spans_key": "incorrect_spans",
}
ner.add_pipe("ner")


hc_relationship_df = pd.read_csv('hc_relationship_table.csv')
coach_career = hc_relationship_df[hc_relationship_df.i_header == "Coaching career (HC unless noted)"]

coach_career[["org", "role_1", "role_2"]] = coach_career.i_data.str.split(r'\(', expand=True)

coach_career["role"] = (coach_career.role_2).where(coach_career.role_2.notna(), coach_career.role_1)

coach_career["org"] = coach_career.org.str.replace(')','')
coach_career["org"] = coach_career.org.str.strip()

coach_career["role_1"] = coach_career.role_1.str.replace(')','')
coach_career["role_2"] = coach_career.role_2.str.replace(')','')
coach_career["role"] = coach_career.role.str.replace(')','')

coach_career["role"] = (coach_career.role).where(coach_career.role.notna(), "HC")
coach_career["coach_role"] = coach_career.role.str.split("/",expand=False)

coach_career["year"] = coach_career.i_label.str.split("–")


coach_career.drop(coach_career.columns[0], axis=1, inplace=True)

# coach_career.to_csv('coach_career.csv', index=False)
# print(coach_career.head())
print(coach_career.columns)








