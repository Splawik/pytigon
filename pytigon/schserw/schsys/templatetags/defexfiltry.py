"""Module contains filters which are automatically loaded."""

from django import template

register = template.Library()


@register.filter(name="translate")
def translate(s, lng):
    """Translate template name based on language.

    Args:
        s (str): Name to convert.
        lng (str): Two-letter language code.

    Returns:
        str: Translated template name.
    """
    if not isinstance(s, str) or not isinstance(lng, str):
        raise ValueError("Both 's' and 'lng' must be strings.")

    if lng == "en":
        return s
    elif lng:
        return s.replace(".html", f"_{lng}.html")
    return s
