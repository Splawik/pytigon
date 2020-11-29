# Javascript frontend

Cześcią frontend'u są WebComponents, którch integracja z Pytigon'em jest tematem oosbnego rozdziału dokumentacji.Tu zostaną opisane pozostałe moduły i ich funkcjonalnosci.

# Moduł ajax-region

## ajax elements

Moduł ajax-region zawiera kilka funkcji, które wspomagają dynamiczną zmianę zawartości strony html bez jej przeładowania. Wprowadza kilka abstrakcyjnych elementów, które nazwiemy ajax elements. Elementy te umożliwiają pobranie z serwera kodu html i umieszczanie go w zdefiniowanym przez użytkownika miejscu.

Html elements to:

1. ajax-region - jest to część strony, w którym znajduje się fragment, którego zawartość chcemy zmienić. We wfragmencie tym musi znajdować się także element inicjujący zmianę zawwartości, np butto lub form.

2. ajax-link - element generuący akcję zmiany zzawartości, najczęściej będą to elementhy a, button, form.

3. ajax-frame - element, którego zawartość zostanie zmieniona w wyniku akcji zainicjowanej przez element ajax-link

Każdy z tych elementów może także posiadać atrybut data-region określający nazwę regionu, która pozwala na definiowanie wielu niezależnych regionów nie wchodzących ze sobą w konflikt.

Na stronie elementy te zaznaczamy poprzez nadanie tagom html klas o nazwach: ajax-region, ajax-link, ajax-frame.
Np jak w tym przykładzie:

```html
<html>
  <body>
    <div class="ajax-region" data-region="test">
      <button class="ajax-link" data-region="test" />

      <div class="ajax-frame" data-region="test"></div>
    </div>
  </body>
</html>
```

Ogólną zasadą jest to że ajax-region musi zawierać wewnątrz ajax-link i ajax-frame. Te 2 z kolei elementy mogą być umieszczone dowolnie - jeden może być rodzicem drugiego lub odwrotnie. Dopuszczalne jest nałożenie tych wszysktich elementów na jeden tag jak w przykładzie:

```html
<div class="ajax-region ajax-frame ajax-link" href="/action/">
  <button href="" target="refresh_frame" />
  <div></div>
</div>
```

W kodzie powyżej po wciśnięciu przyciksku button zostanie z serwera pobrana strona html z adresu "/action/" a następnie zostanie wstawiona jako zawartość elementu div, co spowoduje autometycznie wykasowannie z tego elementu elementu button.

## funkcje modułu

---

### def register_mount_fun(fun):

rejestrowanie funkcji inicjalizującej fragment html. Fukcja fun wywoływana będzie dla każdego wstawianego kodu html do bieżącej strony, argumentem funkcji będzie kod html przetworzony do elementu DOM.

- fun(dest_elem) - rejestrowana funkcja
  - dest_elem - HTMLElement reprezentujący wstawiany kod html

---

### def mount_html(dest_elem, data_or_html, link=None):

montowanie elementu data_or_html w docelowym miejscu wskazanym przez dest_elem.
Poza zamontowaniem uruchamiane są wszystkie funkcje zarejestrowane przez register_mount_fun.
Jeżeli dest_elem posiada funkcję onloadeddata to generowane jest zdarzenie typu "loadeddata" z parametrem event z atrybutem "data", do którego przypisana jest wartość data_or_html. Gdy onloaddata nie istnieje, montowanie polega na zastąpieniu zawartości dest_elem przez wartość data_or_html. Stara zawartość jest usuwana w "inteligentny" sposób. Przed usunięciem dla wszystkich elementów klasy "call_on_remove" wywoływana jest funkcja "on_remove()".

- dest_elem - DOM element, w którym chcemy zamontować element data_or_html.

- data_or_html może być albo daną typu string zawierającą montowany kod html, albo elementem DOM reprezentujący kod html.

- link - element DOM inicjujący montowanie - element opcjonalny

---

## def get_ajax_region(element, region_name=None):

funkcja wyszukuje ajax_region, w którym element znajduje się element będący parametrem funkcji.

