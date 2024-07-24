# Views

Frame comes with a set of pre-built views that rely on Meta Models to dynamically build each of the different CRUD views for either standard or Master Detail models.

## BaseCreateView

`BaseCreateView` is used for creating new instances of a model. It dynamically generates the form based on the model configuration and includes all enabled fields.

- **Template:** `form.html`
- **Methods:**
  - `get_form_class()`: Generates the form class based on the model configuration.
  - `get_context_data()`: Adds model configuration and enabled fields to the context.

## BaseUpdateView

`BaseUpdateView` is used for updating existing instances of a model. It dynamically generates the form based on the model configuration and includes all enabled fields.

- **Template:** `form.html`
- **Methods:**
  - `get_form_class()`: Generates the form class based on the model configuration.
  - `get_context_data()`: Adds model configuration and enabled fields to the context.

## BaseListView

`BaseListView` is used for displaying a list of model instances. It supports searching, pagination, and sorting based on the model configuration.

- **Template:** `list.html`
- **Methods:**
  - `get_queryset()`: Retrieves the queryset, applying search and sorting.
  - `get_context_data()`: Adds model configuration, enabled fields, and actions to the context.
  - `render_to_response()`: Renders the response, using a partial template if the request is an HTMX request.

## BaseDetailView

`BaseDetailView` is used for displaying the details of a single model instance. It dynamically generates the detail view based on the model configuration and includes all enabled fields.

- **Template:** `detail.html`
- **Methods:**
  - `get_context_data()`: Adds model configuration, enabled fields, and actions to the context.

## BaseDeleteView

`BaseDeleteView` is used for deleting model instances. It provides a confirmation view before performing the deletion.

- **Template:** `confirm_delete.html`
- **Methods:**
  - `get_context_data()`: Adds the return URL to the context.

## BaseMasterDetailView

`BaseMasterDetailView` is used for displaying details of a parent model instance along with its child instances in a master-detail layout.

- **Template:** `master_detail.html`
- **Methods:**
  - `get_context_data()`: Adds model configuration, enabled fields, child instances, and actions to the context.

## MasterDetailCreateView

`MasterDetailCreateView` is used for creating new instances of a parent model and its related child models in a master-detail layout.

- **Template:** `master_detail_form.html`
- **Methods:**
  - `get()`: Handles GET requests to render the form.
  - `post()`: Handles POST requests to save the form data.

## MasterDetailUpdateView

`MasterDetailUpdateView` is used for updating existing instances of a parent model and its related child models in a master-detail layout.

- **Template:** `master_detail_form.html`
- **Methods:**
  - `get()`: Handles GET requests to render the form.
  - `post()`: Handles POST requests to save the form data.

## NavigationMixin

`NavigationMixin` is a mixin that adds navigation context to views. It provides the navigation information required to display the application and model menus.

- **Methods:**
  - `get_context_data()`: Adds navigation information to the context.

These views leverage the power of the Meta Models to dynamically generate the appropriate forms, lists, and detail views based on the model configurations, reducing the amount of boilerplate code needed and ensuring a consistent interface across your application.
