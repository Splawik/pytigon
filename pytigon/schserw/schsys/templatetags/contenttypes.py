"""Python template filters."""

from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.filter(name="table_exists")
def table_exists(table_name):
    """Check if a table exists in the database.

    Args:
        table_name (str): The name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    try:
        ContentType.objects.get(model=table_name.lower())
        return True
    except ObjectDoesNotExist:
        return False
    except Exception as e:
        # Log the exception if needed
        return False
