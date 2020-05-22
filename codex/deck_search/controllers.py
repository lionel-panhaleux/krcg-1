from flask import Blueprint, render_template
from markupsafe import escape

deck_search = Blueprint('deck_search', __name__, template_folder="templates")


@deck_search.route('/')
@deck_search.route('/<path:sub_page>')
def index(sub_page = 'index_deck_search'):
    return render_template(sub_page+'.html')
