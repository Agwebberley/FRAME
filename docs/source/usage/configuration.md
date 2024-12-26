# Configuration Reference

This document details all configuration options available in the framework, including their purpose, valid values, and examples of usage.

---

## Global Configuration Options

### Model Name
- **Key**: `model_name`
- **Description**: Specifies the name of the model.
- **Type**: `String`
- **Default**: The model’s class name.
- **Example**:
  ```python
  "model_name": "Task"
  ```

### List Title
- **Key**: `list_title`
- **Description**: The title displayed on the list view.
- **Type**: `String`
- **Default**: `Model Name List`
- **Example**:
  ```python
  "list_title": "Tasks"
  ```

### Create Title
- **Key**: `create_title`
- **Description**: The title displayed on the create form view.
- **Type**: `String`
- **Default**: `Create Model Name`
- **Example**:
  ```python
  "create_title": "Create Task"
  ```

### Enable Search
- **Key**: `enable_search`
- **Description**: Enables the search bar on the list view.
- **Type**: `Boolean`
- **Default**: `False`
- **Example**:
  ```python
  "enable_search": True
  ```

### Default Sort By
- **Key**: `default_sort_by`
- **Description**: Specifies the default field to sort by in the list view.
- **Type**: `String`
- **Default**: `pk`
- **Example**:
  ```python
  "default_sort_by": "pk"
  ```

### List URL
- **Key**: `list_url`
- **Description**: The URL name for the model's list view.
- **Type**: `String`
- **Default**: None
- **Example**:
  ```python
  "list_url": "task-list"
  ```

### Navigation
- **Key**: `navigation`
- **Description**: Indicates whether the model appears in the navigation menu.
- **Type**: `Boolean`
- **Default**: `False`
- **Example**:
  ```python
  "navigation": True
  ```

---

## Tab Configuration Options

### Tabs
- **Key**: `tabs`
- **Description**: Configuration for tabs within a model.
- **Type**: `Dict`
- **Default**: None
- **Fields**:
  - `app_label`: The app label of the tab’s model.
  - `model_name`: The name of the tab’s model.
  - `name_field`: The field name for tab labels.
  - `field`: The related field used to filter the tabs.
  - `add_url`: The URL for creating a new tab.
- **Example**:
  ```python
  "tabs": {
      "app_label": "task",
      "model_name": "TaskList",
      "name_field": "list_name",
      "field": "task_list",
      "add_url": "tasklist-create",
  }
  ```

---

## Field Configuration Options

### Fields
- **Key**: `fields`
- **Description**: A list of field configurations for the model.
- **Type**: `List[Dict]`
- **Field Options**:
  - `name`: The name of the field.
  - `display_name`: The human-readable name for the field.
  - `enable_in_list`, `enable_in_detail`, `enable_in_form`: Toggles field visibility in specific views.
  - `editable_in_list`: Allows inline editing in list views.
  - `custom_fragment`: Specifies a custom template fragment for rendering the field.
  - `role`: Defines special roles (e.g., `"tabs"` for relationships).
- **Example**:
  ```python
  "fields": [
      {
          "name": "task_name",
          "display_name": "Task Name",
          "enable_in_list": True,
          "enable_in_detail": True,
          "enable_in_form": True,
          "editable_in_list": True,
      },
      {
          "name": "task_tags",
          "display_name": "Task Tags",
          "enable_in_list": True,
          "custom_fragment": "custom_fragments/task_tags.html",
      },
  ]
  ```

---

## Actions Configuration Options

### Actions
- **Key**: `actions`
- **Description**: Configures available actions for a model.
- **Type**: `Dict`
- **Fields**:
  - `button`: Actions displayed as buttons.
  - `dropdown`: Actions displayed in dropdown menus.
- **Action Fields**:
  - `name`: The name of the action.
  - `url`: The URL for the action.
  - `disabled`: Specifies views where the action should be disabled.
- **Example**:
  ```python
  "actions": {
      "button": [
          {"name": "Create", "url": "task-create", "disabled": ["detail"]},
      ],
      "dropdown": [
          {"name": "Details", "url": "task-detail", "disabled": ["detail"]},
          {"name": "Edit", "url": "task-update"},
          {"name": "Delete", "url": "task-delete"},
      ],
  }
  ```

---

## Example Full Configuration

```python
@classmethod
def get_config(cls):
    return {
        "model_name": "Task",
        "list_title": "Tasks",
        "create_title": "Create Task",
        "enable_search": True,
        "default_sort_by": "pk",
        "list_url": "task-list",
        "navigation": True,
        "tabs": {
            "app_label": "task",
            "model_name": "TaskList",
            "name_field": "list_name",
            "field": "task_list",
            "add_url": "tasklist-create",
        },
        "fields": [
            {
                "name": "task_name",
                "display_name": "Task Name",
                "enable_in_list": True,
                "enable_in_detail": True,
                "enable_in_form": True,
                "editable_in_list": True,
            },
        ],
        "actions": {
            "button": [{"name": "Create", "url": "task-create"}],
            "dropdown": [
                {"name": "Details", "url": "task-detail"},
                {"name": "Edit", "url": "task-update"},
                {"name": "Delete", "url": "task-delete"},
            ],
        },
    }
```

