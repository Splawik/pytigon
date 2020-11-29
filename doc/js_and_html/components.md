# Komponenty

Jedną z architektur, którą wspiera Pytigon jest klient WEB. Możesz korzystać w swoich projektach z dowolnych technologii webowych wliczając w to: react.js, vue.js.
Pytigon szczególnie wspiera jednak następujące technologie: html, css oraz webcomponents. Do każdej z tych technologii Pytigon dodaje swoje własne rozwiązania pozwalające na maksymalne ujednolicenie tych składników.

1. html - dodany nowy format prezentacji dokumentu html. Jest to ihtml - format, który upraszcza obsługę znaczników html a jednocześnie jest kompilowany do standardowego formatu html.
2. css - tutaj korzystamy z języka sass, który pozwala na tworzenie arkuszy stylów wykorzystując bardziej czytelną składnię, które są następnie kompilowane do czystego kodu css.
3. Webcomponents - Pytigon dodaje cienką warstwę abstrakcji, która pozwala na tworzenie komponentów w twoim ulubionym języku Python.

Ihtml, sass oraz webcomponents tworzone w języku Python dzielą tą samą filozowię: po pierwsze czytelność kodu. Zdaniem autora kod języka Python jest zdecydowanie bardziej czytelny niż kod w JavaScript.
Kod ihtml, wykorzystujący wcięcia do kontroli zasięgu znaczników - zmniejsza ilość kodu, zwiększa czytelność. To samo dotyczy języka sass, który zastępuje nawiasy klamrowe wcięciami - podobnie jak Python.

Poniżej znajduje się struktura przykładoweg komopnentu Pytigon'a. Po jego utworzeniu możesz go użyć na stronie html jako znacznik: <test-component></test-component> lub zapisując to w ihtml:
test-component

kod przykładowego komponentu:

```python
TAG = 'ptig-test'

TEMPLATE = """
div
    a data-bind=href:href
    p...Hello world!
    p data-bind=text
    button data-bind=onclick:onclick
"""

BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins'
js_libs = [BASE_PATH + '/test.js', BASE_PATH + '/test2.js']
css_libs = [BASE_PATH + '/test.css']

with DefineWebComponent(TAG, False, js_libs, css_libs) as comp:

    def width(new_value, old_value, component):
        component.root.style.width = new_value

    def height(new_value, old_value, component):
        component.root.style.height = new_value

    comp.options['attributes'] = {
        "width": width,
        "height": height,
        "href" : None,
    }

    comp.options['template'] = TEMPLATE

    @comp.fun("constructor")
    def constructor(component):
        pass

    @comp.fun("init")
    def init(component):
        def onclick(event):
            print("onclick:)

        component.set_state({"onclick": onclick})
        print(component.root)

    @comp.fun("connectedCallback")
    def connectedCallback(component):
        pass

    @comp.fun("disconnectedCallback")
    def disconnectedCallback(component):
        pass

    #@comp.fun("attributeChangedCallback")
    #def attributeChangedCallback(component):
    #    pass
```

Jak to działa?

Głównym elementem definiującym webcomponent jest klasa DefineWebComponent. Właściwe zdefiniowanie komponentu następuje w funkcji close obiektu tej klasy. Aby tak się mogło stać musimy wcześniej zadeklarować różnego rodzaju właściwości. Obiekt obsługuje "context management protocol" - w przykładzie powyżej wykorzystano tą cechę. W bloku "with" tworzymy nowy obiekt klasy DefineWebComponent, na końcu tego bloku automatycznie wywoływana jest funkcja close definiując tym WebComponent (następuje wywołanie standardowej funkcji standardu WebComponents: customElements.define).

DefineWebComponent wywoływany jest z 4 parametrami, z których tylko pierwszy jest obowiązkowy.

DefineWebComponent(tag , shadow=False, js=None, css=None):

- tag - tag name of an element
- shadow - czy używać shadow DOM
- js - lista bibliotek javascript, które powinny zostać załadowane przed utworzeniem komponentu
- css - lista arkuszy stylu, które powinny zostać załadowane przed uruchomieniem komponentu

Resztę parametrów uzupełniamy definiując kolejne elementy słownika: DefineWebComponents.options

options:

- template - szablon komponentu
- attributes - dict z pozycjami:
  key - nazwa atrybutu przekazywana do komonentu
  value - Jeżeli Null - automatycznie przetwarzanie poprzez funkcję set_state({ key: value })
  Jeżeli not Null - nazwa funkcji wywoływanej z parametrami: new_value, old_value, component
- constructor - funkcja wywoływana z parametrem: komponent, jest uruchamiana z konstruktora obiektu HTMLElement.
- init - funkcja wywoływana z parametrem: komponent. Jeżeli komponent uruchamiany był z opcją "shadow" funckcja wywoływana jest z konstruktora obiektu HTMLElement, w przeciwnym przypadku funkcja uruchamiana jest z metody "connectedCallback" obkiektu HTMLElement. Funkcja jest dobrym miejscem na inicjowanie twojego komponentu. Zmienna component.root zawiera element bazowy komponentu: dla opcji z shadow DOM jest to element shado DOM, w przeciwnym przypadku komponent.root wskazuje na komponent.
- connectCallback - funkcja wywoływana z parametrem komponent, uruchamiana przez funkcję o tej samej nazwie obiektu HTMLElement
- disconnectedCallback - funkcja wywoływana z parametrem komponent, uruchamiana przez funkcję o tej samej nazwie obiektu HTMLElement

Data binding:
komponent utworzony za pomocą DefineWebComponent posiada funkcję:
set_state(dict)

Zawartość słownika mapowana jest na zdefiniowane w TEMPLATE elementy z atrybutem data-bind.

Składnia atrybutu data-bind:

- data-bind="key" - ustawia zawartość elementu (innerHtml) na wartość komponent.state[key]
- data-bind="attribute:key" - ustawia atrybut elementu o nazwie "attribute" na wartość komponent.state[key] poprzez bezpośrednie przypisanie wartości do atrybutu obiektu
- data-bind="attr-attirbute:key" - ustawia atrybut elementu o nazwie "attribute" na wartość komponent.state[key] za pomocą funkcji setAttribute
- data-bind="style-name:key" - ustawia element stylu o nazwie name na wartość komponent.state[key]
- data-bind="class-name:key" - Jeżeli komponent.state[key] - dodaje klasę name do obiektu. Usuwa klasę name z obiektu jeżeli !komponent.state[key]
- data-bind=":key" jest równoważne data-bind="key:key"
- data-bind="[attribute:][mod]key" - jeżeli walue poprzedzone jest znakiem przedrostka ze zbioru:
  "!", "?", "\_", "0", "+", "-", "%" - wartość komponent.state[key] jest odpowiednio przetwarzana; - ! - !komponent.state[key] - ? - bool(komponent.state[key]) - \* - str(komponent.state[key]) - \+ - float(komponent.state[key]) - \- (-1) \* float(komponent.state[key]) - % - float(value)/100
