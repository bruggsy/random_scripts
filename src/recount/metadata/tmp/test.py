names = []

for key in mapped_metadata.keys():

    if not 'EFO' in key:
        continue

    key = re.sub(':','_',key)

    req = requests.get('https://www.ebi.ac.uk/ols/api/ontologies/efo/terms/%s' % urllib.quote_plus(urllib.quote_plus('http://www.ebi.ac.uk/efo/%s' % key)))

    names.append(req.json()['label'])

