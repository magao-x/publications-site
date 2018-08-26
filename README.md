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
poster_file = ""
manuscript_file = ""
slides_file = ""
abstract = '''
'''
```

Multiple authors can be listed as comma-separated quoted strings (i.e. `authors = ["Ada Lovelace", "Lavinia Steward"]`).

All fields are required, except for `url`, `poster_file`, `manuscript_file`, and `slides_file`. However, at least one of `url`, `poster_file`, `manuscript_file`, or `slides_file` should be filled in so that a link appears with the entry allowing users to find the published materials.

## 3. Place files under `media/`

The generator is not smart enough to follow paths and copy files from there, so ensure all media files are included under `media/` in this repository.

## 4. Run `generate.py`

If everything works, no output will be produced. Open `output/index.html` to review your changes.

## 5. Commit and push your changes

Use `git add`, `git commit`, and `git push` to push your edits back up to GitHub.

## 6. rsync `output/` to `magao-x.org`

The publications site lives at https://magao-x.org/publications, which is served from `/srv/www/publications`.

Example command: `rsync -avz --delete ./output/ magao-x.org:/srv/www/publications`