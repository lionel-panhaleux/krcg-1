import urllib.parse
import collections
import re
import unidecode

import flask
from flask_babel import Babel
from flask_babel import gettext

# Importing configuration
from codex.config import configure_app


app = flask.Flask(__name__, template_folder="templates")
babel = Babel(app)
configure_app(app)

# Retrieving locale and timezone information
@babel.localeselector
def get_locale():
    return flask.g.get("lang_code", app.config["BABEL_DEFAULT_LOCALE"])


@babel.timezoneselector
def get_timezone():
    user = flask.g.get("user", None)
    if user is not None:
        return user.timezone


# Managing the currently used language
@app.url_defaults
def add_language_code(endpoint, values):
    if "lang_code" in values:
        return
    if app.url_map.is_endpoint_expecting(endpoint, "lang_code"):
        values["lang_code"] = (
            getattr(flask.g, "lang_code", None) or app.config["BABEL_DEFAULT_LOCALE"]
        )


# set the language code from the request
@app.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        flask.g.lang_code = values.pop("lang_code", app.config["BABEL_DEFAULT_LOCALE"])


# ensure_lang_support function executes before each request
# it is helpful to verify if the provided language is supported by the application
@app.before_request
def ensure_lang_support():
    lang_code = flask.g.get("lang_code", None)
    if lang_code and lang_code not in app.config["SUPPORTED_LANGUAGES"].keys():
        return flask.abort(404)


# Defining Errors
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template("404.html"), 404


# Default route
@app.route("/")
@app.route("/<path:page>")
@app.route("/<lang_code>/<path:page>")
def index(lang_code=app.config["BABEL_DEFAULT_LOCALE"], page="index.html"):
    return flask.render_template(page, language=flask.g.get("lang_code"))


# ######################################################################################
# NAVIGATION
# ######################################################################################
Page = collections.namedtuple("Page", ["name", "path", "url"])


class Nav:
    def __init__(self, name, index=False, children=None):
        self.name = name
        self.index = index
        self.children = children or []

    def page(self, path):
        res = unidecode.unidecode(self.name)
        res = re.sub(r"[^\sa-zA-Z0-9]", "", res).lower().strip()
        res = re.sub(r"\s+", "-", res)
        if res == "home":
            res = path
        else:
            res = path + "/" + res
        if not self.children:
            url = res + ".html"
        elif self.index:
            url = res + "/index.html"
        else:
            url = None
        return Page(self.name, res, url)

    def walk(self, path=None, top=None, ante=None, post=None):
        page = self.page(path or "")
        if not self.children or self.index:
            yield (page.path, {"self": page, "top": top, "prev": ante, "next": post})
        if self.index:
            top = page
        for i, child in enumerate(self.children):
            if i > 0:
                ante = self.children[i - 1].page(page.path)
            else:
                ante = None
            if i < len(self.children) - 1:
                post = self.children[i + 1].page(page.path)
            else:
                post = None
            yield from child.walk(path=page.path, top=top, ante=ante, post=post)


