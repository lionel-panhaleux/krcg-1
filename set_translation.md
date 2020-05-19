## Using Flask-Babel

Text should be marked as following
```html+jinja2
{{ _('Hello World') }}
OR
{{ gettext('Hello World') }}
```

## Extracting text
```shell
pybabel extract -F codex/babel.cfg -o codex/messages.pot codex
```

## Creating a Translation
```shell
pybabel init -i codex/messages.pot -d codex/translations -l fr
```

## Compiling translation
```shell
pybabel compile -d codex/translations
```
