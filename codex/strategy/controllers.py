from flask import Blueprint


strategy = Blueprint('strategy', __name__, template_folder="templates")


@strategy.route('/')
def index():
    return "strategy"
