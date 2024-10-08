from django.core.management.base import BaseCommand
from django.apps import apps
from frame.models import (
    AppConfiguration,
    ModelConfiguration,
    FieldConfiguration,
    ModelAction,
)
from django.conf import settings


class Command(BaseCommand):
    """
    Django management command to add new apps, models, and fields to the configuration models with default values.
    """

    help = (
        "Add any new apps/models/fields to the configuration models with default values"
    )

    def handle(self, *args, **options):
        """
        Handle the command execution.

        This method iterates through the apps and their models defined in settings.CUSTOM_APPS,
        adding any new app configurations, model configurations, field configurations, and default model actions
        to the database.
        """
        # List of custom apps to include in the configuration
        custom_apps = settings.CUSTOM_APPS

        for app_config in apps.get_app_configs():
            app_name = app_config.name
            app_name = app_name.split(".")[-1]

            # Skip apps not in the custom apps list
            if app_name not in custom_apps:
                continue

            # Add app configuration if it doesn't exist
            app_config_obj, created = AppConfiguration.objects.get_or_create(
                name=app_name
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Added new app configuration: {app_name}")
                )

            for model in app_config.get_models():
                model_name = model.__name__

                # Add model configuration if it doesn't exist
                model_config_obj, created = ModelConfiguration.objects.get_or_create(
                    app=app_config_obj,
                    model_name=model_name,
                    defaults={
                        "enable_search": True,
                        "list_title": f"{model_name} List",
                        "default_sort_by": "id",
                        "list_url": f"{model_name}-list".lower(),
                    },
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Added new model configuration: {model_name} in app {app_name}"
                        )
                    )

                for field in model._meta.get_fields():
                    # Skip reverse relations
                    if (
                        field.is_relation
                        and field.many_to_one
                        and not field.related_model
                    ):
                        continue

                    field_name = field.name
                    verbose_name = getattr(field, "verbose_name", field_name)

                    # Add field configuration if it doesn't exist
                    field_config_obj, created = (
                        FieldConfiguration.objects.get_or_create(
                            model=model_config_obj,
                            field_name=field_name,
                            defaults={
                                "enable_in_list": True,
                                "enable_in_detail": True,
                                "display_name": verbose_name,
                                "inherit_permissions": True,
                                "enable_in_form": False
                                if field_name
                                in ["created_at", "updated_at", "is_deleted"]
                                else True,
                            },
                        )
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Added new field configuration: {field_name} in model {model_name}"
                            )
                        )

                # Default Model Actions
                default_actions = [
                    ("Create", "create", "button"),
                    ("Details", "detail", "dropdown"),
                    ("Edit", "update", "dropdown"),
                    (
                        "Delete",
                        "delete",
                        "dropdown",
                    ),
                ]

                for action in default_actions:
                    action_name, action_pattern, action_type = action
                    action_obj, created = ModelAction.objects.get_or_create(
                        list_name=action_name,
                        defaults={
                            "detail_name": action_name,
                            "pattern": action_pattern,
                            "action_type": action_type,
                        },
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Added new model action: {action_name}")
                        )

                    if created:
                        model_config_obj.actions.add(action_obj)

        self.stdout.write(self.style.SUCCESS("Configuration update complete."))
