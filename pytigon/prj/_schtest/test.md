Moduł zawiera uniwersalne typy danych, na bazie których możesz zbudować system za pomocą możesz tworzyć dokumenty elektroniczne,
linijki dokumentów oraz przeprowadzać operacje na kontach księgowych.
Elementem operacji na kontach jest uniwersalny typ Element. Może on reprezentować klienta, dostawcę, materiał, towar itp.


Element
Element pozwala na tworzenie drzewa reprezentującego skomplikowane struktury danhych. Przykładowa struktura jaką możesz utworzyć w swoim programie:


- Firma
    - Działy w firmie
        - Dział 1
            - operator 1
            - operator 2
        - Dział 2
            - operator 1
            - operator 2
    - Wyroby
        - wyrób 1
        - wyrób 2
        ... 
        - wyrob n
    - Waluty
        - PLN
        - USD
        - PLN


Każdy element posiada element nadrzędny (pole parent) oraz do 4 dodatkowych elementów nadrzędnych
grand_parent1, ..., grand_parent4 


w obiektach podrzędnych możesz przedefiniować metodę get_element_queryset, która filtruje spośród wszystkich elementów tylko te dostępne. 

def get_element_queryset():
    return None

schelements_models.GET_ELEMENT_QUERYSET.set_function(get_element_queryset)


- DocReg
    - DocType
        - DocHead
            - DocItem
    - DocRegStatus
        - DocHeadStatus <- DocHead
- Account
    - AccountState
        - AccountOperation <- DocItem


Przykładowe użycie modułu schelements we własnej aplikacji:

1. Dostosuj model Element do własnych potrzeb:

class YourAppElement:
    @staticmethod
    def get_structure():
        ret = {
            "ROOT": {"next": ["O-COM", "I-GRP"]},
            "O-COM": {
                "next": [
                    "O-EMP",
                ],
                "title": "Your company",
                "table": "YourCompanyTable",
            },
            "O-EMP": {
                "title": "Administrator",
                "table": "Administrator",
            },
            "I-GRP": {
                "title": "Group of items",
                "table": "IGroup",
                "next": [
                    "I-INT",
                ],
            },
            "I-INT": {
                "title": "Item",
                "table": "YourItem",
            },
        }
        for pos in ret:
            ret[pos]["app"] = "yourapp"
            if "next" in ret[pos]:
                ret[pos]["next"].append("O-GRP")
        return ret

extend_class(schelements_models.Element, YourAppElement)


Szczególno rolę odgrywa funkcja get_structure. Dla każdego typu elementu, który chcemy wykorzystać w naszej aplikacji należy zdefiniować dedykowany model dziedziczący po Element (patrz punkt 2 poniżej). Pozycja zwracanego słownika (dict) musi zawierać: 
- app: nazwę aplikacji, w której zdefiniowany jest model
- table - nazwa modelu
- title - Opis modelu

Dodatkowo element słownika może zawierać pole:
- next: typ elementu który może może zostać dodany jako potomek elementu.

2. Dodaj modele dziedziczące po Element:

class IGroup(Element):
    class Meta:
        verbose_name = _("Item group")
        verbose_name_plural = _("Item groups")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "yourapp"

        ordering = ["id"]

        proxy = True

admin.site.register(IGroup)

...

class Administrator(Element):
    class Meta:
        verbose_name = _("Administrator")
        verbose_name_plural = _("Administrators")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "yourapp"

        ordering = ["id"]

    email = models.EmailField(
        "Email",
        null=False,
        blank=False,
        editable=True,
        unique=True,
    )

    def save(self, *argi, **argv):
        super().save(*argi, **argv)

        x = self.name.split(" ", 1)
        if len(x) > 1:
            name = x[0]
            surname = x[1]
        else:
            name = ""
            surname = x
        add_user(self, surname, name, self.email.lower(), "ADMINISTRATOR")


admin.site.register(Administrator)


Jeżeli w modelu dziedziczącym nie potrzebujesz dodatkowych pól, dodaj parametr proxy = True do klasy Meta (tak jak w pierwszym modelu). W przeciwnym przypadku pomiń ten parametr (patrz drugi model).


3. Dodaj obsługę uprawnień do elementów:

def get_element_queryset():
    request = get_request()
    if request:
        if request.user.is_superuser:
            return None
        elif (
            hasattr(request.user, "profile")
            and request.user.profile
            and request.user.profile.owner
        ):
            return Q(first_ancestor=request.user.profile.owner.first_ancestor)
    return Q(pk=0)

schelements_models.GET_ELEMENT_QUERYSET.set_function(get_element_queryset)


4. W aplikacji w "Document register" rejestry dokumentów, do działania niezbędne jest wypełnienie pól:
   name i description 

5. Dla każdej pozycji w rejestrze musisz utworzyć 2 modele o nazwach:
   1. nazwa_rejestru + 'DocHead', który dziedziczy po modelu DocHead
   2. nazwa_rejestru + 'DocItem', który dziedziczy po modelu DocItem
   W modelach tych możesz definiować dodatkowe pola wymagade dla nagłówka dokumentu w rejestrze i linijek dokumentów.

6. Dla każdego rejestru dodaj typy dokumentów. Tak jak w przypadku Rejestru dokumentów obowiązkowe pola to: name i description.

7. Dla każdego rejestru dodaj statusy. 









