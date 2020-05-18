# Flask
from flask import Flask, render_template
# Variable Rules
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def template_index():
    return render_template('index.html')

@app.route('/strategy/')
@app.route('/strategy/<path:sub_page>')
def template_strategy(sub_page = 'index'):
    return render_template('strategy/'+sub_page+'.html')

@app.route("/test")
def template_test():
    return render_template('template.html', my_string="Noooo!", my_list=[2,5,6,7])

if __name__ == '__main__':
    app.run(debug=True)
