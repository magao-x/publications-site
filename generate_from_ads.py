import io
from glob import glob
import os
import json
import requests
import dateutil.parser
from jinja2 import Template
from os.path import exists, dirname, join, isdir, basename, splitext
from os import makedirs
import shutil
import datetime

project_dir = dirname(__file__)
output_dir = join(project_dir, 'output')

PREFERRED_LINK_TYPES = [
    ('journal', 'PUB_HTML'),
    ('journal PDF', 'PUB_PDF'),
    ('arXiv', 'EPRINT_HTML'),
    ('arXiv PDF', 'EPRINT_PDF'),
]

MAX_ENTRIES = 1000

def main():
    template = Template(open(join(project_dir, 'template.html')).read())
    makedirs(output_dir, exist_ok=True)
    media_dir, styles_dir = join(output_dir, 'media'), join(output_dir, 'styles')
    if isdir(media_dir):
        shutil.rmtree(media_dir)
    if isdir(styles_dir):
        shutil.rmtree(styles_dir)

    token = os.environ.get('ADS_API_TOKEN')
    if token is None:
        raise RuntimeError("Export ADS_API_TOKEN in your environment with the API key you get from the ADS web interface: https://ui.adsabs.harvard.edu/user/settings/token")

    library_id = os.environ.get('ADS_LIBRARY_ID')
    if library_id is None:
        raise RuntimeError("Export ADS_LIBRARY_ID in your environment with the value from the last segment of the URL. E.g. for https://ui.adsabs.harvard.edu/public-libraries/EctrgCz4QjagJOiSxQlAXg you would export ADS_LIBRARY_ID=EctrgCz4QjagJOiSxQlAXg")

    headers = {'Authorization': 'Bearer ' + token}
    response_payload = requests.get(f"https://ui.adsabs.harvard.edu/v1/biblib/libraries/{library_id}?fl=bibcode&rows={MAX_ENTRIES}&start=0", headers=headers).json()
    bibcodes = response_payload['documents']

    export_payload = {
        'bibcode': bibcodes,
        'sort': 'date desc',
    }
    export_text = requests.post("https://api.adsabs.harvard.edu/v1/export/refabsxml",
                                headers=headers,
                                data=json.dumps(export_payload)).json()['export']

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(export_text, 'xml')

    publications = []
    for rec in soup.find_all('record'):
        extracted = {}
        extracted['title'] = rec.find('title').text
        extracted['authors'] = []
        for author in rec.find_all('author'):
            last_name, first_names = author.text.split(',', 1)
            name = first_names.strip() + ' ' + last_name.strip()
            extracted['authors'].append(name)
        extracted['kind'] = rec.attrs.get('type', 'article')
        extracted['bibcode'] = rec.find('bibcode').text
        extracted['journal'] = rec.find('journal').text
        extracted['abstract'] = rec.find('abstract').text
        extracted['links'] = []
        for label, kind in PREFERRED_LINK_TYPES:
            if rec.find('link', type=kind) is None:
                continue
            url = rec.find('link', type=kind).find('url').text
            extracted['links'].append({'label': label, 'url': url})
        extracted['publication_date'] = dateutil.parser.parse(rec.find('pubdate').text)
        extracted['attachments'] = []
        rec_files = join(project_dir, 'media', extracted['bibcode'])
        if exists(rec_files):
            for fn in glob(join(rec_files, '*')):
                bn = basename(fn)
                name, ext = splitext(bn)
                extracted['attachments'].append({'name': name, 'filename': join('media', extracted['bibcode'], bn)})
        publications.append(extracted)


    # import code
    # code.interact(local=locals())
    output = template.render({
        'publications': publications,
        'today': datetime.datetime.today(),
        'library_id': library_id,
    })
    with open(join(output_dir, 'index.html'), 'w') as f:
        f.write(output)
    shutil.copytree(join(project_dir, 'media'), media_dir)
    shutil.copytree(join(project_dir, 'styles'), styles_dir)
    # import xml.etree.ElementTree as ET
    # tree = ET.parse(io.StringIO(export_text))
    


if __name__ == "__main__":
    main()