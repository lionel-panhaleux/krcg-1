*From gist dated Thu, May 21st*

## Cascade inheritance

I a using a `layout-child.html` extending the global `layout.html` to adapt the current part of the website to the needs of the section

## Templating Archetypes

As I delved into the static version of `aaa.html`, i found that several situations were handled differently from the Strategy section. I chose to built a dedicated template to simplify later interactions
```html+jinja2
{% extends "layout.html" %}

[...]

{% block content %}
	{% block archetype_name %}{% endblock %}
	<div id="decklist" class="decklist" style="display: none">
        <h2 id="deck-name"><a id="deck-link" href="http://example.com"></a></h2>
        <p id="deck-header"></p>
        <h3 id="crypt-header"></h3>
        <ul id="crypt-list">
        </ul>
        <h3 id="library-header"></h3>
        <ul id="library-list">
        </ul>
	</div>

	{% block archetype %}{% endblock %}

	{% block errata %}{% endblock %}
{% endblock %}
```

## Redefining `content`

As you can see, I redefined the `content` block to store different kind of informations: first the name of the archetype, then the common structure of the decklist, then the analysis of the archetype and the errata.

## The `errata` block
This block could store *by default* the `<div>` tag but I figured that some archetypes would be free from any errata so I chose not to include it by default

This block has another trick : **macros**

As erratas affect every deck the same way, I chose to store the specific paragraph into another file and calling to ne needed erratum when it was needed.

```html+jinja2
{% import "layout-erratum.html" as erratum %}

{% block errata %}
<div class="warning">
    <h3>Errata</h3>
    {{ erratum.pentextmsubversion() }}
    {{ erratum.villein() }}
    {{ erratum.parityshift() }}
	{{ erratum.antheliostheredstar() }}
</div>
{% endblock %}
```

This solution will enable a smoothier way of integrating future errata to the pages

For example
```html+jinja2
{% macro pentextmsubversion() -%}
<p>
    <span class="card" onclick="dC('pentextmsubversion')">Pentex™ Subversion</span>
    has been modified by an <em>errata</em> in September 2019.
    It does not prevent a vampire to act anymore, so it is less powerful and should probably
    not be included in the deck.
</p>
{%- endmacro %}
```

## The case of `Pentex(TM) Subversion`

It appeared that the above card has two different texts depending on the impact of the change. The new macro would be

```html+jinja2
{% macro pentextmsubversion( solution = "remove" ) -%}
{% if solution is 'remove' %}
<p>
    <span class="card" onclick="dC('pentextmsubversion')">Pentex™ Subversion</span>
    has been modified by an <em>errata</em> in September 2019.
    It does not prevent a vampire to act anymore, so it is less powerful and should probably
    not be included in the deck.
</p>
{% else %}
<p>
    <span class="card" onclick="dC('pentextmsubversion')">Pentex™ Subversion</span>
    has been modified by an <em>errata</em> in September 2019.
    It does not prevent a vampire to act anymore, so it is less powerful but still has its place in the deck,
    as it was mainly used as a way to disable a blocker anyway.
</p>
{% endif %}
{%- endmacro %}
```
