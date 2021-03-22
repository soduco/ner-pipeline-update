Mise à jour d'un modèle de langue Spacy pour extraire les entrées des annuaires Didot-Bottin
===


****Scripts Python à utiliser:****

   - **xml2iob** : transforme un fichier au format XML en fichier IOB utilisable par Spacy.
   - **postprocessing**: règles de correction de certaines erreurs d'extraction du modèle.
   - **test-directories-extraction**: script de test du pipeline d'extraction d'entités nommées.

****Ressources:****

Les données d'entraînement se divisent en deux corpus, de tailles à peu près égales, correspondant aux pages des annuaires traitées lors de l'atelier d'annotation de décembre 2020 : un corpus d'entraînement, un corpus de développement. Ils sont annotés à l'aide de balises XML du type <ent categ='TEXT'></ent>, la valeur de TEXT correspondant au type de l'entité nommée comprise entre les les balises. Les valeurs possibles de TEXT pour nos corpus sont:
    
    - PER: entrée d'annuaire, très majoritairement des personnes, parfois des noms d'entreprises ou d'administrations...
    - TITRE: éventuel titre honorifique de la personne concernée par l'entrée courante. Par exemple "O. ::LH::" signifie "Officier de la Légion d'Honneur".
    - ACT: éventuelle activité signalée dans l'entré d'annuaire. Par exemple "cordonnier".
    - LOC: localisation fournie dans l'entrée d'annuaire. Par exemple "impasse Guemenée".
    - CARDINAL: numéro complétant la localisation. Par exemple "8 bis".

****Etapes du traitement****

0- Installer Spacy:

`python -m venv .env`

`.env\Scripts\activate`

`pip install -U pip setuptools wheel`

`pip install -U spacy`

`python -m spacy download fr_core_news_lg`

1- Convertir les corpus d'entraînement et de développement en IOB avec le script xml2iob, puis en JSON, et enfin en *.spacy avec les lignes de commande suivantes:

`python -m spacy convert ./training-data/Didot_Train.iob ./training-data --converter ner --file-type json -n 10 --model fr_core_news_lg --lang fr`

`python -m spacy convert ./training-data/Didot_Train.json ./training-data --converter json --file-type spacy -n 10 --model fr_core_news_lg --lang fr`

`python -m spacy convert ./training-data/Didot_Dev.iob ./training-data --converter ner --file-type json -n 10 --model fr_core_news_lg --lang fr`

`python -m spacy convert ./training-data/Didot_Dev.json ./training-data --converter json --file-type spacy -n 10 --model fr_core_news_lg --lang fr`

2- Créer un fichier de configuration de base de modèle avec l'utilitaire fourni ici: https://spacy.io/usage/training#quickstart. NB: On veut seulement un pipeline qui fait de l'extraction d'entités nommées, donc on peut ne sélectionner que les composants NER et Tok2Vec.
 Coller ce fichier dans le dossier "ner".

3- Ajouter les chemins des fichiers d'entraînement *.spacy dans ce fichier de config. Pour dire que l'on veut "mettre à jour" les composants de ner et tok2vec, ajouter;

```
[components.ner]
source = "fr_core_news_lg"
```

4- Pour ajouter un label au composant de ner, laisser le système le détecter tout seul dans les données d'entraînement.

5- Générer le fichier de configuration final avec la commande:

`cd ner`

`python -m spacy init fill-config base_config.cfg config.cfg`

6- Lancer l'entraînement du modèle avec la commande:
`python -m spacy train ./config.cfg --output ./`

7- En option: Le fichier postprocessing.py contient des règles permettant d'étendre vers la gauche ou la droite l'étendue des entités nommées détectées par le modèle lorsqu'il est assez évident que celle-ci ne couvre pas l'ensemble des tokens qui devraient en faire partie. Pour ajouter ces règles comme un composant du pipeline de nlp, à appliquer après l'étape de 'ner', il faut:	
- Dans le fichier config.cfg du model-best ajouter :
- Dans la partie [nlp]: `pipeline = ["tok2vec","ner","expand_entities"]`
- Plus bas, une partie : 
```
[components.expand_entities]
factory = "expand_entities"
```

8- Pour tester le nouveau pipeline, exécuter le script test-directories-extraction. Les résultats sont visualisables via un navigateur à l'adresse: http://localhost:5000 

9- Générer un package python qui contient tout le pipeline (fichier *.tar.gz):
`python -m spacy package ./model-best ./ --code ./postprocessing.py --name ner_directories --version 0.2`

