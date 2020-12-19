# Template tags

W szablonach aplikacji Pytigon możesz korzystać ze wszystkich elementów tag systemu Django.
Dokumentację znajddziesz pod adresem:

https://docs.djangoproject.com/en/dev/ref/templates/builtins/

Dodatkowo Pytigon wprowadza szereg nowych tagów, rozszerzających możliwości systemu.

## Actions

---

### row_actions

---

dla bierzącego wiersza tag generuje serię przycisków, jeden przycisk przypisany do jednej akcji.

Zapis akcji może odbywać cię w 2 układach - elementów rozdzielonych średnikiem lub elementów rozdzielonych znakiem nowego wiersza, tak jak w przykładzie:

```
{% row_actions %}
    action1,Action 1,,,test;action2;action3
{% endrow_actions %}

{% row_actions %}
    action1,Action 1,,,test
    action2
    action3
{% endrow_actions %}

{% row_actions %}
    action1,title=Action 1,tag_class=test
    action2
    action3
{% endrow_actions %}

```

Akcja składa się z kilku elementów oddzielonych znakiem ','. Kolejne elementy oznaczają:

> action,title,icon_name,target,attrs,class,url

Tylko pierwszy element jest obowiązkowy, kolejne są opcjonalne.

- action: napis w formacie "action-second_action/x1/x2/x3"
  > możesz tworzayć akcję złożoną z kilku akcji prostych, kolejne człony oddzielasz myślnikami.
      Parametry x1, x2, x3 zostają przekazane jako parametry GET akcji, jednocześnie przekazywane są do szablonu skojarzonego z akcją jako parametry x1, x2 i x3
- title
- icon_name - icon in format
- target - nadpisuje domyślny parametr target akcji
- attrs - nadpisuje domyślne atrybuty akcji
- tag_class - nadpisuje domyślną klasę akcji
- url - nadpisuje domyślny url akcji

Do szablonu skojarzonego z akcją zostają przekazane następujące parametry:

- path - request.path
- bp - base_path
- app - app_path
- tp - table_path
- tpf - table_path_and_filter
- table_name - table name
- id - row id
- object_name - object name
- child_tab - True if table is subtable

zdefiniowane akcje:

- default: url={ap}table/{table_name}/{id}/action/{action}/
- action: target=inline_edit
- new_row:
- edit: url={tp}{id}/edit/
- edit2: url={tp}{id}/edit2/
- delete: url={tp}{id}/delete/
- delete2: url={tp}{id}/delete2/
- field_list: url={ap}table/{object_name}/{id}/{x1}/-/form/sublist/
- field_list_get: url={ap}{object_name}/{id}/{x1}/-/form/get/
- field_action: url={ap}{object_name}/{id}/{x1}/-/form/sublist/
- field_edit: url={ap}table/{object_name}/{id}/{x1}/py/editor/
- any_field_edit: {app_path}table/{object_name}/{id}/{x1}/{x2}/editor/
- print: target=\_blank
- template_edit: icon=client://mimetypes/x-office-presentation.png
- pdf: target=\_bank, url={tp}{id}/pdf/view/
- odf: url={tp}{id}/odf/view/
- xlsx: url={tp}{id}/xlsx/view/
- null: target=null
- inline: target=inline_edit
- popup: target=popup_edit
- popup_edit: target=popup_edit
- popup_info: target=popup_info
- popup_delete: target=popup_delete
- refresh_frame: target=refresh_frame
- top: target=\_top

---

### action

---

default action - see row_actions description

```python
@inclusion_tag('widgets/action.html')
def action(context, action, title = "", icon_name = "", target = "", attrs = "", tag_class = "", url = ""):
    ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url)
    return ret
```

---

### view_row

---

> def view_row(context, title = "", icon_name = "", target = "popup_info", attrs = "", tag_class = "", url = "")

shortcut for: action="view_row", url="{tp}%s/\*/view/"

---

### get_row

---

> def get_row(context, title = "", icon_name = "", target = "", attrs = "", tag_class = "", url = "")

shortcut for: action="get"

---

### button

---

> def button(context, title = "", icon_name = "", target = "", attrs = "", tag_class = "", url = "")

shortcut for: action="button"

---

### new_row

---

> def new_row(context, title="", icon_name="", target='', attrs='', tag_class='', url="", action="new_row/-"):

shortcut for: action="new_row/-"

---

### new_row_inline

---

> def new_row_inline(context, title="", icon_name="", target='', attrs='', tag_class='', url="", action="new_row-inline/-")

---

### list_action

---

> def list_action(context, action, title="", icon_name="", target='\_parent', attrs='', tag_class="", url="", active=False)

shortcut for

---

### wiki_link

---

> def wiki_link(context, subject, wiki_description, icon_name="", target='\_self', attrs="", tag_class="", url=""):

shortcut for: action="wiki", url="/schwiki/%s/%s/view/"

## form tags

---

### form

---

Show default form. Zawartość tag'a zawiera listę pól formularza oraz jego parametry.
Zawartość powinna posiadać następujący układ:

> field1,field2,field3:field_format/group_format/addon_format

