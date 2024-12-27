"""
Module containing core views for the FRAME application.

This module includes a set of base views and utility functions for handling
common patterns in Django applications, such as dynamic form generation,
navigation, and report generation.
"""

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from frame.mixins import (
    FormsetMixin,
    NavigationMixin,
    ReportMixin,
)
from frame.models import LogMessage
from frame.utils import (
    generate_dynamic_form,
    get_editable_fields,
    get_enabled_fields,
)


class BaseCreateView(LoginRequiredMixin, NavigationMixin, FormsetMixin, CreateView):
    """
    Base view for creating model instances with dynamic form generation.

    :param template_name: Path to the template for the create view.
    """

    template_name = "form.html"

    def get_form_class(self):
        """
        Dynamically get the form class based on the model.

        :return: Form class for the model.
        """
        return generate_dynamic_form(
            self.model._meta.app_label,
            self.model.__name__,
            self.request.user,
        )

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        """
        context = super().get_context_data(**kwargs)
        context["enabled_fields"] = get_enabled_fields(
            self.model._meta.app_label,
            self.model.__name__,
            self.request.user,
        )
        if "pk" in context["enabled_fields"]:
            context["enabled_fields"].remove("pk")
        context["return_url"] = self.model.__name__.lower() + "-list"
        context["model_class"] = self.model
        context["verbose_name"] = self.model._meta.verbose_name
        context["verbose_name_plural"] = self.model._meta.verbose_name_plural

        return context


class BaseUpdateView(LoginRequiredMixin, NavigationMixin, FormsetMixin, UpdateView):
    """
    Base view for updating model instances with dynamic form generation.

    :param template_name: Path to the template for the update view.
    """

    template_name = "form.html"

    def get_form_class(self):
        """
        Dynamically get the form class based on the model.

        :return: Form class for the model.
        """
        return generate_dynamic_form(
            self.model._meta.app_label,
            self.model.__name__,
            self.request.user,
        )

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        """
        context = super().get_context_data(**kwargs)
        context["enabled_fields"] = get_enabled_fields(
            self.model._meta.app_label,
            self.model.__name__,
            self.request.user,
        )
        if "pk" in context["enabled_fields"]:
            context["enabled_fields"].remove("pk")
        context["return_url"] = self.model.__name__.lower() + "-list"
        context["model_class"] = self.model
        context["verbose_name"] = self.model._meta.verbose_name
        context["verbose_name_plural"] = self.model._meta.verbose_name_plural
        return context


