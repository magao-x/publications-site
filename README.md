# publications-site

Quick and dirty site generator

## 1. Install dependencies

```
pip install toml jinja2
```

## 2. Edit `publications.toml`

The `publications.toml` file is a [TOML](https://github.com/toml-lang/toml) file with sections of the form

```
[[publications]]
title = ""
authors = [
    ""
]
published_in = ""
publication_date = 1970-01-01T00:00:00
url = ""
bibcode = ""
poster_file = ""
manuscript_file = ""
slides_file = ""
abstract = '''
'''
```

Multiple authors can be listed as comma-separated quoted strings (i.e. `authors = ["Ada Lovelace", "Lavinia Steward"]`).

The `bibcode` field is for an ADS [BibCode](http://adsabs.github.io/help/actions/bibcode), like `2018SPIE10703E..09M` from the link http://adsabs.harvard.edu/abs/2018SPIE10703E..09M to retrieve an abstract from [ADS](http://adsabs.harvard.edu).

All fields are required, except for `url`, `poster_file`, `manuscript_file`, and `slides_file`. However, at least one of `url`, `poster_file`, `manuscript_file`, or `slides_file` should be filled in so that a link appears with the entry allowing users to find the published materials.

## 3. Place files under `media/`

Ensure all media files are included under `media/` in this repository so that your links work. The `poster_file`, `manuscript_file`, and `slides_file` attributes should start with `media/` (i.e. the path relative to the folder containing `generate.py`, though the generator just uses the path as-is).

### 3.1. (optional) Compress oversized PDFs

Following [this AskUbuntu]() question, if you have `gs` (GhostScript) installed you can shrink PDF file sizes dramatically with this command:

```
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
```

Where `input.pdf` is the file to shrink, and `output.pdf` will be created by GhostScript. This turned a 35.6 MB PDF from PowerPoint into a 2.1 MB file with minimal loss in quality.

## 4. Run `generate.py`

If everything works, no output will be produced. Open `output/index.html` to review your changes.

## 5. Commit and push your changes

Use `git add`, `git commit`, and `git push` to push your edits back up to GitHub.

## 6. rsync `output/` to `magao-x.org`

The publications site lives at https://magao-x.org/publications, which is served from `/srv/www/publications`.

Example command: `rsync -avz --delete ./output/ magao-x.org:/srv/www/publications`
