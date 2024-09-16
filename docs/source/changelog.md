# Changelog

## [0.5.0] - 15-09-2024
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


## [0.4.0] - 15-09-2024
### Changed
- Create Changelog
- Transition from admin based configuration to a written configuration inside of the models

### Deprecated
- All of the admin based configuration (will be removed in 0.5.0)
    - FieldConfiguration
    - ModelConfiguration
    - AppConfiguration
    - ActionConfiguration
