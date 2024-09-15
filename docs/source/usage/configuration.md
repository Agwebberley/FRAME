# Configuration
### Added in 0.4.0
#### This is a STUB and will be updated with more information soon

The configuration system allows you to quickly define the behavior of your models and applications.

Every model to be recognized by the system must have a `@classmethod` called `get_config` that returns a dictionary with the configuration options.

An example of a model with configuration options is shown below:

```python
    @classmethod
    def get_config(cls):
        return {
            "model_name": "Customer",
            "list_title": "Customers",
            "create_title": "Create Customer",
            "enable_search": True,
            "default_sort_by": "created_at",
            "list_url": "customer-list",
            "navigation": True,
            "fields": [
                {
                    "name": "name",
                    "display_name": "Name",
                    "enable_in_list": True,
                    "enable_in_detail": True,
                    "enable_in_form": True,
                },
                {
                    "name": "email",
                    "display_name": "Email",
                    "enable_in_list": True,
                    "enable_in_detail": True,
                    "enable_in_form": True,
                },
                {
                    "name": "phone",
                    "display_name": "Phone",
                    "enable_in_list": True,
                    "enable_in_detail": True,
                    "enable_in_form": True,
                },
                {
                    "name": "address",
                    "display_name": "Address",
                    "enable_in_list": False,
                    "enable_in_detail": True,
                    "enable_in_form": True,
                },
            ],
            "actions": {
                "button": [
                    {
                        "name": "Create",
                        "url": "customer-create",
                        "disabled": ["detail"],
                    },
                ],
                "dropdown": [
                    {
                        "name": "Details",
                        "url": "customer-detail",
                        "disabled": ["detail"],
                    },
                    {
                        "name": "Edit",
                        "url": "customer-update",
                    },
                    {
                        "name": "Delete",
                        "url": "customer-delete",
                    },
                ],
            },
     }
```
