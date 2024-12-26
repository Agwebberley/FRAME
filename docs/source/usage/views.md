# Views

This document provides guidance on working with views in the framework. As of version `0.9.0`, the framework consolidates functionality into base views and introduces additional mixins and utilities for enhanced flexibility and interactivity.

---

## Overview of Base Views

The framework provides a set of prebuilt base views that streamline CRUD operations and incorporate dynamic features such as navigation, report generation, and inline editing.

### Available Base Views
1. **BaseCreateView**
   - Handles creating new instances of models.
   - Supports dynamic forms generated based on user permissions and enabled fields.

2. **BaseUpdateView**
   - Manages updates to existing model instances.
   - Includes dynamic form generation and contextualized navigation.

3. **BaseListView**
   - Lists model instances with support for search, filtering, pagination, and inline editing.
   - Integrates seamlessly with HTMX for real-time updates.

4. **BaseDetailView**
   - Displays detailed information about a single model instance.
   - Supports child model listings and configurable reports.

5. **BaseDeleteView**
   - Provides a confirmation flow for deleting instances with contextual navigation.

---

## Consolidated Master-Detail Functionality

The previously separate MasterDetail views have been deprecated. Their functionality is now integrated into `BaseDetailView` and other base views, streamlining the framework and reducing redundancy.

### Example: Parent-Child Relationships
In `BaseDetailView`, child model instances are dynamically retrieved and displayed within the detail view of the parent model. This is configured automatically using the `get_child_models` utility and child model definitions in `get_config`.

---

## Ajax and HTMX Utility Views

The framework supports modern web interactivity with views designed for HTMX and Ajax workflows. These utility views make it easier to implement real-time updates without reloading the entire page.

### Available Utility Views

1. **update_field**
   - Dynamically updates a single field of a model instance via Ajax.
   - Accepts `POST` requests with the following parameters:
     - `app`: The app label of the model.
     - `model`: The name of the model.
     - `pk`: The primary key of the instance to update.
     - `field`: The field name to update.
     - `value`: The new value for the field.

   Example:
   ```html
   <input type="checkbox"
          hx-post="/update-field/"
          hx-include="[name='app'], [name='model'], [name='pk'], [name='field']"
          hx-trigger="change">
   ```

2. **edit_field**
   - Returns a field-specific editing form fragment via Ajax.
   - Accepts `POST` requests with the following parameters:
     - `app`: The app label of the model.
     - `model`: The name of the model.
     - `pk`: The primary key of the instance to edit.
     - `field`: The field name to edit.

   Example:
   ```html
   <span hx-post="/edit-field/"
         hx-include="[name='app'], [name='model'], [name='pk'], [name='field']"
         hx-trigger="dblclick"
         hx-swap="outerHTML">
     {{ field_value }}
   </span>
   ```

### Benefits of HTMX Integration
- **Minimal Boilerplate**: Simplifies interactivity without requiring a full front-end framework.
- **Real-Time Updates**: Enables inline edits, live searches, and dynamic form interactions.
- **Customizable Fragments**: Leverages reusable partial templates for rendering updates (`editable_field_fragment.html`, `edit_field_fragment.html`).

---

## Mixins

The framework introduces several reusable mixins to enhance the functionality of views.

### NavigationMixin
Adds navigation metadata to the context, dynamically building menus based on enabled models.

### ReportMixin
Enables report generation in views, with options for PDF output, date ranges, and customizable orientations.

### FormsetMixin
Handles inline formsets for managing related models, simplifying parent-child form submissions.

### Other Enhancements
As of `0.9.0`, all mixins are designed to be composable, allowing you to layer multiple functionalities into a single view.

---

## Customizing Views

Customization can be achieved by subclassing the base views and adding or overriding methods. For example:

```python
from frame.base_views import BaseListView

class CustomListView(BaseListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)
```

For advanced use cases, you can also create custom mixins to extend the provided base functionality.
