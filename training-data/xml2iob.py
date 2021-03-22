# Code adapted from https://github.com/bryanoliveira/xml2conll
from pathlib import Path
from xml.dom import minidom
import nltk


def cat2bio(category):
    """ Map categories to BIO format """
    global last_category
    if category == 'O':
        last_category = False
        return 'O'
    elif last_category == category:
        return 'I-' + category
    else:
        last_category = category
        return 'B-' + category


def scandown(elements, categ, output, depth=0):
    """ Scan all the paragraphs searching for text and the annotations """
    global lines
    for el in elements:
        if el.nodeName == '#text':
            for token in nltk.word_tokenize(el.nodeValue):
                category = cat2bio(categ)
                #print(token + ' ' + category)
                output.write(token + ' ' + category + '\n')
        scandown(
            el.childNodes,
            el.attributes['categ'].value if el.attributes and 'categ' in el.attributes else 'O',
            output,
            depth + 1
        )

    if depth == 1:
        output.write('\n')

# Update nltk
nltk.download('punkt')
# Parse all xml files in the current directory
file_list = list(Path('./').rglob('*.xml'))
for file in file_list:
    xmldoc = minidom.parse(file.__str__())
    entries = xmldoc.getElementsByTagName('p')
    print('On traite ' + str(len(entries)) + ' entrées d\'annuaires.')
    output_file_name = file.__str__().split('xml')[0] + ('iob')
    with open(output_file_name, 'a', encoding='utf-8') as output:
        last_category = False
        scandown(entries, 'O', output)