- element - element DOM, dla którego wyszukujemy region
- region_name - nazwa regionu, jeżeli parametr pusty - znajdowany będzie najbliższy region bez względu na jego nazwę.

---

## def get_ajax_link(element, region_name=None):

funkcja wyszukuje ajax_link znajdujący się w ajax_region wyznaczonym dla elementu będącego parametrem funkcji.

- element - element DOM, dla którego wyszukujemy ajax_link
- region_name - nazwa regionu, jeżeli parametr pusty - znajdowany będzie najbliższy region bez względu na jego nazwę.

---

## def get_ajax_frame(element, region_name=None):

funkcja wyszukuje ajax_frame znajdujący się w ajax_region wyznaczonym dla elementu będącego parametrem funkcji.

- element - element DOM, dla którego wyszukujemy ajax_frame
- region_name - nazwa regionu, jeżeli parametr pusty - znajdowany będzie najbliższy region bez względu na jego nazwę.

---

## def refresh_ajax_frame(element, region_name=None, data_element=None, callback=None):

odświeżanie zawartości elementu ajax-frame

- element - element DOM, według którego wyznaczany jest ajax-region, ajax-link i ajax-frame. Na podstawie atrybutu href, action lub src przypisanego do ajax-link wyznaczany jest adres strony internetowej, której zawarotość zostaje pobrana z serwera. Alternatywnie w przypadku gdy do funkcji przekazywany jest niepusty parametr data_element, zamiast pobierania danych z sewera on reprezentuje pobraną zawartość. Pobrana zawartość zostaje wstawiona do wyszukanego elementu ajax-frame. Wstawianie zawartości odbywa się poprzez użycie funkcji onloaddata, jeżeli ajax-frame zawiera taką funkcję lub za pomocą funkcji mount_html w przeciwnym przypadku.
- nazwa regionu, jeżeli parametr pusty - znajdowany będzie najbliższy region bez względu na jego nazwę.
- data_element - zawartość pobranej strony, jeżeli parametr ten jest pusty adres strony pobierany jest z elementu ajax-link
- callback - funkcja, która zostanie wywołana, gdy proces odświeżania zakończy się. Funkcja callback jest elementem opcjonalnym.

---

## def ajax_load(element, url, complete):

pobranie zawartości strony z adresu url i zamontowanie zawarotści w elemencie DOM "element"

- element - element DOM, w który zostanie zamontowana pobrana zawartość.

---

# Moduł events

Pytigon wprowadza znaczne modyfikacje w zakresie obsługi zdażeń związanych z obsługą zdarzeń "click" oraz "submit". Celem modyfikacji jest stworzenie strony SPA (Single-Page Application), która od strony programistycznej będzie wymagała minimalnych zmian w stosunku do aplikacji klasycznych.

Najważniejsze zmiany związane są z atrybutem "target", którego wartości zostały przedefiniowane w stosunku do standardu. Atrybut ten może przyjmować następujące wartości:

- inline - pobrana strona pokazywana jest w okienku typu inline
- inline_edit - pobrana strona pokazywana jest w okienku typu inline utworzonym wg szablonu dedokowanemu dla operacji edycji lub tworzeniu elementów
- inline_info - pobrana strona pokazywana jest w okienku typu inline utowrzonym wg szablonu dedokowanemu do pokazywania inforamcji dodatkowych
- inline_delete - pobrana strona pokazywana jest w okienku typu inline utowrzonym wg szablonu dedokowanemu dla operacji kasowania elementów
- inline_error - pobrana strona pokazywana jest w okienku typu inline utowrzonym wg szablonu dedokowanemu do pokazywania błędów

- popup - pobrana strona pokazywana jest w okienku modalnym
- popup_edit - pobrana strona pokazywana jest w okienku modalnym utowrzonym wg szablonu dedokowanemu dla operacji edycji lub tworzeniu elementów
- popup_info - pobrana strona pokazywana jest w okienku modalnym utowrzonym wg szablonu dedokowanemu do pokazywania inforamcji dodatkowych
- popup_delete - pobrana strona pokazywana jest w okienku modalnym utowrzonym wg szablonu dedokowanemu dla operacji kasowania elementów
- popup_error - pobrana strona pokazywana jest w okienku modalnym utowrzonym wg szablonu dedokowanemu do pokazywania błędów

