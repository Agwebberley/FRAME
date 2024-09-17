from django.apps import apps


def nav_helper():
    """
    Helper function to retrieve applications and their models that have navigation enabled.

    :return: Dictionary of apps and their corresponding models with navigation enabled.
    :rtype: dict
    """
    apps_with_models = {}
    # Get all apps with navigation enabled
    # Iterate over all apps and get models with navigation enabled
    # Use the model's get_config method to get the configuration
    # NOTE: No longer using AppConfiguration model
    for app in apps.get_app_configs():
        models_with_nav = []
        for model in app.get_models():
            # Check if get_config method exists
            if not hasattr(model, "get_config"):
                continue
            model_config = model.get_config()
            if model_config["navigation"]:
                models_with_nav.append(
                    {
                        "name": model.get_config()["model_name"],
                        "plural": model._meta.verbose_name_plural,
                        "url": model.__name__.lower() + "-list",
                    }
                )
        if models_with_nav:
            apps_with_models[app.label] = {
                "name": app.verbose_name,
                "models": models_with_nav,
            }
    return apps_with_models


class NavigationMixin:
    """
    Mixin to add navigation context to views.
    """

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view, adding navigation information.

        :param kwargs: Additional context data.
        :return: Context data with navigation information.
        :rtype: dict
        """
        if hasattr(super(), "get_context_data"):
            context = super().get_context_data(**kwargs)
        else:
            context = {}

        apps_with_models = nav_helper()

        context["apps"] = apps_with_models
        context["current_app"] = self.request.resolver_match.app_name
        return context
