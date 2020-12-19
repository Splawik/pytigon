# Model fiels

Definiując modele danych W aplikacjach Pytigon możesz wykorzystywać wszystkie pola zdefiniowane standardowo przez Django, czyli między innymi z:

- AutoField
- BigAutoField
- BigIntegerField
- BinaryField
- BooleanField
- CharField
- DateField
- DateTimeField
- DecimalField
- DurationField
- EmailField
- FileField
- FileField
- FilePathField
- FloatField
- ImageField
- IntegerField
- GenericIPAddressField
- JSONField
- NullBooleanField
- PositiveBigIntegerField
- PositiveIntegerField
- PositiveSmallIntegerField
- SlugField
- SmallAutoField
- SmallIntegerField
- TextField
- TimeField
- URLField
- UUIDField

> module: django.db.models

Pola te są znakomicie opisane w dokumentacji Django, skoncentruję się więc wylącznie na kilku dodatkowych polach, dodanych przez system Pytigon.

## UserField

Pole to jest wykorzystywane wyłącznie w SChDevTools i służy deklaracji pola w modelu pomijając jakiekolwiek wspomganie ze strony tego narzędzia. W parametrze tego pola (self.param) podajesz pełną definicje pola np:

```python
txt = models.TextFields()
```

## PtigForeignKey GForeignKey

> module: pytigon_lib.schdjangoext.fields.PtigForeignKey

extended version of ForeignKey - additional fields: search_fields, query, is_new_button

## PtigHiddenForeignKey GHiddenForeignKey

> module: pytigon_lib.schdjangoext.fields.PtigHiddenForeignKey

ForeignKey with: field.widget = HiddenInput()

## PtigForeignKeyWidthIcon ForeignKeyWidthIcon

> module: pytigon_lib.schdjangoext.fields.PtigForeignKeyWidthIcon

If '|' in label, first part href to image, second part - label

## PtigManyToManyFieldWidthIcon ManyToManyFieldWidthIcon

> module: pytigon_lib.schdjangoext.fields.PtigManyToManyFieldWidthIcon

If '|' in label, first part href to image, second part - label