- \_top - zamienia zawartość całego elementu <body> na pobraną zawartośćð
- \_top2 - wyświetla pobraną zawartość w specjalnym okienku aplikacji, który z definicji powinien znajdować się w górnej części ekeranu i być dostępny dla wszystkich okienek aplikacji.
- \_self - zmienia zawartość aktualnej podstorny na pobraną zawartość.
- \_parent - tworzy nową podstronę wypełniając ją pobraną zawartością.

- refresh_frame - odświeża ajax-frame - dokładny opis mechanizmu w module ajax-region
- refresh_page - odświeża aktualną podstronę - zamiennik dla \_self
- refresh_app - przeładowywuje całą aplikację

- null - pobiera stronę nie wykonując żadnej akcji na aktualnej stronie

Dla elementów inline\* pod uwagę brany jest także atrybut data-inline-position. Określa on argument insert_selector funkcji super_insert, za pomocą której nowe okienko jest wstawiane na aktualną stronę.

## funkcje modułu

---

## register_global_event(event_type, fun, selector):

rejestrowanie funkcji obsługującej zdarzenia

- event_type - for example "click"
- fun: function with parameters: (event, target_element):
- selector css selector

---

## def process_href(href, elem):

funkcja przetwarza element href zamieniając symboliczne odnośniki na zawartość elementów bieżącej strony. Odnośniki to nazwy umieszczone w podwójnych nawiasach kwadratowych - na podstawie nazw wyszukiwany jest element DOM wg nazwa a następnie pobierana jego wartość val.
Np dla href="/table/test/?val1=[[input1]]&val2=[[txt1]]
zwracana jest wartość "/table/test/?val1=test1&val2=text2" jeżeli w input1 wpisana jest wartość test1 a w elemencie txt wartość "text2"

- hef - wartość podlegająca przetworzeniu
- elem - element bazowy, na podstawie którego wyznaczany jest ajax-region, w którym wyszukiwana jest nazwa odnośnika.

---

# Moduł tabmenu

## funkcje modułu:

---

## def get_menu():

funkcja zwraca globalne menu.

- return value - zwraca obiekt klasy TabMenu:

```python
    class TabMenu:
        def on_menu_href(self, elem, data_or_html, title, title_alt=None, url=None):
        def remove_page(self, id):
```

# Moduł tools

## Dodatkowe funkcje ogólnego zastosowania:

---

## klasa Loading

```python
class Loading():
    def __init__(self, element):

    def create(self):

    def start(self):

    def set_progress(self, progress):

    def stop(self):

    def remove(self):
```

Klasa umożliwia wyświetlanie animacji symbolizującej oczekiwanie. Jeżeli do funkcji przekażemy element DOM ze zdefiniowaną klasą "ladda-button" to do tworzenia efektu oczekiwania zostanie użyta biblioteka ladda-bootstrap. W przeciwnym przypadku efekt oczekiwania realizowany będzie poprzez wyświetlenie elementu o id równym "loading-indicator". Elementym tym może być przykładowo animowany element svg lub png.

Przykladowe użycie klasy:

```python
wait_obj = Loading()
wait_obj.create()
wait_obj.start()

def callback():
    nonlocal wait_obj
    wait_obj.stop()
    wait_obj.remove()

long_running_process(callback)
```

---

## def ajax_get(url, complete, process_req=None):

funkcja pobiera dane z serwera, a następnie wywołuje funkcje complete

- url - adres strony do pobrania
- complete - funkcja wywolywana po pobraniu zawartości z serwera. Przekazywana funkcja powinna mieć jeden parametr
  - def complete(response_text):
    - response_text - pobrana strona internetowa w postaci tekstowej
- process_req - funkcja, która przed kontaktem z serwerem dodatkowo przetworzy używany do komunikacji obiekt typu XMLHttpRequest. Parametr nieobowiązkowy, domyślnie pusty. Funkcja powinna mieć jeden argument
  - def process(req):
    - req - obiekt typu XMLHttpRequest

