## list

r'((?P<base*filter>[\w=*,;-]\*)/|)
(?P<filter>[\w=*,;-]\*)/
(?P<target>[\w_-]\*)/
[_]?(?P<vtype>list|sublist|tree|get|gettree|table_action)/$'

schattachements/table/Attachements//prawa**DokPrzydzielenia**{{object.id}}\_\_default/form/list/

GET: offset, sort, order, search
POST: \_FilterForm{ModelName}

- base_filter:

  - parent = int(base_filter)

- filter:

- target:

  - pdf: render pdf document
  - odf: render odf document
  - xlsx: render xlsx document
  - json: render json document
  - txt: render txt document
  - verXYZ: html, defautlt template changed to templateXYZ.html (added suffix 'XYZ')
  - default: html

- vtype:
  - list
  - sublist
  - tree
  - get
  - gettree
  - table_action: TODO - dokładny opis

context:

- title
- rel_field:
- filter: from url
- base_filter: from url
- app_name
- table_name
- form: views attribute \_FilterForm{ModelName}
- doc_tyype - from url target
- uuid - uuid.uuid4()

self.model.filter(filter)

parent = int(self.kwargs['base_filter'])
ret = ret.filter(parent=parent)

self.model.sort(ret, self.sort, self.order)
self.sort=='cid':
ret = ret.order_by('id')
ret = ret.order_by('-id')

if hasattr(self.form, 'process_empty_or_invalid'):
return self.form.process_empty_or_invalid(self.request, ret)















# add

url = r'(?P<add_param>[\w=_-]*)/add/$'

if hasattr(self.model, 'init_new'):
    if kwargs['add_param'] and kwargs['add_param'] != '-':
        self.init_form = self.object.init_new(request, self, kwargs['add_param'])
    else:
        self.init_form = self.object.init_new(request, self)


if self.object and hasattr(self.object, 'get_form_class'):
    self.form_class = self.object.get_form_class(self, request, True)

