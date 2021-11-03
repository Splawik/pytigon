FIELD_LIST_TEMPLATE = """field_list/{{choice.0}},{{choice.1}}{% if choice.2 or choice.3 %},icon_name={{choice.2}}{% if choice.3 %}/{{choice.3}}{% endif %}{% endif %}{% if choice.4 %},target='{{choice.4}}'{% endif %}"""
FIELD_EDIT_TEMPLATE = """field_edit/{{choice.0}},{{choice.1}}{% if choice.2%},icon_name={{choice.2}}{% endif %}{% if choice.3 %}/{{choice.3}}{% endif %}{% if choice.4 %},target='{{choice.4}}'{% endif %}"""
VIEW_ROW_TEMPLATE = """%view_row object{% if choice.1%},icon_name={{choice.1}}{% endif %}{% if choice.2 %}/{{choice.2}}{% endif % }"""
NEW_ROW_TEMPLATE = """% {% if choice.1 == 'NO'%}new_row{% else %}new_row_inline{% endif %} {% choice.0 %}{% if choice.2%},icon_name={{choice.2}}{% endif %}{% if choice.3 %}/{{choice.3}}{% endif %}"""
ACTION_TEMPLATE = """action {{choice.0}}{% if choice.1 %},title={{ choice.1 }}{%endif%}{% if choice.2 %},icon_name={{ choice.2 }}{%endif%}{% if choice.3 %},target={{ choice.3 }}{%endif%}{% if choice.4 %},attrs={{ choice.4 }}{%endif%}{% if choice.5 %},tag_class={{ choice.5 }}{%endif%}{% if choice.6 %},url={{ choice.6 }}{%endif%}"""
ROW_RELATED_LIST_TEMPLATE = """% row_related_list "{{choice.0}}" title="{{choice.1}}" filter="{{choice.2}}"{% if choice.3 %} icon_name="{{ choice.3 }}"{% endif %}"""

ALL_TEMPLATE ="""
%% all
    % with {% if choice.0 %}title='{{choice.0}}{% endif %} {% if choice.1 %}table_type='{{choice.1}}'{% endif %} {% if choice.2 %}form_width={{choice.2}}{% endif %} {% if choice.3 %}form_height={{choice.3}}{% endif %}:
        {{ block.super }}
"""

LIST_ROW_ATTR_TEMPLATE = """
%% list_row_attr
    {% templatetag openblock %} if object.<<condition>> {% templatetag closeblock %}class=danger{% templatetag openblock %} endif {% templatetag closeblock %}
"""

ID_EXTRA_TEMPLATE = """
%% id_extra
    % list_sublist app="" table_name="" filter="" title="" icon_name="fa fa-lg fa-caret-down" target="" attrs="" tag_class="" url="" action="field_list"
    {{ block.super }}
"""

DIALOG_TYPE_TEMPLATE = """
%% dialog_type
    .{{choice.0}}
"""

SCROLL_TEMPLATE = """
%% scroll
"""

PYTHONCODE_TEMPLATE = """
%% pythoncode
    script language=python
        def signal_from_child(self, child, signal):
            if signal=='set_bitmap_list':
                bitmaps = {
                    "<<name1>>": "<<image_path1>>",
                }
                child.set_bitmaps(bitmaps)

        def filter_url(self, target, href):
            return href
"""

MOVE_ROWS_TEMPLATE = """
% if not forloop.first:
    % row_actions:...field_up,Move up
% if not forloop.last:
    % row_actions:...field_down,Move down
"""