class BaseListView(LoginRequiredMixin, ReportMixin, NavigationMixin, ListView):
    """
    Base view for listing model instances with search and pagination support,
    and report generation capability.

    :param template_name: Path to the template for the list view.
    :param report_template_name: Path to the template for the report.
    :param date_range: Whether date range filtering is enabled.
    :param paginate_by: Number of items per page.
    :param date_field: Default field for date range filtering.
    :param orientation: Orientation for report generation ('portrait' or 'landscape').
    :param allow_orientation_selection: Whether orientation selection is allowed.
    :param sort_fields: List of fields for sorting.
    """

    template_name = "list.html"
    report_template_name = "reports/list.html"
    date_range = True
    paginate_by = 10
    date_field = "created_at"
    orientation = "landscape"
    allow_orientation_selection = True
    sort_fields = ["pk"]

    def get_queryset(self):
        """
        Get the queryset for the view, applying search and sorting.

        :return: Filtered and sorted queryset.
        """
        queryset = self.model.objects.all()
        search_query = self.request.GET.get("search", "").strip()
        filter_field = self.request.GET.get("filter", "").strip()
        exact_match = self.request.GET.get("exact_match", "").lower() == "true"

        if filter_field and search_query:
            queryset = self.apply_filter(
                queryset, filter_field, search_query, exact_match
            )
        elif search_query:
            queryset = self.apply_global_search(queryset, search_query)

        return queryset

    def apply_filter(self, queryset, filter_field, search_query, exact_match):
        """
        Apply filtering based on a specific filter field and search query.

        :param queryset: The queryset to filter.
        :param filter_field: Field to filter on.
        :param search_query: Search query value.
        :param exact_match: Whether to perform an exact match.
        :return: Filtered queryset.
        """
        filter_condition = (
            {filter_field: search_query}
            if exact_match
            else {f"{filter_field}__icontains": search_query}
        )
        return queryset.filter(Q(**filter_condition))

    def apply_global_search(self, queryset, search_query):
        """
        Apply a global search across all enabled fields.

        :param queryset: The queryset to search.
        :param search_query: Search query value.
        :return: Filtered queryset.
        """
        search_conditions = Q()
        enabled_fields = get_enabled_fields(
            self.model._meta.app_label,
            self.model.__name__,
            self.request.user,
            view_type="list",
            properties=False,
        )
        for field in enabled_fields:
            if self.is_searchable_field(field):
                search_conditions |= Q(**{f"{field}__icontains": search_query})
        return queryset.filter(search_conditions)

    def is_searchable_field(self, field):
        """
        Check if a field is searchable (not a relation).

        :param field: Field name.
        :return: True if the field is searchable, False otherwise.
        """
        field_obj = self.model._meta.get_field(field)
        return not field_obj.is_relation

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        """
        context = super().get_context_data(**kwargs)
        context["enabled_fields"] = get_enabled_fields(
            self.model._meta.app_label,
            self.model.__name__,
            self.request.user,
            view_type="list",
        )
        if "pk" in context["enabled_fields"]:
            context["enabled_fields"].remove("pk")
        context["search_query"] = self.request.GET.get("search", "")
        context["app_label"] = self.model._meta.app_label
        context["model_class"] = self.model
        context["date_range"] = self.date_range
        context["allow_orientation_selection"] = self.allow_orientation_selection
        context["orientation"] = self.orientation
        context["editable_fields"] = get_editable_fields(
            self.model._meta.app_label,
            self.model.__name__,
            self.request.user,
            view_type="list",
        )
        return context


class BaseDetailView(
    LoginRequiredMixin, ReportMixin, NavigationMixin, FormsetMixin, DetailView
):
    """
    Base view for displaying details of a model instance.

    :param template_name: Path to the template for the detail view.
    :param report_template_name: Path to the template for the detail report.
    :param date_range: Whether date range filtering is enabled.
    :param orientation: Orientation for report generation ('portrait' or 'landscape').
    :param allow_orientation_selection: Whether orientation selection is allowed.
    """

    template_name = "detail.html"
    report_template_name = "reports/detail.html"
    date_range = False
    orientation = "portrait"
    allow_orientation_selection = True


class BaseDeleteView(LoginRequiredMixin, NavigationMixin, DeleteView):
    """
    Base view for deleting model instances with confirmation.

    :param template_name: Path to the template for the delete confirmation.
    :param success_url: URL to redirect after a successful delete.
    """

    template_name = "confirm_delete.html"
    success_url = reverse_lazy("home")


class HomeView(NavigationMixin, View):
    """
    Temporary home view. Will be replaced with a dashboard.

    :param template_name: Path to the template for the home view.
    """

    template_name = "home.html"

    def get(self, request):
        """
        Handle GET request for the view.

        :param request: HTTP request object.
        :return: Rendered home page.
        """
        context = self.get_context_data()
        return render(request, self.template_name, context)


class LogMessageView(BaseListView):
    """
    View for listing log messages.

    :param model: The model associated with this view.
    """

    model = LogMessage


class LogMessageDetailView(BaseDetailView):
    """
    View for displaying details of a log message.

    :param model: The model associated with this view.
    """

    model = LogMessage


def update_field(request):
    """
    Handle field update requests.

    :param request: HTTP request object.
    :return: Rendered field fragment or error response.
    """
    if request.method == "POST":
        app_name = request.POST.get("app")
        model_name = request.POST.get("model")
        pk = request.POST.get("pk")
        field = request.POST.get("field")
        value = request.POST.get(field)

        model_class = apps.get_model(app_name, model_name)
        obj = get_object_or_404(model_class, pk=pk)

        if obj._meta.get_field(field).get_internal_type() == "BooleanField":
            value = value == "on"

        setattr(obj, field, value)
        obj.save()

        return render(
            request,
            "partials/editable_field_fragment.html",
            {
                "obj": obj,
                "field": field,
                "value": value,
                "app_label": app_name,
                "model_class": model_class,
            },
        )
    return JsonResponse({"success": False}, status=400)


def edit_field(request):
    """
    Handle field editing requests.

    :param request: HTTP request object.
    :return: Rendered editable field fragment.
    """
    app_label = request.POST.get("app")
    model_name = request.POST.get("model")
    pk = request.POST.get("pk")
    field = request.POST.get("field")

    model = apps.get_model(app_label, model_name)
    obj = get_object_or_404(model, pk=pk)
    field_type = obj._meta.get_field(field).get_internal_type()
    if field_type == "CharField" and obj._meta.get_field(field).choices:
        field_type = "ChoiceField"

    return render(
        request,
        "partials/edit_field_fragment.html",
        {
            "obj": obj,
            "field": field,
            "field_type": field_type,
            "app_label": app_label,
            "model_name": model_name,
        },
    )
