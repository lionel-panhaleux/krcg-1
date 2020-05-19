from flask import abort, Flask, g, render_template, current_app
from flask_babel import Babel

# Importing modules
from codex.strategy.controllers import strategy

# Importing configuration
from codex.config import configure_app

app = Flask(__name__, template_folder="templates")
babel = Babel(app)
configure_app(app)

# Retrieving locale and timezone information
@babel.localeselector
def get_locale():
    return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])

@babel.timezoneselector
def get_timezone():
    user = g.get('user', None)
    if user is not None:
        return user.timezone

# Managing the currently used language
# set_language_code is used to inject values into a call for url_for() automatically
@app.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or not g.lang_code:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code

# obtain and set the language code from the request on the application globals flask.g object
@app.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        g.lang_code = values.pop('lang_code', None)

# ensure_lang_support function executes before each request
# it is helpful to verify if the provided language is supported by the application
@app.before_request
def ensure_lang_support():
    lang_code = g.get('lang_code', None)
    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
        return abort(404)

## Default route
@app.route("/")
@app.route("/<lang_code>/")
def index():
    return render_template('index.html', language = g.get("lang_code", "en"))

# Adding Blueprints
app.register_blueprint(strategy, url_prefix='/strategy')
app.register_blueprint(strategy, url_prefix="/<lang_code>/strategy")