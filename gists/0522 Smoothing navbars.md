## About navbars

Navbars are some of the more redundant part of a website. Yet, for some time now, I left it as is.
It is somewhat abherrant not to do something about it.

Here is the overall structure of the `footer` block used to display the navbar:
```html+jinja2
{% block footer %}
    <nav role="navigation">
        <a class="prev" href="{{ url_for('strategy.index', sub_page='bloat') }}">Bloat</a>
        <a href="{{ url_for('strategy.index') }}">Strategy</a>
        <a class="next" href="{{ url_for('strategy.index', sub_page='archetypes') }}">Archetypes</a>
    </nav>
{% endblock %}
```

This block appears in EVERY page. Today is about time for me to feel concerned about this point.

## Simplifying the navbar

To lessen the burden of an update, I think that every section should have a layout-`section`.html base template.
Even if it is just to have this tiny bit of templating: (*strategy section*)

**layout-strategy.html**
```html+jinja2
{% block footer %}
    <nav role="navigation">
        {% block previous %}{% endblock %}
        <a href="{{ url_for('strategy.index') }}">Strategy</a>
        {% block next %}{% endblock %}
    </nav>
{% endblock %}
```

**deck-building.html**
```html+jinja2
{% block previous %}
    <a class="prev" href="{{ url_for('strategy.index', sub_page='bloat') }}">Bloat</a>
{% endblock %}

{% block next %}
    <a class="next" href="{{ url_for('strategy.index', sub_page='archetypes') }}">Archetypes</a>
{% endblock %}
```

As it did not reduce the number of lines of the document, it fulfills its role as only representing what is changing.

*it will be tomorrow's task to rewrite every page this way as I feel it to be prettier*

## What can be upgraded

The 'root' layout file sets the `footer` block as follow:

```html+jinja
<footer>
    {% block footer %}
    <img src="{{ url_for('static', filename='img/icons/dark-pack.png') }}">
    <p>
        {{ _('Portions of the materials are the copyrights and trademarks of Paradox Interactive AB, and are used with permission. All rights reserved. For more information please visit') }}
        <a target="_blank" href="http://white-wolf.com">white-wolf.com</a>.
    </p>
    {% endblock %}
</footer>
```

The whole navbar system could be digged deeper:

**root layout.html**
```html+jinja
<footer>
    {% block footer %}
        {% block previous %}{% endblock %}
        {% block current %}
    <img src="{{ url_for('static', filename='img/icons/dark-pack.png') }}">
    <p>
        {{ _('Portions of the materials are the copyrights and trademarks of Paradox Interactive AB, and are used with permission. All rights reserved. For more information please visit') }}
        <a target="_blank" href="http://white-wolf.com">white-wolf.com</a>.
    </p>
        {% endblock %}
        {% block next %}{% endblock %}
    {% endblock %}
</footer>
```

**layout-strategy.html**
```html+jinja
{% extends "layout.html" %}

{% block current %}
    <a href="{{ url_for('strategy.index') }}">Strategy</a>
{% endblock %}
```

Pro: it does help to deal with redundant nav links
Con: it render the templated file less readable
