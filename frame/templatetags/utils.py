from django import template

register = template.Library()


@register.filter
def get_field_value(instance, field_name):
    """
    Get the value of a specified field from a model instance.

    :param instance: The model instance.
    :type instance: Model
    :param field_name: The name of the field.
    :type field_name: str
    :return: The value of the specified field, or an empty string if the field does not exist.
    :rtype: any
    """
    return getattr(instance, field_name, "")


@register.filter
def fformsets(value):
    """
    Remove spaces from a string and make sure it is singular by removing the last character.

    :param value: The input string.
    :type value: str
    :return: The modified string.
    :rtype: str
    """
    return value.replace(" ", "")[:-1]


@register.filter
def titlify(value):
    """
    Replace underscores with spaces in a string and title case it.

    :param value: The input string.
    :type value: str
    :return: The modified string.
    :rtype: str
    """
    return value.replace("_", " ").title()


@register.filter
def get_property(obj, prop):
    """
    Get a property from an object.

    :param obj: The object.
    :type obj: any
    :param prop: The name of the property.
    :type prop: str
    :return: The value of the specified property.
    :rtype: any
    """
    return getattr(obj, prop)


@register.filter
def is_foreign_key(instance, field):
    """
    Check if a field is a ForeignKey.

    :param instance: The model instance.
    :type instance: Model
    :param field: The name of the field.
    :type field: str
    :return: True if the field is a ForeignKey, False otherwise.
    :rtype: bool
    """
    try:
        return instance._meta.get_field(field).get_internal_type() == "ForeignKey"
    except AttributeError:
        return False


@register.filter
def get_detail_url(instance, field):
    """
    Get the detail URL for the related model of a ForeignKey field.

    :param instance: The model instance.
    :type instance: Model
    :param field: The name of the field.
    :type field: str
    :return: The detail URL pattern name for the related model, or an empty string if not applicable.
    :rtype: str
    """
    try:
        return (
            instance._meta.get_field(field).related_model._meta.model_name + "-detail"
        )
    except AttributeError:
        return ""


@register.filter
def get_foreign_key_value(instance, field):
    """
    Get the primary key value of a related model instance from a ForeignKey field.

    :param instance: The model instance.
    :type instance: Model
    :param field: The name of the ForeignKey field.
    :type field: str
    :return: The primary key value of the related model instance, or an empty string if not applicable.
    :rtype: any
    """
    try:
        return getattr(instance, field).pk
    except AttributeError:
        return ""


@register.filter
def get_item(dictionary, key):
    """
    Get the value of a specified key from a dictionary.

    :param dictionary: The dictionary.
    :type dictionary: dict
    :param key: The key.
    :type key: str
    :return: The value of the specified key, or an empty string if the key does not exist.
    :rtype: any
    """
    return dictionary.get(key, "")


@register.filter
def get_choices(instance, field):
    """
    Get the choices for a field.

    :param instance: The model instance.
    :type instance: Model
    :param field: The name of the field.
    :type field: str
    :return: The choices for the specified field, or an empty list if the field does not exist.
    :rtype: list
    """
    try:
        return instance._meta.get_field(field).choices
    except AttributeError:
        return []


@register.filter
def get_field_config(model_class, field_name):
    """
    Get the configuration for a field.

    :param model_class: The model class.
    :type model_class: Model
    :param field_name: The name of the field.
    :type field_name: str
    :return: The configuration for the specified field, or an empty dictionary if the field does not exist.
    :rtype: dict
    """
    fields = model_class.get_config()["fields"]
    for field in fields:
        if field["name"] == field_name:
            return field
    return {}
