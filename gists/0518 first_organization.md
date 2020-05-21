*From gist dated Mon, May 18th*

## Structure of the run.py file

I used Flask to handle routing as it appeared to make Jinja2 templating easier
```python
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

if __name__ == '__main__':
    app.run(debug=True)
```

## Ordering files

As I used the above system, I sorted the files following the following system

```
run.py
|- static
	|- css
	|- fonts
	|- img
		|- card-images
		|- icons
	|- js
	|- pdf
|- template
	|- strategy
		|- deck-guides
		index.html
	layout.html
	index.html
```
## Where I am at

Currently, the biggest issue with the system I came up with is hypertext links like this snippet from `template/strategy/combat.html`

```html
<p>
	Combat does not help reducing the prey's pool, at least not directly.
	The core principle of combat is <strong>bruise</strong>: reducing its opponents blood amount.
	It forces the minions to hunt or stay in torpor,
	seriously reducing <a href="../strategy/fundamentals.html#AB">A&B</a>.
	As a bonus, reducing the blood amount on the table means diminishing the effectivness of
	<a href="bloat.html#leeching">leeching</a> techniques.
</p>
```

## Fixing

Here's the solution, it works just fine :
```html+jinja
<a href="{{ url_for('template_strategy', sub_page='fundamentals', _anchor='AB') }}">
```
