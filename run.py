from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def template_index():
    return render_template('index.html')

@app.route("/strategy/")
def template_strategy():
    return render_template('strategy.html')

@app.route("/test")
def template_strategy():
    return render_template('template.html', my_string="Noooo!", my_list=[2,5,6,7])

if __name__ == '__main__':
    app.run(debug=True)
