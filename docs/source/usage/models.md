# Models

This section describes the primary models used in the FRAME Django Template helper app, with a focus on the `BaseModel`. The `BaseModel` is designed to provide a common foundation for other models, including features such as automatic timestamping, soft deletion, and event publishing.

## BaseModel

The `BaseModel` is an abstract base class that provides common fields and functionality for other models. By inheriting from `BaseModel`, you can ensure that all your models have consistent behavior and fields.

### Purpose

- **Automatic Timestamping:** The `BaseModel` includes `created_at` and `updated_at` fields that automatically track when an instance is created and last updated.
- **Soft Deletion:** Instead of permanently deleting records, `BaseModel` provides an `is_deleted` field to mark records as deleted. This allows for recovery and auditing.
- **Event Publishing:** When instances are created, updated, or deleted, `BaseModel` publishes events to an external system (e.g., AWS SNS) for further processing. See [Pub/Sub](aws.md) for details.

### Fields

- `created_at` (DateTimeField): Automatically set to the current date/time when the object is created.
- `updated_at` (DateTimeField): Automatically set to the current date/time when the object is updated.
- `is_deleted` (BooleanField): Boolean flag for soft deleting objects.

### Methods

- `save(*args, **kwargs)`: Overridden to publish create/update events.
- `delete(*args, **kwargs)`: Overridden to perform a soft delete and publish delete events.
- `serialize()`: Serializes the model instance into a JSON-serializable dictionary.

### Managers

- `objects`: Custom manager to filter out deleted objects.
- `all_objects`: Default manager that includes deleted objects.

### Example

```python
from django.db import models
from frame.models import BaseModel

class MyModel(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
```

### Meta Models

Frame includes several meta models that provide additional functionality. These meta models allow FRAME to dynamically generate the appropriate forms and configurations for your application. You can read more about these meta models and their configurations on the [admin](admin.md) page.
