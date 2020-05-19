from flask import Blueprint, render_template
from markupsafe import escape

archetypes = Blueprint('archetypes', __name__, template_folder="templates")


@archetypes.route('/')
@archetypes.route('/<path:sub_page>')
def index(sub_page = 'index_archetypes'):
    return render_template(sub_page+'.html')
