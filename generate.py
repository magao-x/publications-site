from jinja2 import Template
import toml
from os.path import exists, dirname, join, isdir
from os import makedirs
import shutil
import datetime

project_dir = dirname(__file__)
output_dir = join(project_dir, 'output')

if __name__ == "__main__":
    template = Template(open(join(project_dir, 'template.html')).read())
    publications = toml.load(join(project_dir, 'publications.toml'))['publications']
    makedirs(output_dir, exist_ok=True)
    output = template.render({
        'publications': publications,
        'today': datetime.datetime.today()
    })
    with open(join(output_dir, 'index.html'), 'w') as f:
        f.write(output)
    media_dir, styles_dir = join(output_dir, 'media'), join(output_dir, 'styles')
    if isdir(media_dir):
        shutil.rmtree(media_dir)
    if isdir(styles_dir):
        shutil.rmtree(styles_dir)
    shutil.copytree(join(project_dir, 'media'), media_dir)
    shutil.copytree(join(project_dir, 'styles'), styles_dir)