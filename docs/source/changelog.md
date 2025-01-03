# Changelog

## [0.9.0] - 12-25-2024

### Added
- `frame/templates/partials/tabs.html`: New partial template for tabs in tables.
- `frame/templates/partials/editable_field_fragment.html`: New partial template for editable field fragments.
- `frame/templates/partials/edit_field_fragment.html`: New partial template for editing fields.
- `frame/base_views.py`: Added functions `update_field` and `edit_field` for dynamic field updates.
- `frame/templatetags/utils.py`: Added new template filters `get_item`, `get_choices`, and `get_field_config` for enhanced field handling.

### Changed
- `frame/base_views.py`:
  - Enhanced `get_queryset` method with filtering and global search capabilities.
  - Added debugging prints for search queries.
  - Included new methods `apply_filter`, `apply_global_search`, and `is_searchable_field`.
  - Updated `get_context_data` to include `app_label`, `editable_fields`, and `tabs`.
- `frame/templates/partials/table_container.html`: Improved table layout with full width.
- `frame/templates/partials/table_body.html`: Enhanced table body to support dynamic field editing.
- `frame/templates/list.html`: Integrated tabs partial into the list template.
- `frame/utils.py`:
  - Added `get_editable_fields` for editable field retrieval in list views.
  - Improved `get_enabled_fields` to handle model properties correctly.
- `frame/urls.py`: Added new URL patterns for `update-field` and `edit-field`.

### Removed
- `frame/models.py`: Removed unused imports `Group` and `settings`.


## [0.8.0] - 11-12-2024

### Added
- `fake_data.py`: New management command to generate fake data for the `Part` model.
- `actions_dropdown.html`: New partial template for a dropdown menu with model actions.
- TailwindCSS support for template styles.
- Alpine.js and HTMX scripts in `base.html` for enhanced client-side interactivity.
- Dark mode toggle and sidebar expansion control with Alpine.js.

### Changed
- Refactored `base_views.py`: Replaced `query` with `search` as the parameter name for search queries.
- Improved layout in `base.html`, `detail.html`, `form.html`, `home.html`, and `list.html`:
  - Updated HTML structure for responsiveness and dark mode compatibility.
  - Integrated TailwindCSS for more flexible and modern styling.
  - Redesigned sidebar and header to support expanded/collapsed views.
- Updated `generate_report_modal.html`:
  - Converted modal to a TailwindCSS-style modal with improved form layout.
  - Added close button functionality without Bootstrap dependencies.

### Removed
- `update_config.py`: Removed management command for updating app configurations automatically.

## [0.7.0] - 11-7-2024

### Summary
This update introduces significant improvements to FRAME, focusing on enhancing formset handling, adding support for child models, and refining documentation. Key changes include the introduction of the FormsetMixin, adjustments to base views, and the new introduction page in documentation.

### New Features
- **Formset Handling**: Added `FormsetMixin` to manage formsets in create and update views, allowing dynamic form management for related models.
- **Child Model Integration**: Updated base views to support dynamic form generation for child models, improving support for parent-child relationships.
  
### Enhancements
- **Documentation**: Introduced a comprehensive "Introduction" page to FRAME’s documentation, explaining its integration with Django and its usage with supporting tool Py_StarUML.
- **Template Updates**: Revamped `form.html` to support tabbed navigation for parent and child forms, enhancing user experience.
- **Contextual Updates**: Updated views to include `verbose_name` and `verbose_name_plural` for better template display of model details.

### Fixes
- **Bug Fix in Detail View**: Corrected an issue in the detail page where any relationship was mistakenly shown as a formset, ensuring accurate representation of related models.



