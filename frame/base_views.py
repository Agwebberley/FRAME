from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from frame.models import LogMessage
from frame.utils import (
    get_enabled_fields,
    generate_dynamic_form,
    get_child_models,
)
from frame.mixins import (
    NavigationMixin,
    ReportMixin,
    FormsetMixin,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q


class BaseCreateView(LoginRequiredMixin, NavigationMixin, FormsetMixin, CreateView):
    """
    Base view for creating model instances with dynamic form generation.
    """

    template_name = "form.html"

    def get_form_class(self):
        """
        Dynamically get the form class based on the model.

        :return: Form class for the model.
        :rtype: class
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
        :rtype: dict
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
    """

    template_name = "form.html"

    def get_form_class(self):
        """
        Dynamically get the form class based on the model.

        :return: Form class for the model.
        :rtype: class
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
        :rtype: dict
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
    """

    template_name = "list.html"
    report_template_name = "reports/list.html"
    date_range = True
    paginate_by = 10
    date_field = "created_at"
    orientation = "landscape"
    allow_orientation_selection = True

    def get_queryset(self):
        """
        Get the queryset for the view, applying search and sorting.
        """
        queryset = self.model.objects.all()
        search_query = self.request.GET.get("search", "")
        if search_query:
            q_objects = Q()
            for field in get_enabled_fields(
                self.model._meta.app_label,
                self.model.__name__,
                self.request.user,
                view_type="list",
                properties=False,
            ):
                if not self.model._meta.get_field(field).is_relation:
                    q_objects |= Q(**{field + "__icontains": search_query})
                else:
                    q_objects |= Q(**{field + "__name__icontains": search_query})
            queryset = queryset.filter(q_objects)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.
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
        print("Search Query: " + context["search_query"])
        context["model_class"] = self.model
        context["date_range"] = self.date_range
        context["allow_orientation_selection"] = self.allow_orientation_selection
        context["orientation"] = self.orientation

        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Render the response, using a partial template if the request is an HTMX request.
        """
        if self.request.htmx:
            return render(self.request, "partials/table_container.html", context)
        return super().render_to_response(context, **response_kwargs)


class BaseDetailView(
    LoginRequiredMixin, ReportMixin, NavigationMixin, FormsetMixin, DetailView
):
    """
    Base view for displaying details of a model instance.
    """

    template_name = "detail.html"
    report_template_name = "reports/detail.html"
    date_range = False
    orientation = "portrait"
    allow_orientation_selection = True

    def get_report_context_data(self, **kwargs):
        context = super().get_report_context_data(**kwargs)
        context["enabled_fields"] = getattr(
            self, "selected_fields", context["enabled_fields"]
        )
        # Add any additional context specific to the detail report
        return context

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context["enabled_fields"] = get_enabled_fields(
            self.object._meta.app_label,
            self.object._meta.model_name,
            self.request.user,
            view_type="detail",
        )

        parent_model = self.object.__class__
        child_models = get_child_models(
            app_name=parent_model._meta.app_label, model_name=parent_model.__name__
        )
        child_instances = []
        for child_model in child_models:
            related_name = child_model._meta.model_name + "_set"
            child_objects = getattr(self.object, related_name).all()
            child_instances.append(
                {
                    "name": child_model._meta.verbose_name_plural,
                    "objects": child_objects,
                    "fields": get_enabled_fields(
                        child_model._meta.app_label,
                        child_model.__name__,
                        self.request.user,
                        view_type="list",
                    ),
                }
            )

        context["child_instances"] = child_instances

        context["model_class"] = self.object.__class__
        context["date_range"] = self.date_range
        context["allow_orientation_selection"] = self.allow_orientation_selection
        context["orientation"] = self.orientation

        return context


class BaseDeleteView(LoginRequiredMixin, NavigationMixin, DeleteView):
    """
    Base view for deleting model instances with confirmation.
    """

    template_name = "confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context["return_url"] = self.model.__name__.lower() + "-list"
        return context


class HomeView(NavigationMixin, View):
    """
    Temporary home view. Will be replaced with a dashboard.
    """

    template_name = "home.html"

    def get(self, request):
        """
        Handle GET request for the view.

        :param request: HTTP request object.
        :return: Rendered home page.
        :rtype: HttpResponse
        """
        return render(request, self.template_name, self.get_context_data())


class LoginView(LoginView):
    """
    View for handling user login.
    """

    template_name = "form.html"
    next_page = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        context["saveOveride"] = "Login"
        context["hOveride"] = "Login"
        return context


class LogoutView(LogoutView):
    """
    View for handling user logout.
    """

    next_page = reverse_lazy("home")
    template_name = "home.html"


class LogMessageView(BaseListView):
    """
    View for listing log messages.
    """

    model = LogMessage


class LogMessageDetailView(BaseDetailView):
    """
    View for displaying details of a log message.
    """

    model = LogMessage
