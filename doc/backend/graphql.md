# GraphQL

Serwer Pytigon'a zintegrowany jest językiem zapytań GraphQL. Język ten jest udostępniony pod dwoma adresami:

- /grapql/ - interfejs prywatny, dostęp tylko dla zalogowanych użytkownikóœ
- /graphql_public/ - interfejs publiczny

## JWT

Interfejs publiczny udostępnia możliwość autoryzacji aplikacji klienta za pomocą standardu JWT. Poniżej przykłąd krótkiego skryptu pobierającego klucz

```python

import httpx

GET_TOKEN_QUERY = """mutation {
  tokenAuth(
    username: "username",
    password: "user_password"
  ) {
    token
  }
}"""



r = httpx.post("https://pytigon_site/graphql_public/", json={"query": GET_TOKEN_QUERY})
print(r.status_code)
print(r.text)

```

## Generowanie zapytań

Po pobraniu tokena można za jego pomocą uzyskać dostęp do API prywatnego oraz do wszystkich zasobów strony dostępnych dla użytkownika, za pomocą którego danych został pobrany token.

```python

import httpx

AUTH = {
    "data": {
        "tokenAuth": {
            "token": "eyJ0 ... token from sample 1"
        }
    }
}


r = httpx.get(
    "https://pytigon_site/",
    headers={"Authorization": "JWT " + AUTH["data"]["tokenAuth"]["token"]},
)

print(r.status_code)
print(r.text)


```

Standardowo przez GraphQL mamy dostęp do wszystkich tabel zdefiniowanych w aplikacji Pytigon. Gdy tworzymy aplikację pytigon przy pomocy narzędzia SChDevTools, w projekcie automatycznie pojawia się plik schema.py z domyślną implementacją API GraphQL'a. Możemy oczywiście go rozszerzać w niczym nieograniczonym zakresie.
Jeżeli chcemy filtrować dane w tabelach musimy zdefiniować wg jakich kolumn i w jaki sposób chcemy to robić.
Standardowym sposobem defionowania filtrów na potrzeby GraphQL jst zdefiniowanie pola: filter_fields w modelu tabeli.
Np:

plik models.py

```python
...

class TestModel(models.Model):

    ...
    filter_fields = {
        'name': ['exact', 'icontains', 'istartswith'],

    ...
...

```

## Integracja GraphQL i Select2

GraphQL służy głównie do tworzenia API dla aplikacji zewnętrznych, które chcemy zintegrować z Pytigon'em. Pytigon wykorzystuje jednak ten język także wewnętrznie. Elementem wykorzystującycm GraphQL jest web component:
ptig-select2.

Komponent ptig-select2 służy do wybierania danych spośród listy dospnych opcji. Bazuje on na bibliotece select2 napisanej w javascript. Select2 potrafi integrować się ze zdalnym źródłem danych. W przypadku aplikacji Pytigon źródłem tym jest GraphQL.

Przykład użycia komponentu na stronie html:

```html
<ptig-select2
  width="300px"
  href="{{base_path}}schwiki/table/PageObjectsConf/-/form/get/"
  target="_popup"
>
  graphql { schwiki_Pageobjectsconfall(name_Istartswith: "$$$") { edges { node {
  id, text:name }}} }
</ptig-select2>
```

W tag'u ptig-select2 umieszczamy zapytanie w języku GraphQL, znak $$$ zastępowany jest automatycznie poprzez zawartość wprowadzoną w polu selelct2.

Do komponentu możemy przekazać parametr href. Jeżeli jest on niiepusty powinien zawierać adres formularza, który posłuży na wybranie elementu z listy w sposób bardziej rozbudowany niż standardowy popup kontrolki select2.
W naszym przykładzie podany jest adres wyświetlający tabelę PageObjectConf, w której dokonać wyboru elementu.
