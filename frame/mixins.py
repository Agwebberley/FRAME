from django.apps import apps
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def nav_helper():
    """
    Helper function to retrieve applications and their models that have navigation enabled.

    :return: Dictionary of apps and their corresponding models with navigation enabled.
    :rtype: dict
    """
    apps_with_models = {}
    # Get all apps with navigation enabled
    # Iterate over all apps and get models with navigation enabled
    # Use the model's get_config method to get the configuration
    # NOTE: No longer using AppConfiguration model
    for app in apps.get_app_configs():
        models_with_nav = []
        for model in app.get_models():
            # Check if get_config method exists
            if not hasattr(model, "get_config"):
                continue
            model_config = model.get_config()
            if model_config["navigation"]:
                models_with_nav.append(
                    {
                        "name": model.get_config()["model_name"],
                        "plural": model._meta.verbose_name_plural,
                        "url": model.__name__.lower() + "-list",
                    }
                )
        if models_with_nav:
            apps_with_models[app.label] = {
                "name": app.verbose_name,
                "models": models_with_nav,
            }
    return apps_with_models


class NavigationMixin:
    """
    Mixin to add navigation context to views.
    """

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view, adding navigation information.

        :param kwargs: Additional context data.
        :return: Context data with navigation information.
        :rtype: dict
        """
        if hasattr(super(), "get_context_data"):
            context = super().get_context_data(**kwargs)
        else:
            context = {}

        apps_with_models = nav_helper()

        context["apps"] = apps_with_models
        context["current_app"] = self.request.resolver_match.app_name
        return context


class ReportMixin:
    """
    Mixin to add report generation functionality to Django class-based views.
    """

    report_template_name = None  # Template used for generating the report
    report_title = "Report"  # Default report title
    date_range = False  # Flag to indicate if date range is needed

    def get_report_context_data(self, **kwargs):
        """
        Get context data for the report.
        Override this method to provide additional context.
        """
        context = self.get_context_data(**kwargs)
        context["report_title"] = self.report_title
        context["date_range"] = self.date_range
        context["enabled_fields"] = self.selected_fields
        return context

    def generate_pdf(self, context):
        """
        Generate PDF from the report template and context.
        """
        html_string = render_to_string(self.report_template_name, context)
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()
        return pdf_file

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for report generation.
        """
        # Check if this is a report generation request
        if "generate_report" in request.POST:
            # Get the report title if provided
            self.report_title = request.POST.get("report_title", self.report_title)

            if hasattr(self, "get_object"):
                # Get the object if provided
                self.object = self.get_object()

            # Set self.object_list if applicable (for ListView)
            if hasattr(self, "get_queryset"):
                self.object_list = self.get_queryset()

            # Get selected fields if applicable
            selected_fields = request.POST.getlist("fields")
            print("Selected fields: ", selected_fields)
            if selected_fields:
                self.selected_fields = selected_fields

            # Get additional data if needed (e.g., date range)
            if self.date_range:
                self.start_date = request.POST.get("start_date")
                self.end_date = request.POST.get("end_date")
            # Implement any custom logic here

            # Prepare context data
            context = self.get_report_context_data()

            # Generate PDF
            pdf_file = self.generate_pdf(context)

            # Create HTTP response
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="{self.report_title}.pdf"'
            )
            return response

        # If not a report generation request, proceed normally
        return super().post(request, *args, **kwargs)