- field1,field2... - jest to lista pól formularza django oddzielona przecinkami
- field_format - pole określa format każdego z pól formularza. Format ten określony jest przy pomocy klas biblioteki css: Bootstrap. Do zrozumienia znaczenie field_format musisz przynajmniej pobierznie zapoznać się z dokumentacją biblioteki a szczególnie z częścią zatytułowaną Bootstrap Layout. Pole field_format może występować w kilku wariantach:
  - "!" - w tym przypadku pola formularza i ich etykiety są ukryte,
  - "^" - pole pełnej szerokości (Bootstrap col-12 class), label oznaczona klasą label-floating
  - "-" - pole pełnej szerokości (Bootstrap col-12 class), label oznaczona klasą label-over-field
  - "" (wartość pusta) - pole pełnej szerokości (Bootstrap col-12 class), brak label
  - "x:y:z" - x,y,z wartości typu integer, które zostają rozwinięte do klas przypisanych do pól formólarza wg schematu: "col-sm-x col-md-y col-lg-z" (patrz Bootstrap layout). Dla elementów label automatycznie zostają wyliczone klasy, które pozwalają umieścić to pole obok pola formularzu aby razem dawały pełną szerokość 12. Jeżeli pole x,y lub z przyjmuje wartość 12 to dla pola label też jest przypisywana szerokość 12 - co powoduje że label zajmuje całą linie a pole formularza przenoszone jest do kolejnego wiersza, który także wypełniony zostaje w pełnej szerokości.
- group_format - pole określające szerokość całej grupy pól - występuje w 2 wariantach:
  - "x:y:z" - określenie klas col-sm-x, col-md-y, col-lg-z analogicznie jak w poprzednim punkcie, tylko tym razem klasy zostają przypisane do elementu form-group.
  - "x" - skrócona wersja dla "x:x:x"
- addon_format - pole może występować w kilku wariantach:
  - (-X)text - append button with text after field
  - (X-)text - insert button with text before field
  - (-x)text - append text after field
  - (x-)text - insert text before field

```python
% form:
    .parent,description,payment,account_state:12:3:3/12:12:12/(-X)abc
```

### field

Show form field. Zawartość tag'a zawiera definicję pola w formacie:

```
% field field_object field_format/group_format/addon_format
```

- field_object: field name (in context exists 'form' with django Form object) or form field
- field_format/group_format/addon_format - opisane w poprzednim punkcie

---

### vert_form

---

Form with default field_format = "^/12"

---

### inline_form

---

Form with default field_format = "^/"

---

### col2_form

---

Form with default field_format = "^/12:6:6"

---

### form_item

---

```
    % form_item field_name:
        ...
```

Tag form_item pozwala na umieszczenie na stronie html pola formularza o nazwie field_name zdefiniowanego w formularzu przekazanym do szablonu jako zmienna form. Użytkownik może zmienić zawartość pola nie martwiąc się o prawidłowe przypisanie klas i atrybutow.

Przykład:

```
% form_item rel_to:
    select name=choices,,,id=id_choices,,,class=select form-control
        %if not object.choices or object.choices == ""
            option selected=selected,,,value=...---------
        %else
            option value=...---------
        %for choice in object.parent.parent.schchoice_set.all
            %if choice.name == object.choices
                option value={{choice.name}},,,selected=selected...{{choice.name}}
            %else
                option value={{choice.name}}...{{choice.name}}
```

---

### get_table_row

---

> def get_table_row(context, field_or_name, prj=None, app_name=None, table_name=None, search_fields=None, filter=None, label = None, initial = None, is_get_button=True, is_new_button=False, get_target="popup_edit", new_target="inline")

- field_or_name - field name (from var form) or form object.
- prj - project
- app_name - django application name
- table_name - django model name
- search_fields - wyrażenie, które może być użyte przez funkcję queryset.filter
- filter
- label
- initial
- is_get_button
- is_new_button
- get_target

Example:

```
% get_table_row "wikiobj_id" "schwiki" "wiki" "PageObjectsConf" "name__icontains" label="Type of wiki object" filter="1" is_get_button=True

```

## include tags

---

### frame

---

> def frame(context, href, height)

- href - source of frame
- height - height attribute of div frame

---

### module_link

---

> def module_link(context, href)

- href - module link destination

---

### jscript_link

---

> def jscript_link(context, href)

- href - javascript link destination

---

### css_link

---

> def css_link(context, href)

- href - css link destination

---

### link

---

> def link(context, href, rel, typ)

- href - location of the linked document
- rel - specifies the relationship between the current document and the linked document
- typ - specifies the media type of the linked document

see: https://www.w3schools.com/tags/tag_link.asp

---

### component

---

> def component(context, href)

- href - module link destination

## other tags

---

### spec

--

> def spec(format)

```python
def spec(format):
    return format.replace('{', '{{').replace('}', '}}').replace('[', '{%').replace(']', '%}')
```

---

### markdown2html

---

Convert markdown_str from markdown format to html.

> def markdown2html (context, markdown_str, path=None, section = None)

- markdown_str - string in markdown format
- path - base path of wiki page
- section - section of wiki page

---

### subtemplate

---

Render template from string: template_string

> def subtemplate(context, template_string)

- template_string - source string with template

---

### editable

---

> def editable(context, name, title="", url=None)

- name - name of field
- title - popup window title
- url - see x-editable documentaction

---

### td_editable

---

> def td_editable(context, name, title="")

- name - name of edited column
- title - popup window title

---

### svg_standard_style

---

Insert standard css styles for svg.

> def svg_standard_style(context,)

Example:

```
===>
    <svg
        width="100%"
        viewBox="0 0 210 297"
        version="1.1"
        id="svg8">
        <style>
            {% svg_standard_style %}
            #path4520:hover {
                fill:#f00 !important;
                stroke: orange !important;
                stroke-width: 1 !important;
                rx: 22px !important;
                ry: 22px !important;
                cursor: pointer;
            }
        </style>
    </svg>
```
