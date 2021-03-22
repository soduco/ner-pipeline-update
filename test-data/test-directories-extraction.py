import spacy
import pandas as pd
from spacy import displacy
from pathlib import Path
from spacy.tokens import Doc
from ner import postprocessing

#Load test data
file_name = 'Didot_1851a_sample.csv'
tab = pd.read_csv(Path(file_name), encoding='utf8')
raw = tab['raw']
raw = raw.apply(lambda txt: '%s\n' % txt)

#Load updated pipeline
nlp = spacy.load('../ner/model-best')

#Extract named entities in text
docs = nlp.pipe(list(raw))
merged = Doc.from_docs(list(docs))

#Print results in browser: see http://localhost:5000
directory_entities = ["LOC","PER","CARDINAL","ACT","TITRE"]
options = {"ents": directory_entities}
displacy.serve(merged, style="ent", options=options)