---

## def ajax_post(url, data, complete, process_req=None):

funkcja podobna do funkcji ajax_get, z tą różnicą że komunikuje się z serwerem nie przy pomocy metody GET ale POST.
Argumenty identyczne z funkcją get z wyjątkiem jednego:

- data - słownik z parametrami przekazywanymi do metody POST

---

## def ajax_json(url, data, complete, process_req=None):

funkcja identyczna do ajax_post z tym wyjątkiem że do funkcji complete przekazywany jest obiekt powstały z dekodowania zwracanego przez serwer danych typu json.

---

## def ajax_submit(form, complete, data_filter=None, process_req=None):

funkcja przy pomocy metody POST wysyła do serwera zawartość formularza "form", po pobraniu zwrotnych danych wywołuje metodę "complete". Parametry complete i process_req identyczne jak dla funkcji ajax_post.

- form - element DOM typu form
- data_filter - funkcja, która jeżeli jest niepusta przetwarza dane formularza przed wysyłką
  - def data_filter(data):
    - data - dane formularza
    - return - przetworzone dane formularza

---

## def load_css(path, on_load = None):

dynamiczne pobranie z serwera arkusza stylów i zamontowanie go w bieżącej stronie

- path - url arkusza css
- on_load - funkcja wywoływana po pobraniu i zamontowaniu arkusza stylów, funkcja powinna mieć postać:
  - def on_load(req):
    - req - obiekt typu XMLHttpRequest, który został użyty do pobrania arkusza stylów

---

## def load_js(path, fun):

funkcja identyczna z load_css tylko zamiast arkusza stylów pobiera i montuje skrypt javascript.

---

## def load_many_js(paths, fun):

funkcja pobiera z serwera kilka skryptów i po pobraniu i zamontowaniu uruchamia funkcję fun.

- paths - tablica z url'ami do skryptów
- fun - funkcja bez parametrów uruchamiana po zamontowaniu wszystkich skryptów

---

## def send_to_dom(html_text, base_elem):

funkcja wysyła ciąg znaków do struktury bieżącej strony.

