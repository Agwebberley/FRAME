import datetime
from decimal import Decimal
import json
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from frame.aws_utils import publish_event
from django.forms.models import model_to_dict


# Meta Models
class BaseModelManager(models.Manager):
    """
    Custom manager to filter out deleted objects.
    """

    def get_queryset(self):
        """
        Get the queryset, filtering out objects marked as deleted.
        """
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """
    Abstract base model with common fields and soft delete functionality.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseModelManager()
    all_objects = models.Manager()  # Manager that includes deleted objects

    def save(self, *args, **kwargs):
        """
        Override save method to publish create or update events.
        """
        is_new_instance = not self.pk
        super().save(
            *args, **kwargs
        )  # Save first to ensure we have an ID for new instances

        event_data = {
            "channel": self.__class__.__name__,
            "action": "created" if is_new_instance else "updated",
            "data": self.serialize(),
        }
        publish_event(self.__class__.__name__, json.dumps(event_data))

    def delete(self, *args, **kwargs):
        """
        Override delete method to perform a soft delete and publish delete events.
        """
        self.is_deleted = True
        self.save(*args, **kwargs)  # Pass args and kwargs to save

        event_data = {
            "channel": self.__class__.__name__,
            "action": "deleted",
            "data": self.serialize(),
        }
        publish_event(self.__class__.__name__, json.dumps(event_data))

    def serialize(self):
        """
        Serialize the model instance into a JSON serializable dictionary.
        """

        def convert_to_serializable(value):
            if isinstance(value, datetime.datetime):
                return value.isoformat()
            elif isinstance(value, datetime.date):
                return value.isoformat()
            elif isinstance(value, Decimal):
                return float(value)
            return value

        data = model_to_dict(self)
        data = {k: convert_to_serializable(v) for k, v in data.items()}

        return data

    class Meta:
        abstract = True


class LogMessage(BaseModel):
    """
    Model to log messages for different actions and channels.
    """

    channel = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    message = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.channel} - {self.action}"


class ModelAction(models.Model):
    """
    Model to define actions that can be performed on other models.
    """

    ACTION_TYPES = {("dropdown", "Dropdown"), ("button", "Button")}
    list_name = models.CharField(max_length=255)
    detail_name = models.CharField(max_length=255, null=True, blank=True)
    pattern = models.CharField(max_length=255)
    action_type = models.CharField(
        max_length=255, choices=ACTION_TYPES, default="dropdown"
    )
    # Enabled Pages
    enable_in_list = models.BooleanField(default=True)
    enable_in_detail = models.BooleanField(default=True)
    include_pk = models.BooleanField(default=True)

    def __str__(self):
        return self.list_name


class AppConfiguration(models.Model):
    """
    Model to store application-wide configuration settings.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    navigation_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ModelConfiguration(models.Model):
    """
    Model to store configuration settings for individual models.
    """

    app = models.ForeignKey(
        AppConfiguration, related_name="models", on_delete=models.CASCADE
    )
    model_name = models.CharField(max_length=255)
    enable_search = models.BooleanField(default=True)
    list_title = models.CharField(max_length=255, blank=True, null=True)
    default_sort_by = models.CharField(max_length=255, blank=True, null=True)
    navigation_enabled = models.BooleanField(default=True)
    list_url = models.CharField(max_length=255, blank=True, null=True)
    # Views
    actions = models.ManyToManyField(ModelAction, related_name="models", blank=True)
    # Reports
    list_report = models.BooleanField(default=False)
    detail_report = models.BooleanField(default=False)
    # Permissions
    read_permission_groups = models.ManyToManyField(
        Group, related_name="read_model_permissions", blank=True
    )
    read_permission_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="read_model_permissions", blank=True
    )
    write_permission_groups = models.ManyToManyField(
        Group, related_name="write_model_permissions", blank=True
    )
    write_permission_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="write_model_permissions", blank=True
    )

    def __str__(self):
        return f"{self.app.name} - {self.model_name}"


class FieldConfiguration(models.Model):
    """
    Model to store configuration settings for individual fields within models.
    """

    model = models.ForeignKey(
        ModelConfiguration, related_name="fields", on_delete=models.CASCADE
    )
    field_name = models.CharField(max_length=255)
    enable_in_list = models.BooleanField(default=True)
    enable_in_detail = models.BooleanField(default=True)
    enable_in_form = models.BooleanField(default=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    inherit_permissions = models.BooleanField(default=True)
    # Reports
    list_report = models.BooleanField(default=True)
    detail_report = models.BooleanField(default=True)
    # Permissions
    read_permission_groups = models.ManyToManyField(
        Group, related_name="read_field_permissions", blank=True
    )
    read_permission_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="read_field_permissions", blank=True
    )
    write_permission_groups = models.ManyToManyField(
        Group, related_name="write_field_permissions", blank=True
    )
    write_permission_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="write_field_permissions", blank=True
    )

    def __str__(self):
        return f"{self.model.model_name} - {self.field_name}"
