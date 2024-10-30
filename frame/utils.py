from django import forms
from django.apps import apps


def get_enabled_fields(app_name, model_name, user, view_type="list", properties=True):
    """
    Get the enabled fields for a model based on the user's permissions and the view type.

    :param app_name: The name of the app.
    :type app_name: str
    :param model_name: The name of the model.
    :type model_name: str
    :param user: The user instance.
    :type user: User
    :param view_type: The type of view ('list', 'detail', 'form').
    :type view_type: str
    :param properties: Whether to include properties in the enabled fields.
    :type properties: bool
    :return: A list of enabled field names.
    :rtype: list
    """
    model = apps.get_model(app_label=app_name, model_name=model_name)
    model_config = model.get_config()
    print(model_config)
    field_configs = model_config["fields"]
    model_field_names = [field.name for field in model._meta.get_fields()]
    enabled_fields = []
    for field_config in field_configs:
        if field_config["name"] in model_field_names:
            field = model._meta.get_field(field_config["name"])
            if not (field.auto_created or field.one_to_one or field.many_to_many):
                if view_type == "list" and field_config["enable_in_list"]:
                    enabled_fields.append(field_config["name"])
                elif view_type == "detail" and field_config["enable_in_detail"]:
                    enabled_fields.append(field_config["name"])
                elif view_type == "form" and field_config["enable_in_form"]:
                    enabled_fields.append(field_config["name"])
    if view_type != "form" and properties:
        properties = [
            prop for prop in dir(model) if isinstance(getattr(model, prop), property)
        ]
        if "pk" in properties:
            properties.pop(properties.index("pk"))
        if "get_config" in properties:
            properties.pop(properties.index("get_config"))
        enabled_fields += properties

    if "is_deleted" in enabled_fields:
        enabled_fields.pop(enabled_fields.index("is_deleted"))
    return enabled_fields


def user_has_model_read_permission(user, model_config):
    """
    Check if a user has read permission for a model.

    :param user: The user instance.
    :type user: User
    :param model_config: The model configuration instance.
    :type model_config: ModelConfiguration
    :return: True if the user has read permission, False otherwise.
    :rtype: bool
    """
    if user.is_superuser:
        return True
    if model_config.read_permission_users.filter(id=user.id).exists():
        return True
    if model_config.read_permission_groups.filter(
        id__in=user.groups.values_list("id", flat=True)
    ).exists():
        return True
    return False


def user_has_model_write_permission(user, model_config):
    """
    Check if a user has write permission for a model.

    :param user: The user instance.
    :type user: User
    :param model_config: The model configuration instance.
    :type model_config: ModelConfiguration
    :return: True if the user has write permission, False otherwise.
    :rtype: bool
    """
    if user.is_superuser:
        return True
    if model_config.write_permission_users.filter(id=user.id).exists():
        return True
    if model_config.write_permission_groups.filter(
        id__in=user.groups.values_list("id", flat=True)
    ).exists():
        return True
    return False


def user_has_field_read_permission(user, field_config):
    """
    Check if a user has read permission for a field.

    :param user: The user instance.
    :type user: User
    :param field_config: The field configuration instance.
    :type field_config: FieldConfiguration
    :return: True if the user has read permission, False otherwise.
    :rtype: bool
    """
    if field_config.inherit_permissions:
        return user_has_model_read_permission(user, field_config.model)
    if user.is_superuser:
        return True
    if field_config.read_permission_users.filter(id=user.id).exists():
        return True
    if field_config.read_permission_groups.filter(
        id__in=user.groups.values_list("id", flat=True)
    ).exists():
        return True
    return False


def user_has_field_write_permission(user, field_config):
    """
    Check if a user has write permission for a field.

    :param user: The user instance.
    :type user: User
    :param field_config: The field configuration instance.
    :type field_config: FieldConfiguration
    :return: True if the user has write permission, False otherwise.
    :rtype: bool
    """
    if field_config.inherit_permissions:
        return user_has_model_write_permission(user, field_config.model)
    if user.is_superuser:
        return True
    if field_config.write_permission_users.filter(id=user.id).exists():
        return True
    if field_config.write_permission_groups.filter(
        id__in=user.groups.values_list("id", flat=True)
    ).exists():
        return True
    return False


def generate_dynamic_form(app_name, model_name, user, instance=None):
    """
    Generate a dynamic form for a model based on the user's permissions and enabled fields.

    :param app_name: The name of the app.
    :type app_name: str
    :param model_name: The name of the model.
    :type model_name: str
    :param user: The user instance.
    :type user: User
    :param instance: The model instance (optional).
    :type instance: Model
    :return: The dynamic form class.
    :rtype: ModelForm
    """
    model_class = apps.get_model(app_label=app_name, model_name=model_name)
    enabled_fields = get_enabled_fields(app_name, model_name, user, view_type="form")

    class DynamicForm(forms.ModelForm):
        class Meta:
            model = model_class
            fields = enabled_fields

            def __init__(self, *args, **kwargs):
                super(DynamicForm, self).__init__(*args, **kwargs)

    return DynamicForm


def get_actions(app_name, model_name, view_type="list"):
    """
    Get the actions available for a model based on the view type.

    :param app_name: The name of the app.
    :type app_name: str
    :param model_name: The name of the model.
    :type model_name: str
    :param view_type: The type of view ('list', 'detail').
    :type view_type: str
    :return: A dictionary or list of actions.
    :rtype: dict or list
    """
    model = apps.get_model(app_label=app_name, model_name=model_name)
    model_config = model.get_config()
    actions = model_config["actions"]
    # POSSIBLY DELETE THIS
    return actions


def generate_inline_formset(app_label, parent_model, child_model, model_name, user):
    """
    Generate an inline formset for a parent model and its child model.

    :param app_label: The app label of the parent model.
    :type app_label: str
    :param parent_model: The parent model class.
    :type parent_model: Model
    :param child_model: The child model class.
    :type child_model: Model
    :param model_name: The name of the child model.
    :type model_name: str
    :param user: The user instance.
    :type user: User
    :return: The inline formset class.
    :rtype: InlineFormSet
    """
    return forms.inlineformset_factory(
        parent_model,
        child_model,
        form=generate_dynamic_form(app_label, model_name, user),
        extra=1,
        can_delete=True,
    )


def get_child_models(app_name, model_name):
    """
    Get the child models of a model.

    :param app_name: The name of the app.
    :type app_name: str
    :param model_name: The name of the model.
    :type model_name: str
    :return: A list of child model classes.
    :rtype: list
    """
    model = apps.get_model(app_label=app_name, model_name=model_name)
    child_models = []
    model_config = model.get_config()
    # Safely get 'children' key; default to empty list if not present
    for child in model_config.get("children", []):
        child_model = apps.get_model(app_label=app_name, model_name=child)
        child_models.append(child_model)
    return child_models
