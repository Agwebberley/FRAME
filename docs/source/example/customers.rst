# Customers App

The `customers` app provides a minimalist example of the essential components required to create a functional app within the FRAME library.

## Creating a New App

To create a new app, follow these steps:

1. Run the following command to start a new app:

   `python manage.py startapp <app_name>`

2. Move the newly created app folder into your `<project_slug>` directory.
3. Add the app to the `INSTALLED_APPS` list in your `settings.py` file.
4. Update the `apps.py` file in your app folder, changing the `name` variable to:

   `<project_slug>.<app_name>`

5. Create a `urls.py` file within the app directory.
6. Add the app’s URLs to the `urlpatterns` list in the `urls.py` file located in the `<project_slug>` folder. (Refer to the template for an example.)

## Models

The `models.py` file demonstrates a basic implementation of the `BaseModel` class, which extends `models.Model`. This example shows how to set up models that integrate seamlessly with FRAME's architecture.

## Views

In the `views.py` file, models are connected to templates using class-based views. FRAME provides a comprehensive set of generic views for handling create, update, delete, and list operations on models. There are two main types of generic views available: Basic and Master-Detail. The `customers` app uses Basic views. For an example of Master-Detail views, refer to the `orders` app.

## Templates

*TODO: Add documentation on customizing templates for specific use cases.*

## Admin Integration

To integrate a new app with FRAME, use the following command:

`python manage.py update_config`

This command will register `AppConfiguration`, `ModelConfiguration`, and `FieldConfiguration` entries for any new components since the last run. You can then manage the app through the admin interface.

For the `customers` app, ensure that the `create`, `update`, `detail`, and `delete` actions are enabled in the `Customer` model configuration. These actions correspond to the views provided in the `customers` app. By default, these actions are disabled to prevent errors in cases where corresponding views do not exist.

