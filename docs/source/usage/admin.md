# Admin

This section explains how to use the meta models properly within the FRAME Django Template helper app and outlines the current configuration options available in the admin dashboard.

## Using Meta Models

The FRAME app relies on meta models to dynamically generate forms and views. Proper configuration of these meta models is crucial for the system to function correctly.

### Running the `update_config` Management Command

Whenever you complete a migration, you should run the `update_config` management command. This command will create entries for every app, model, and field in the configuration models.
```bash
python manage.py update_config
```

### Initial Configuration

When entries are created, all actions are enabled by default. This can cause errors if a particular model does not support an action. For example, if the `LogMessage` model does not have a create view, enabling the create action will cause an error. To resolve this, you need to manually disable the unsupported actions in the admin dashboard. (Note: At some point, logic will be added to handle this properly)

### Admin Dashboard

The admin dashboard allows you to make a variety of configuration changes. This section will explain the current options available for configuration.

## Current Configuration Options

### AppConfiguration

The `AppConfiguration` model stores configuration settings for applications.

- **Name**: The unique name of the application.
- **Description**: A description of the application. This field can be left blank.
- **Navigation Enabled**: A boolean indicating whether navigation is enabled for the application.

### ModelConfiguration

The `ModelConfiguration` model stores configuration settings for individual models within an application.

- **App**: The associated `AppConfiguration` instance.
- **Model Name**: The name of the model.
- **Enable Search**: A boolean indicating whether search is enabled for the model.
- **List Title**: The title of the list view. This field can be left blank.
- **Default Sort By**: The default sorting field for the list view. This field can be left blank.
- **Navigation Enabled**: A boolean indicating whether navigation is enabled for the model.
- **List URL**: The URL for the list view. This field can be left blank.
- **Actions**: The actions associated with the model. You can enable or disable actions as needed.
- **Read Permission Groups**: Groups with read permissions for the model.
- **Read Permission Users**: Users with read permissions for the model.
- **Write Permission Groups**: Groups with write permissions for the model.
- **Write Permission Users**: Users with write permissions for the model.

### FieldConfiguration

The `FieldConfiguration` model stores configuration settings for individual fields within models.

- **Model**: The associated `ModelConfiguration` instance.
- **Field Name**: The name of the field.
- **Enable in List**: A boolean indicating whether the field is enabled in the list view.
- **Enable in Detail**: A boolean indicating whether the field is enabled in the detail view.
- **Enable in Form**: A boolean indicating whether the field is enabled in forms.
- **Display Name**: The display name of the field. This field can be left blank.
- **Inherit Permissions**: A boolean indicating whether the field inherits permissions from the model.
- **Read Permission Groups**: Groups with read permissions for the field.
- **Read Permission Users**: Users with read permissions for the field.
- **Write Permission Groups**: Groups with write permissions for the field.
- **Write Permission Users**: Users with write permissions for the field.

## Summary

The admin dashboard provides powerful tools for configuring your applications, models, and fields within the FRAME Django Template helper app. By properly setting up and managing these configurations, you can ensure that your application behaves as expected and takes full advantage of FRAME's dynamic capabilities.

For more detailed information on each configuration option, refer to the Django admin documentation or the specific model documentation within the FRAME app.