## [0.6.1] - 10-1-2024
### Summary
Massive additions to the docs, most notibly the hello world tutorial and the docs for Py_StarUML.  Py_StarUML has been brought up to date (as it hasn't been updated since before FRAME was seperated out).  You can find the docs for Py_StarUML [here](pystaruml) and the repo (with a copy of the docs) at [https://github.com/agwebberley/Py_StarUML](https://github.com/agwebberley/Py_StarUML).


## [0.6.0] - 09-17-2024

### Summary
Version 0.6.0 builds upon the previous enhancements by introducing a reusable ReportMixin, which centralizes report generation logic for easier reuse across different views. This update allows for dynamic date range filtering in reports, enabling users to specify start and end dates while ensuring valid input through server-side validation. Users now have the ability to select which fields to include in their reports, with checks to ensure at least one field is chosen. Additionally, we've added options to generate reports in either landscape or portrait orientation, which can be configured by developers or selected by users in the report configuration modal. Mixins have been organized into a separate file for better code management, and several bug fixes have been implemented to resolve attribute errors and improve context data handling, resulting in a more robust and user-friendly reporting feature.

### New Features

#### Enhanced Report Generation with `ReportMixin`

- **Introduction of `ReportMixin`**: Created a reusable mixin (`ReportMixin`) to centralize report generation logic across multiple views.
  - **Reusability**: Allows easy integration of report generation into any class-based view by simply including the mixin.
  - **Customization**: Supports extensive customization options for reports.

#### Date Range Filtering in Reports

- **Dynamic Date Range Filtering**: Added the ability to filter report data based on a user-specified date range.
  - **Flexible Configuration**: Set `date_range = True` in views to enable date range filtering.
  - **Date Field Specification**: Introduced `date_field` attribute to specify which model field to use for date filtering.
  - **Validation**: Implemented server-side validation to ensure valid date inputs and proper date range logic.

#### Field Selection Enhancements

- **User-Selectable Fields**: Users can now select which fields to include in their reports.
  - **Dynamic Field Handling**: The mixin handles the selected fields and updates the report context accordingly.
  - **Validation**: Ensured that at least one field must be selected to generate a report.

#### Orientation Configuration for Reports

- **Landscape and Portrait Orientation**: Introduced options to generate reports in either landscape or portrait orientation.
  - **View-Level Configuration**: Set `orientation` attribute in views to specify default orientation.
  - **User Selection**: Added `allow_orientation_selection` flag to enable users to choose orientation in the report configuration modal.
  - **Implementation**: Utilized WeasyPrint's `@page` CSS rule to set page orientation dynamically during PDF generation.

### Improvements

#### Centralization of Mixins

- **Mixins Organized in Separate File**: Moved all mixins, including `ReportMixin`, into a dedicated `mixins.py` file.
  - **Code Organization**: Improved code maintainability and readability by centralizing mixin classes.
  - **Ease of Access**: Simplified import statements and enhanced modularity.

#### Bug Fixes and Stability Enhancements

- **Resolved Attribute Errors**:
  - **`self.object` Handling**: Fixed issues where `self.object` was not available in `DetailView` during report generation by setting it in the mixin.
  - **`self.object_list` Handling**: Addressed problems with `self.object_list` in `ListView` by ensuring it's properly set during `POST` requests.
- **Context Data Management**:
  - **Consistent `enabled_fields`**: Ensured that `enabled_fields` in the context is updated based on user-selected fields.
  - **Mixin and View Coordination**: Adjusted `get_context_data` methods to respect mixin attributes and prevent overwriting.

#### User Experience Enhancements

- **Report Configuration Modal Updates**:
  - **Dynamic Form Fields**: Updated the modal to include date range inputs and orientation options based on view configuration.
  - **Client-Side Validation**: Added JavaScript validation to ensure correct date input before form submission.
- **Error Messaging**:
  - **User Feedback**: Leveraged Django's messaging framework to provide clear error messages and guidance when issues arise during report generation.

### Notes

- **Compatibility Considerations**:
  - **Mixin Order in Views**: Emphasized the importance of mixin ordering to ensure correct method resolution (`ReportMixin` should precede generic views like `ListView` and `DetailView`).
- **Customization and Extensibility**:
  - **Override Methods**: Provided mechanisms to override mixin methods like `get_report_context_data` for further customization.
  - **Additional Features**: Set the groundwork for future enhancements, such as supporting multiple page sizes and asynchronous report generation.


## [0.5.0] - 09-15-2024

### Summary
In version 0.5.0, we've added a customizable report generation feature directly within the main list view of the application. Users can now click a "Generate Report" button to open a modal overlay, where they can set a custom report title, select a specific date range, and choose which fields to include in their report. The application dynamically generates PDF reports using WeasyPrint, ensuring that users can create tailored reports without navigating away from the page. This update enhances the user experience by providing an intuitive and seamless way to produce personalized reports with consistent styling.

### New Features
#### Customizable Report Generation
- Report Generation Overlay: Introduced a new "Generate Report" button in the main list view, allowing users to generate customized PDF reports without leaving the page.
    - Modal Configuration: Clicking the "Generate Report" button opens a modal overlay where users can configure their report settings.
    - Custom Report Title: Users can specify a custom title for their report.
    - Date Range Selection: Added the ability to filter report data by a specific date range.
    - Field Selection: Users can select which fields to include in the report from a list of all available fields.
- Dynamic PDF Generation: Reports are generated on-the-fly based on user-selected options.
    - WeasyPrint Integration: Leveraged WeasyPrint to convert HTML templates into PDF format.
    - Self-Contained Templates: Created a standalone list_print.html template to ensure consistent styling and formatting in the generated PDFs.
    - Inline CSS Styling: Implemented inline CSS within the report template for better control over the printed output.
#### Improvements
- Enhanced List View (`BaseListView`):
    - POST Method Handling: Added a `post` method to handle report generation requests directly from the list view.
    - Context Data Expansion: Updated `get_context_data` to include all fields available for report generation.
    - Queryset Filtering: Implemented filtering of data based on user-selected date ranges to ensure reports contain relevant information.
    - Error Handling: Added validations to handle cases where the start date is after the end date or when no data is available for the selected range, providing appropriate user feedback.

- User Experience Enhancements:
    - Bootstrap Modal Integration: Utilized Bootstrap's modal component for a seamless and responsive overlay experience.
    - Form Validation: Included both server-side and optional client-side validation to enhance form submission reliability.
    - Feedback Mechanisms: Employed Django's messaging framework to display error messages and warnings, improving user communication.

- Bug Fixes
    - Template Adjustments: Ensured that all templates, especially partials and the print template, are correctly referencing context variables and are free from deprecated code or unnecessary inclusions.
    - Field Display Logic: Resolved issues where certain fields were not displaying correctly due to misconfigurations in the `enabled_fields` logic.

- Notes
    - Model Assumptions: Adjusted the codebase to accommodate models that include a date field used for filtering in report generation. Users should ensure that their models have an appropriate date field or adjust the code accordingly.
    - Extensibility: Laid the groundwork for future enhancements, such as asynchronous report generation, emailing reports, and advanced filtering options.

#### Known Issues
- Date Range Limitations: The current implementation only supports date filtering based on a single date field. Future iterations may include support for multiple date fields or custom date ranges.  A Date Range is required for the report to be generated.
- Styling Consistency: While the generated PDFs are styled consistently, the list view and modal overlay may require further styling adjustments for a more polished appearance.
- CSS Issues: Currently, the inline CSS is limited to basic styling. Future improvements may include more advanced styling options for users to customize their reports further.

#### Deleted
- Removed the admin-based configuration for field, model, app, and action configurations. These configurations are now handled directly within the models themselves.

#### Future Work
- Advanced Filtering: Enhance the date range selection to include custom date ranges and support multiple date fields for filtering.
- Asynchronous Generation: Implement asynchronous report generation to improve performance and user experience.
- Email Integration: Allow users to email generated reports directly from the application.
- Custom Styling: Provide users with additional styling options to customize the appearance of their reports.
- User Preferences: Save user preferences for report generation settings to streamline the process for frequent users.
- Additional Output Formats: Support additional output formats such as CSV, Excel, or HTML for generated reports.
- Orientation and Layout: Allow users to select the orientation and layout of the generated PDF reports for better readability.


## [0.4.0] - 09-15-2024
### Changed
- Create Changelog
- Transition from admin based configuration to a written configuration inside of the models

### Deprecated
- All of the admin based configuration (will be removed in 0.5.0)
    - FieldConfiguration
    - ModelConfiguration
    - AppConfiguration
    - ActionConfiguration
