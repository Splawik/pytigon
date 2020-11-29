# Szablony Pytigon'a

System szablonów Pytigona bazuje na szablonach django:

https://docs.djangoproject.com/en/2.2/ref/templates/language/

Szablon Pytigon'a to zapisany w innym formacie szablon django. Przy pomocy specjalnego preprocesora szablony Pytigon'a (standardowe rozszerzenia .ihtml) kompilowane są do szablonów .html, zgodnych w 100% ze składnią django.

Zamiarem autora było poprawić czytelość szablonów django nie rezygnując ze 100% kompatybilności z nimi.
Najbardziej znaczącą zmianą w stosunku do Django było wprowadzenie wcięć. Zasady są następujące:

---

### Jeżeli pierwszy nie będący spacją znak w linii nie zaczyna się od litery i znaku '%', linia tekstu nie jest przetwarzana.

blok:

```html
<h1>Hello world!</h1>
```

konwertowany jest do:

```
<h1>Hello world!</h1>
```

---

### Jeżeli pierwszy znak w linii nie będący spacją jest '.' to znak '.' jest pomijany, reszta nie jest przetwarzana.

blok:

```
.abc
```

konwertowany jest do:

```
abc
```

---

### Jeżeli pierwszy nie będący spacją znak jest literą, traktowany jest jako tag html. Automatycznie generowany jest tag zamykający gdy na tym samym poziomie wcięcia lub mniejszym pojawia się ciąg znaków

blok

```
h1
```

konwertowany jest do:

```html
<h1></h1>
```

blok:

```
h1
div
    p
```

konwertowany jest do:

```html
<h1></h1>
<div><p></p></div>
```

---

### Składnia taga html jest następująca: tag[ key=value[,,,[key=value]]...clear html text

blok:

```
p class=test
```

konwertowany jest do:

```html
<p class="test"></p>
```

blok:

```
p class=test,,,style=padding:10...Hello world!
```

konwertowany jest do:

```html
<p class="hello" style="padding:10">Hello world!</p>
```

---

### Jeżeli linia zaczyna się od '%%' - oznacza to początek bloku django, jeżeli linia kończy się znakiem ':' automatycznie dodawany jest element zamykający blok zgodnie z poziomem wcięć

blok:

```
%% test:
    p...Hello!
```

konwertowany jest do:

```html
{% block test %}
<p>Hello!</p>
{% endblock %}
```

---

### Jeżeli linie rozpoczyna pojedynczy znak '%' traktowany jest jako tag Django. Jeżeli linia kończy się znakiem ':' aytomatycznie jest dodawany tag zamykający.

blok:

```
% for row in table:
    li...{{row}}
```

konwertowany jest do:

```html
{% for row in table %}
<li>{!{row}!}</li>
{% endfor %}"
```

---

### Jeżeli linia zanczyna się od sekwencji "===>" kolejne linie przekształcane są bez zmian aż skończy się fragment wyznaczony przez wcięcia:

blok:

```
style type=text/css===>
    .table th {
        background-color: #CEE;
    }

    body {
        margin: 5px;
        font-size: 12px;
    }

body
```

konwertowany jest do:

```html
<style type="text/css">
  .table th {
    background-color: #cee;
  }

  body {
    margin: 5px;
    font-size: 12px;
  }
</style>
<body></body>
```

---

### Jeżeli linia kończy się sekwencją '>>>', tekst przekształcany jest bez zmian aż do momentu pojawienia się sekwencji '|| |'

blok:

```
style type=text/css>>>
.table th {
    background-color: #CEE;
}

body {
margin: 5px;
font-size: 12px;
}|| |

body
```

konwertowany jest do:

```html
<style type="text/css">
  .table th {
    background-color: #cee;
  }

  body {
    margin: 5px;
    font-size: 12px;
  }
</style>
<body></body>
"""
```
