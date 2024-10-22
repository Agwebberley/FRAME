from django.apps import apps
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.shortcuts import redirect
from django.contrib import messages


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
    orientation = "portrait"  # Default orientation ('portrait' or 'landscape')
    allow_orientation_selection = False  # Allow user to select orientation

    def get_report_context_data(self, **kwargs):
        """
        Get context data for the report.
        Override this method to provide additional context.
        """
        context = self.get_context_data(**kwargs)
        context["report_title"] = self.report_title
        context["date_range"] = self.date_range
        context["enabled_fields"] = getattr(
            self, "selected_fields", context.get("enabled_fields", [])
        )
        context["orientation"] = self.orientation
        context["allow_orientation_selection"] = self.allow_orientation_selection
        return context

    def generate_pdf(self, context):
        """
        Generate PDF from the report template and context.
        """
        html_string = render_to_string(self.report_template_name, context)

        # Determine the orientation CSS
        orientation_css = "@page { size: A4 %s; }" % self.orientation

        # Create a CSS object with the orientation
        css = CSS(string=orientation_css)

        # Generate PDF with the orientation CSS
        html = HTML(string=html_string)
        pdf_file = html.write_pdf(stylesheets=[css])
        return pdf_file

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for report generation.
        """
        # Check if this is a report generation request
        if "generate_report" in request.POST:
            # Get the report title if provided
            self.report_title = request.POST.get("report_title", self.report_title)

            # Set self.object if applicable (for DetailView)
            if hasattr(self, "get_object"):
                self.object = self.get_object()

            # Set self.object_list if applicable (for ListView)
            if hasattr(self, "get_queryset"):
                self.object_list = self.get_queryset()

                # Get additional data if needed (e.g., date range)
                if self.date_range:
                    self.start_date = request.POST.get("start_date")
                    self.end_date = request.POST.get("end_date")

                    # Validate date inputs
                    if self.start_date and self.end_date:
                        if self.start_date > self.end_date:
                            messages.error(
                                request, "Start date cannot be after end date."
                            )
                            return redirect(request.path)
                        else:
                            # Apply date range filtering to the queryset
                            date_field_name = getattr(
                                self, "date_field", "date_field"
                            )  # Replace 'date_field' with your actual date field
                            date_filter = {
                                f"{date_field_name}__range": [
                                    self.start_date,
                                    self.end_date,
                                ]
                            }
                            self.object_list = self.object_list.filter(**date_filter)
                    else:
                        messages.error(
                            request, "Please provide both start and end dates."
                        )
                        return redirect(request.path)

            # Get selected fields if applicable
            selected_fields = request.POST.getlist("fields")
            if selected_fields:
                self.selected_fields = selected_fields

            # Get orientation if allowed and provided
            if self.allow_orientation_selection:
                orientation = request.POST.get("orientation", self.orientation)
                if orientation in ["portrait", "landscape"]:
                    self.orientation = orientation
                else:
                    messages.error(request, "Invalid orientation selected.")
                    return redirect(request.path)

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


class FormsetMixin:
    """
    Mixin to handle formsets in create and update views.
    """

    def get_formsets(self):
        """
        Return a list of formsets.
        Override this method to provide formsets.
        """
        return []

    def form_valid(self, form):
        """
        Called when form is valid. Saves formsets.
        """
        response = super().form_valid(form)
        formsets = self.get_formsets()
        for formset in formsets:
            formset.instance = self.object
            formset.save()
        return response

    def form_invalid(self, form):
        """
        Called when form is invalid. Re-renders form with errors.
        """
        formsets = self.get_formsets()
        context = self.get_context_data(form=form, formsets=formsets)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Include formsets in context.
        """
        context = super().get_context_data(**kwargs)
        if "formsets" not in context:
            context["formsets"] = self.get_formsets()
        return context