STRUCTURE = Nav(
    gettext("Home"),
    index=True,
    children=[
        Nav(
            gettext("Strategy"),
            index=True,
            children=[
                Nav(gettext("Fundamentals")),
                Nav(gettext("Combat")),
                Nav(gettext("Bloat")),
                Nav(gettext("Deck building")),
                Nav(gettext("Archetypes")),
                Nav(gettext("Table Talk")),
                Nav(
                    gettext("Deck guides"),
                    children=[
                        Nav(gettext("Den of Fiends")),
                        Nav(gettext("Libertine Ball")),
                        Nav(gettext("Pact with Nephandi")),
                        Nav(gettext("Parliament of Shadows")),
                    ],
                ),
            ],
        ),
        Nav(
            gettext("Archetypes"),
            index=True,
            children=[
                Nav(gettext("AAA")),
                Nav(gettext("Akunanse Wall")),
                Nav(gettext("Amaravati Politics")),
                Nav(gettext("Anti ventrue Grinder")),
                Nav(gettext("Baltimore Purge")),
                Nav(gettext("Bima Dominate")),
                Nav(gettext("Black Hand")),
                Nav(gettext("Cats")),
                Nav(gettext("Council of Doom")),
                Nav(gettext("Cybelotron")),
                Nav(gettext("Daughters Politics")),
                Nav(gettext("Death Star")),
                Nav(gettext("Dmitri's Big Band")),
                Nav(gettext("Emerald Legion")),
                Nav(gettext("Euro Brujah")),
                Nav(gettext("Girls Will Find Inner Circle")),
                Nav(gettext("Goratrix High Tower")),
                Nav(gettext("Guruhi Rush")),
                Nav(gettext("Hunters")),
                Nav(gettext("Ishtarri Politics")),
                Nav(gettext("Jost Powerbleed")),
                Nav(gettext("Khazar's Diary")),
                Nav(gettext("Kiasyd Stealth & Bleed")),
                Nav(gettext("Lasombra Nocturn")),
                Nav(gettext("Lutz Politics")),
                Nav(gettext("Madness Reversal")),
                Nav(gettext("Mind Rape")),
                Nav(gettext("Mistress")),
                Nav(gettext("Nananimalism")),
                Nav(gettext("Nephandii")),
                Nav(gettext("Nosferatu Royalty")),
                Nav(gettext("Rachel Madness")),
                Nav(gettext("Ravnos Clown Car")),
                Nav(gettext("Renegade Assault")),
                Nav(gettext("Saulot & Friends")),
                Nav(gettext("Scout")),
                Nav(gettext("Shambling Hordes")),
                Nav(gettext("Spirit Marionette")),
                Nav(gettext("Stanislava")),
                Nav(gettext("Team Jacob")),
                Nav(gettext("The Bleeding Vignes")),
                Nav(gettext("The Dark Side of Politics")),
                Nav(gettext("The unnamed")),
                Nav(gettext("Tupdogs")),
                Nav(gettext("Tzimisce Toolbox")),
                Nav(gettext("Tzimisce Wall")),
                Nav(gettext("Ventrue Royalty")),
                Nav(gettext("War Chantry")),
                Nav(gettext("War Ghouls")),
                Nav(gettext("Weenie AUS")),
                Nav(gettext("Weenie DEM")),
                Nav(gettext("Weenie DOM")),
            ],
        ),
        Nav(
            gettext("Best Cards"),
            index=True,
            children=[
                Nav(
                    gettext("Generic"),
                    children=[
                        Nav(gettext("Master")),
                        Nav(gettext("Political action")),
                        Nav(gettext("No discipline")),
                        Nav(gettext("Animalism")),
                        Nav(gettext("Auspex")),
                        Nav(gettext("Celerity")),
                        Nav(gettext("Dominate")),
                        Nav(gettext("Fortitude")),
                        Nav(gettext("Necromancy")),
                        Nav(gettext("Obfuscate")),
                        Nav(gettext("Potence")),
                        Nav(gettext("Presence")),
                    ],
                ),
                Nav(
                    gettext("Sects"),
                    children=[
                        Nav(gettext("Anarch")),
                        Nav(gettext("Camarilla")),
                        Nav(gettext("Laibon")),
                        Nav(gettext("Sabbat")),
                    ],
                ),
                Nav(
                    gettext("Clans"),
                    children=[
                        Nav(gettext("Ahrimanes")),
                        Nav(gettext("Akunanse")),
                        Nav(gettext("Assamite")),
                        Nav(gettext("Baali")),
                        Nav(gettext("Brujah")),
                        Nav(gettext("Caitiff")),
                        Nav(gettext("Daughters of Cacophony")),
                        Nav(gettext("Followers of Set")),
                        Nav(gettext("Gangrel")),
                        Nav(gettext("Giovanni")),
                        Nav(gettext("Guruhi")),
                        Nav(gettext("Harbingers of Skulls")),
                        Nav(gettext("Imbued")),
                        Nav(gettext("Ishtarri")),
                        Nav(gettext("Kiasyd")),
                        Nav(gettext("Lasombra")),
                        Nav(gettext("Malkavian")),
                        Nav(gettext("Nosferatu")),
                        Nav(gettext("Ravnos")),
                        Nav(gettext("Salubri")),
                        Nav(gettext("Toreador")),
                        Nav(gettext("Tremere")),
                        Nav(gettext("True Brujah")),
                        Nav(gettext("Tzimisce")),
                        Nav(gettext("Ventrue")),
                    ],
                ),
            ],
        ),
        Nav(gettext("Deck Search"), index=True),
        Nav(gettext("Card Search"), index=True),
    ],
)


HELPER = dict(STRUCTURE.walk())
print(HELPER)


def _link(page, name=None, _class=None, locale=None, _anchor=None, **params):
    if not page or not page.url:
        return ""
    name = name or page.name
    url = "/" + (locale or get_locale()) + page.url
    if params:
        url += "?" + urllib.parse.urlencode(params)
    if _anchor:
        url += "#" + _anchor
    if _class:
        _class = f"class={_class} "
    else:
        _class = ""
    return flask.Markup(f'<a {_class}href="{url}">{name}</a>')


@app.context_processor
def linker():
    path = flask.request.path[3:]
    if path[-11:] == "/index.html":
        path = path[:-11]
    if path[-5:] == ".html":
        path = path[:-5]
    if path[-1:] == "/":
        path = path[:-1]

    def link(page, name=None, _anchor=None, **params):
        return _link(HELPER[page]["self"], name=name, _anchor=_anchor, **params)

    def translation(locale, name):
        return _link(HELPER[path]["self"], name=name, locale=locale)

    def top():
        return _link(HELPER[path]["top"])

    def next():
        return _link(HELPER[path]["next"], _class="next")

    def prev():
        return _link(HELPER[path]["prev"], _class="prev")

    return dict(link=link, translation=translation, top=top, next=next, prev=prev)


def file_name(name):
    name = unidecode.unidecode(name).lower()
    if name[:4] == "the ":
        name = name[4:] + "the"
    name = re.sub(r"[^a-zA-Z0-9]", "", name)
    return name


@app.context_processor
def display_card():
    def card(name, display_name=None):
        return flask.Markup(
            """<span class="card" onclick="dC('{fname}')">{name}</span>""".format(
                name=display_name or name, fname=file_name(name)
            )
        )

    return dict(card=card)
