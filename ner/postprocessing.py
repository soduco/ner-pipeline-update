from spacy.language import Language
from spacy.tokens.span import Span

@Language.component('expand_entities')
def expand_left_right(doc):
  return expand_right(expand_left(doc))


def expand_left(doc):

  if not doc.ents:
    return doc
    
  expandme = ['PER','ACT','TITRE']

  first_ent = doc.ents[0]
  
  # On peut étendre à gauche
  new_ents = ()
  if first_ent.start > 0 and first_ent.label_ in expandme:
    if first_ent.label_ == 'PER':
      new_ent = Span(doc, 0, first_ent.end, label=first_ent.label)
      new_ents =(new_ent,) + doc.ents[1:]
    elif first_ent.label_ in ['ACT','TITRE']:
      pos = first_ent.start
      if doc[first_ent.start].nbor(-1).is_punct: 
        pos -= 1

      new_ent = Span(doc, 0, pos, label='PER')
      new_ents = (new_ent,) + doc.ents

  if new_ents:
    doc.ents = new_ents

  return doc


#On crée des règles de correction des étiquetages ratés pour les ACTIVITES
def expand_right(doc):
  expandme = ['ACT', 'LOC']

  # pour chaque entité dans acts, on récupère tous les tokens jusqu'à la prochaine entité
  new_entities = []
  for ent in doc.ents:
    if ent.label_ not in expandme:
      new_entities.append(ent)
      continue
    
    new_end_pos = ent.end
    last_token = None
    # Continue until we reach another entity
    for token in doc[ent.end:]:
      if token.ent_type_:
        break
      new_end_pos += 1
      last_token = token
    
    # On n'attrape pas la dernière virgule
    if last_token and last_token.is_punct:
      new_end_pos -= 1

    if ent.end == new_end_pos:
      new_entities.append(ent)
    else:
      new_ent = Span(doc, ent.start, new_end_pos, label=ent.label)
      new_entities.append(new_ent)

  doc.ents = new_entities
  return doc
