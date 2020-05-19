from flask import Blueprint, render_template
from markupsafe import escape

strategy = Blueprint('strategy', __name__, template_folder="templates")


@strategy.route('/')
@strategy.route('/<path:sub_page>')
def index(sub_page = 'index_strategy'):
    return render_template(sub_page+'.html')