- html_text - tekst w formacie: [html][operator][selector]. Selector definiuje konstrukcję użytą do wyszukiwania elementu przez funkcję super_query_selector. Operator może przyjąć następujące wartości:

  - ===>> - umieszczenie tekstu html na końcu wyszukanego elementu
  - ===<< - umieszczzenie tekstu html na początku wyszukanego elementu
  - ===> - zamiana zawartości wyszukajnego elementu przez tekst html
  - ===) - umieszczenie tekstu html za wyszukanym elementem
  - ===( - umieszczenie tekstu html przed wyszukanym elementem

  przykładowo html_text = "Hello world!>===>>.message" będzie przetwożony w następujący sposób:
  We elemencie DOM base_element wyszukany zostanie element zawierający klasę "message". Na końcu wyszukanego elementu zostanie dopisany tekst "Hello world!".

- base_element - element DOM, od którego zacznie się wyszukiwanie elementu docelowego przy pomocy znajdującego się w html_text selector'a.

---

## def get_elem_from_string(html, selectors=None):

funkcja konwertuje tekst html na element typu DOM.

- html - tekst do skonwertowania na obiekt DOM
- selector - jeżeli niepusty ze skonwertowanego tekstu wyłuskiwany jest element wg selector'a css "selector'

---

## def is_hidden(el):

sprawdza czy element DOM el jest ukryty

---

## def is_visible(el):

sprawdza czy element DOM el jest widowczny

---

## def super_query_selector(element, selector):

Bardziej rozbudowana wersja funkcji querySelector. Parametr "selector" jest listą segmentów oddzilonych znakiem '/', dla których przeprowadzane są kolejne wyszukiwania.
Pierwsze wyszukiwanie odbywa się dla elementu "element" będącego parametrem funkcji. Dla elemetu tego wywoływana jest funkcja queyrSelector(segment) lub closest (closest w przypadku gdy segment zaczyna się od znaku '^')
Znaleziony element stanowi element startowy do następnego wyszukiwania bazującego na kolejnym segmencie selector'a. Funkcja w podbny sposób przetwarza wszystkie segmenty selektora aż do końca.

    Przykłąd 1:
    wywołanie funkcji:
        x = super_query_selector(element, ".class_name")
    jest równoważne z wywowołaniem funkcji
        x = element.querySelector(".class_name")

    Przykład2:
    wywołanie funkcji:
        x = super_query(element, "^div.frame/.message/^div")
    jest równoważne funkcjom:
        x = element.closest("div.frame")
        x = x.querySelector(".message")
        x = x.closest("div")

---

## def super_insert(base_element, insert_selector, inserted_element):

Funkcja wyszukuje element a następnie zmienia zawartość elementu docelowego.
Paremetr insert_selector składa się z 2 części oddzielonych znakiem ":"
Pierwsza część przed znakiem ":" to selektor przekazywany razem z parametrem base_element do funkcji super_query_selector.
Zwrócony przez tą funkcję element jest przetwarzany wg 2 części parametru "insert_selector".
Druga część przyjmuje następujące wartości:

- "overwrite" lub '>' - znaleziony element jest zamieniany na element "inserted_element"

- "append_first" lub '<<' - inserted_element jest wstawiany jako pierwsze dziecko dla znalezionego elementu

- "append" lub '>>' lub '' - inserted_element jest wstawiany jako ostatnie dziecko dla znalezionego dokumentu

- "after" lub ')' - wstaw inserted_element za znalezionym elementem

- "before" lub '('- wstaw inserted_elemenet za znalezionym elementem

- "class" - przepisz klasy z elementu inserted_element do znalezionego elementu

---

## def remove_element(element):

funkcja usuwa element uwzględniając specyficzne usuwanie elementów oznaczonych klasą "call_on_remove" - szczegóły opisane przy okazji funkcji mount_html.

---

## def process_resize(target_element):

Nie zawsze wymiary elementów można ustalić wyłącznie przy pomocy css, czasami konieczne jest użycie funkcji javascript. Funkcja process_resize ułatwia to zadanie.
Aby można było dynamicznie kontrolować rozmiar elementu musi on mieć przypisaną jedną z 2 klas: flexible_size lub flexible_size_round2. Dla tych elementów znajdujących się wewnątrz target_element będącego parametrem funkcji wywoływana jest jedna z trzech akcji:

1. Jeżeli obiekt posiada funkcję "process_resize" to funkcja ta jest wywoływana z parametrem zawierającym słownik z elementami określającymi położenie - opis słownika poniżej.
2. Jeżeli obiek posiada atrybut "data-size" to jest on przetwarzany przez funkcję format (standardowa funkcja języka python), która wywoływana jest z parametrem w postaci słownika, którego opis znajduje się poniżej. Tekst po sformatowaniu powinien utworzyć poprawny styl css, który jest przypisywany w kolejnym etapie do elementu.
3. Jeżeli obiekt nie spełnia warunków 1 i 2 to jest uruchamiana domyślna procedura. Dla obiektu ustawiana jest wysokość w taki sposób, że położenie górnej krawędzi obiektu nie zmienia się natomiast dolna część zbliża się do dolnej krawędzi okna przeglądarki.

słownik z elementami położenie:

- w - szerokość okna porzeglądarki
- h - wysokość okna przeglądarki
- parent_offset_x - przesunięcie w poziomie względem obiektu nadrzędnego
- parent_offset_y - przesunięcie w pionie względem obiektu nadrzędnego
- body_offset_x - przesunięcie w poziomie względem okna przeglądarki
- body_offset_y - przesunięcie w pionie wzgędem okna przeglądarki

Przykład użycia:

1. obiekt, dla którego wywoływana jest standardowa procedura, wysokość elemntu ustawiana jest tak aby dolna krawędź elementu zbliżała się do dolnej krawędzi okna przeglądarki.

```html
<div class="flexible_size"></div>
```

2. obiekt, dla którego wyliczany jest styl na podstawie atrybutu data-size

```html
<div
  class="flexible_size"
  data-size="height:calc({h}px - {body_offset_y}px); width:calc({w}px / 2);"
></div>
```
