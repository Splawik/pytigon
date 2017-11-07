import django.forms.widgets

class ImgFileInput(django.forms.widgets.ClearableFileInput):
    def format_value(self, value):
        return value

    def value_from_datadict(self, data, files, name):
        if name in data:
            return  data[name]
        elif name in files:
            return files[name]
        else:
            return None