ACTIONS =  {
    'form': {
        'template': """% form:""",
    },
    'two_columns_form': {
        'template': """% form "^/12:6:6":""",
    },
    'three_columns_form': {
        'template': """% form "^/12:4:4":""",
    },
    'advanced_form': {
        'title': 'Field parameters',
        'choices': [
            {'title': 'default label format [sm:md:lg]', 'values': [ '^', '12:12:12', '12:3:3', '12:4:4', '12:6:6']},
            {'title': 'default field format [sm:md:lg]', 'values': [ '12:12:12', '12:6:6', '12:4:4', '12:3:3', '12:1:1']},
        ],
        'template':  """% form {% choice.0 %}/{% choice.1 %}:""",
    },
    'form_field': {
        'title': 'Field parameters',
        'choices': [
            {'title': 'name', 'values': [], 'source_of_values': 'object_fields'},
            {'title': 'hidden', 'values': [ 'NO', 'YES'],},
        ],
        'template': """{{choice.0}}{% if choice.1=="YES" %}:!{% endif %}""",
    },
    'field': {
        'title': 'Field parameters',
        'choices': [
            {'title': 'name', 'values': [], 'source_of_values': 'object_fields'},
            {'title': 'label format [sm:md:lg]', 'values': [ '^', '12:12:12', '12:3:3', '12:4:4', '12:6:6']},
            {'title': 'field format [sm:md:lg]', 'values': [ '12:12:12', '12:6:6', '12:4:4', '12:3:3', '12:1:1']},
        ],
        'template': """% form {{choice.0}} {{choice.1 }}/{{ choice.2 }}""",
    },
    'field_list': {
        'title': 'Field parameters',
        'choices': [
            {'title': 'related field name', 'values': [], 'source_of_values': 'relfields'},
            {'title': 'title', 'values': []},
            {'title': 'button icon name', 'values': []},
            {'title': 'list icon name', 'values': []},
            {'title': 'target', 'values': ['_inline', '_parent', 'popup',] },
        ],
        'template': FIELD_LIST_TEMPLATE,
    },
    'field_edit': {
        'title': 'Field parameters',
        'choices': [
            {'title': 'edited field name', 'values': [], 'source_of_values': 'txtfields'},
            {'title': 'title', 'values': []},
            {'title': 'button icon name', 'values': []},
            {'title': 'list icon name', 'values': []},
            {'title': 'target', 'values': ['_parent', '_inline', 'popup',] },
        ],
        'template': FIELD_EDIT_TEMPLATE,
    },
    'action': {
        'title': 'Action parameters',
        'choices': [
            {'title': 'action', 'values': []},
            {'title': 'title', 'values': []},
            {'title': 'button icon name', 'values': []},
            {'title': 'list icon name', 'values': []},
            {'title': 'target', 'values': ["_blank", "_parent", "_top", "_self", "popup", "popup_edit", "popup_info", "popup_delete", "inline_edit", "inline_info", "inline_delete", "inline", "none", "refresh_obj", "refresh_page", "refresh_app",]},
            {'title': 'attrs', 'values': [ "+disabled='disabled'", "data-inline-position='^tr:after'"] },
            {'title': 'tag_class', 'values': ['+btn-danger', '+<<class1>> <<class2>>', '<<class>>',]},
            {'title': 'url', 'values': []},
        ],
        'template': ACTION_TEMPLATE,
    },
    'row_related_list': {
        'title': 'Action parameters',
        'choices': [
            {'title': 'application/table', 'values': [], 'source_of_values': 'tables'},
            {'title': 'title', 'values': []},
            {'title': 'filter', 'values': []},
            {'title': 'icon name', 'values': []},
        ],
        'template': ROW_RELATED_LIST_TEMPLATE,
    },
    'view_row': {
        'title': 'Parameters',
        'choices': [
            {'title': 'title', 'values': []},
            {'title': 'button icon name', 'values': []},
            {'title': 'list icon name', 'values': []},
        ],
        'template': VIEW_ROW_TEMPLATE,
    },
    'new_row': {
        'title': 'Parameters',
        'choices': [
            {'title': 'title', 'values': [], },
            {'title': 'inline', 'values': ['NO', 'YES'], },
            {'title': 'button icon name', 'values': []},
            {'title': 'list icon name', 'values': []},
        ],
        'template': NEW_ROW_TEMPLATE,
    },
    'list_action': {
        'title': 'Parameters',
        'choices': [
            {'title': 'title', 'values': [], },
            {'title': 'inline', 'values': ['NO', 'YES'], },
            {'title': 'button icon name', 'values': []},
            {'title': 'list icon name', 'values': []},
        ],
        'template': NEW_ROW_TEMPLATE,
    },
    'permision': {
       'title': 'Parameters',
       'choices': [
           {'title': 'application/permission', 'values': [], 'source_of_values': 'permissions'},
       ],
       'template': """ perms.{{choice.0}} """,
    },
    'user_in_group': {
       'title': 'Parameters',
       'choices': [
           {'title': 'group', 'values': []},
       ],
       'template': """request.user|user_in_group:'{{choice.0}}'""",
    },
    'all': {
        'title': 'Block parameters',
        'choices': [
            { 'title': 'title', 'values': [] },
            { 'title': 'table type', 'values': [ 'datatable',] },
            { 'title': 'form width', 'values': [] },
            { 'title': 'form height', 'values': [] },
        ],
        'template': ALL_TEMPLATE,
    },
    'list_row_attr': {
        'template': LIST_ROW_ATTR_TEMPLATE,
    },
    'id_extra': {
        'template': ID_EXTRA_TEMPLATE,
    },
    'dialog_type': {
        'title': 'Block parameters',
        'choices': [
            {'title': 'type', 'values': [ 'modal-lg', 'modal-sm', ]},
        ],
        'template': DIALOG_TYPE_TEMPLATE,
    },
    'scroll': {
        'template': SCROLL_TEMPLATE,
    },
    'pythoncode': {
        'template': PYTHONCODE_TEMPLATE,
    },
    'move_rows': {
        'template': MOVE_ROWS_TEMPLATE,
    },
}
