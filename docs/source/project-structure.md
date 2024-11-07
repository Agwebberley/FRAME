# Project Structure

FRAME is designed to extend Django's core functionality through a structured library of reusable components. Understanding the FRAME project structure will help you locate and use its components efficiently.

## Directory Overview

The FRAME project follows a modular structure that organizes key components into distinct directories. Each directory is tailored to specific functions like views, mixins, templates, and utilities, providing a clear layout for development and customization.

```plaintext
frame/
├── templates/
├── base_views.py
├── utils.py
├── models.py
├── mixins.py
├── __init__.py
├── settings.py
```

## Directory and File Descriptions

### `frame/base_views.py`

This file contains FRAME's base views, which extend Django's generic views (e.g., `CreateView`, `UpdateView`). These views are designed to handle CRUD operations with additional FRAME-specific functionality such as formset handling and dynamic configuration.

**Main Classes:**
- **`BaseCreateView`**: A base view for creating model instances with customizable forms and formsets.
- **`BaseUpdateView`**: A view for updating model instances, with support for child model formsets.
- **`BaseListView`**: A base list view with optional search functionality and navigation settings.
- **`BaseDetailView`**: A detail view for displaying model instances with related child objects.

These base views provide a foundation for building consistent and reusable views across FRAME applications.

### `frame/mixins.py`

The `mixins` file includes reusable mixin classes that add specific features to FRAME views, like navigation or report generation. Mixins are a modular way to add functionality without duplicating code across views.

**Main Mixins:**
- **`NavigationMixin`**: Adds navigation links (like "next" or "previous") to views for easier model browsing.
- **`ReportMixin`**: Provides support for generating reports and handling export options.
- **`FormsetMixin`**: Manages formsets for child models within create and update views, making it easier to handle related models in a single form.

### `frame/templates/`

This directory contains HTML templates that FRAME uses to render forms, lists, and detail views. These templates are designed with Bootstrap for a clean and responsive layout.

**Main Templates:**
- **`form.html`**: Used by create and update views, supporting dynamic forms and formsets.
- **`list.html`**: Template for displaying model lists, with optional search and sorting capabilities.
- **`detail.html`**: Template for displaying details of a single model instance, with support for related child models.
- **`confirm_delete.html`**: Confirmation page template used by delete views.

These templates are customizable and provide a consistent look across FRAME-based applications.

### `frame/utils.py`

The `utils.py` file contains utility functions that support FRAME’s core functionalities, including helper functions for formset generation, child model handling, and field retrieval.

**Key Functions:**
- **`generate_inline_formset`**: Creates formsets for handling related child models in forms.
- **`get_child_models`**: Retrieves child models for a given parent model, which is useful for Master-Detail views.
- **`get_enabled_fields`**: Returns fields that are configured to be visible or editable in forms and views.

These utilities provide essential backend support for FRAME’s view and model configurations.

### `frame/models.py`

This file includes FRAME's base model classes, such as `BaseModel`, which provides a standardized model structure with additional functionality. `BaseModel` extends Django’s ORM model with extra features that align with FRAME’s architecture.

### `frame/__init__.py`

This file initializes the FRAME library and ensures that all components are accessible when FRAME is imported. It may also include version information and other metadata.

### `frame/settings.py`

The `settings.py` file contains default settings for FRAME, including configuration options that can be overridden in Django’s main `settings.py` for project-specific customizations.

**Common Settings:**
- **FRAME-specific settings**: Options for enabling/disabling features (e.g., navigation, search).
- **Template and URL configurations**: Settings related to template paths and URLs used within FRAME.

## Example Applications

> TODO: Linking this section

FRAME includes several example applications that demonstrate its components in action, such as `customers`, `orders`, and `finance`. These apps showcase how to use `BaseModel`, `BaseView`, `FormsetMixin`, and other FRAME components to build fully functional Django apps with minimal setup.

- **`customers`**: Demonstrates basic CRUD operations with FRAME’s base views.
- **`orders`**: Shows complex relationships, including many-to-many and one-to-many setups.
- **`finance`**: Provides an example of integrating FRAME with external services (like AWS SNS) and handling inter-app communication.

## Summary

This structure keeps FRAME’s components organized and accessible, allowing developers to quickly locate and customize views, models, and templates as needed. By following this structure, FRAME ensures a streamlined development experience with a consistent, modular approach.
