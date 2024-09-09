from django.http import JsonResponse
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.apps import apps
from frame.models import ModelConfiguration, AppConfiguration, LogMessage
from frame.utils import (
    generate_inline_formset,
    get_enabled_fields,
    generate_dynamic_form,
    get_actions,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q


def nav_helper():
    """
    Helper function to retrieve applications and their models that have navigation enabled.

    :return: Dictionary of apps and their corresponding models with navigation enabled.
    :rtype: dict
    """
    apps = AppConfiguration.objects.filter(navigation_enabled=True)

    apps_with_models = {}

    for app in apps:
        models = ModelConfiguration.objects.filter(app=app, navigation_enabled=True)
        apps_with_models[app] = models

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
        return context


class BaseCreateView(LoginRequiredMixin, NavigationMixin, CreateView):
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
        model_config = get_object_or_404(
            ModelConfiguration, model_name=self.model.__name__
        )
        return generate_dynamic_form(
            model_config.app.name, model_config.model_name, self.request.user
        )

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(
            ModelConfiguration, model_name=self.model.__name__
        )
        context["config"] = model_config
        context["enabled_fields"] = get_enabled_fields(
            model_config.app.name, model_config.model_name, self.request.user
        )
        if "pk" in context["enabled_fields"]:
            context["enabled_fields"].remove("pk")
        context["return_url"] = model_config.model_name.lower() + "-list"

        return context


class BaseUpdateView(LoginRequiredMixin, NavigationMixin, UpdateView):
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
        model_config = get_object_or_404(
            ModelConfiguration, model_name=self.model.__name__
        )
        return generate_dynamic_form(
            model_config.app.name, model_config.model_name, self.request.user
        )

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(
            ModelConfiguration, model_name=self.model.__name__
        )
        context["config"] = model_config
        context["enabled_fields"] = get_enabled_fields(
            model_config.app.name, model_config.model_name, self.request.user
        )
        if "pk" in context["enabled_fields"]:
            context["enabled_fields"].remove("pk")
        context["return_url"] = model_config.model_name.lower() + "-list"
        return context


class BaseListView(LoginRequiredMixin, NavigationMixin, ListView):
    """
    Base view for listing model instances with search and pagination support.
    """

    template_name = "list.html"
    paginate_by = 10

    def get_queryset(self):
        """
        Get the queryset for the view, applying search and sorting.

        :return: Queryset of model instances.
        :rtype: QuerySet
        """
        model_config = get_object_or_404(
            ModelConfiguration, model_name=self.model.__name__
        )
        queryset = self.model.objects.all()
        search_query = self.request.GET.get("query", "")
        if search_query:
            q_objects = Q()
            for field in get_enabled_fields(
                model_config.app.name,
                model_config.model_name,
                self.request.user,
                view_type="list",
                properties=False,
            ):
                if not self.model._meta.get_field(field).is_relation:
                    q_objects |= Q(**{field + "__icontains": search_query})
                else:
                    q_objects |= Q(**{field + "__name__icontains": search_query})
            queryset = queryset.filter(q_objects)
        if model_config.default_sort_by:
            queryset = queryset.order_by(model_config.default_sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(
            ModelConfiguration, model_name=self.model.__name__
        )
        context["config"] = model_config
        context["enabled_fields"] = get_enabled_fields(
            model_config.app.name,
            model_config.model_name,
            self.request.user,
            view_type="list",
        )
        if "pk" in context["enabled_fields"]:
            context["enabled_fields"].remove("pk")
        context["actions"] = get_actions(model_config.app.name, model_config.model_name)
        context["search_query"] = self.request.GET.get("query", "")
        context["model_class"] = self.model
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Render the response, using a partial template if the request is an HTMX request.

        :param context: Context data for the view.
        :param response_kwargs: Additional response arguments.
        :return: HttpResponse object.
        :rtype: HttpResponse
        """
        if self.request.htmx:
            return render(self.request, "partials/table_container.html", context)
        return super().render_to_response(context, **response_kwargs)


class BaseDetailView(LoginRequiredMixin, NavigationMixin, DetailView):
    """
    Base view for displaying details of a model instance.
    """

    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(
            ModelConfiguration, model_name=self.model.__name__
        )
        context["config"] = model_config
        context["enabled_fields"] = get_enabled_fields(
            model_config.app.name,
            model_config.model_name,
            self.request.user,
            view_type="detail",
        )
        context["actions"] = get_actions(
            model_config.app.name, model_config.model_name, view_type="detail"
        )

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


class BaseMasterDetailView(LoginRequiredMixin, NavigationMixin, DetailView):
    """
    Base view for displaying details of a parent model instance along with its child instances.
    """

    template_name = "master_detail.html"

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        :param kwargs: Additional context data.
        :return: Context data with additional information.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        model_config = get_object_or_404(
            ModelConfiguration, model_name=self.model.__name__
        )
        context["config"] = model_config
        context["enabled_fields"] = get_enabled_fields(
            model_config.app.name,
            model_config.model_name,
            self.request.user,
            view_type="detail",
        )
        parent_model = self.model
        child_models = [
            rel.related_model
            for rel in parent_model._meta.related_objects
            if rel.one_to_many
        ]

        child_instances = []
        for child_model in child_models:
            child_instances.append(
                {
                    "name": child_model._meta.verbose_name_plural,
                    "objects": child_model.objects.filter(
                        **{parent_model._meta.model_name + "_id": self.object.pk}
                    ),
                    "fields": get_enabled_fields(
                        model_config.app.name,
                        child_model.__name__,
                        self.request.user,
                        view_type="list",
                    ),
                }
            )

        context["child_instances"] = child_instances
        context["actions"] = get_actions(
            model_config.app.name, model_config.model_name, view_type="detail"
        )

        return context


class MasterDetailBaseView(LoginRequiredMixin, NavigationMixin):
    """
    Base view for handling master-detail relationships with formsets.
    """

    template_name = "master_detail_form.html"
    success_url = reverse_lazy("home")

    def get_parent_and_child_models(self, app_label, model_name):
        """
        Get the parent and child models based on the app label and model name.

        :param app_label: App label of the parent model.
        :param model_name: Name of the parent model.
        :return: Tuple containing the parent model and a list of child models.
        :rtype: tuple
        """
        parent_model = apps.get_model(app_label, model_name)
        child_models = [
            rel.related_model
            for rel in parent_model._meta.related_objects
            if rel.one_to_many
        ]
        return parent_model, child_models

    def get_parent_form(self, app_label, model_name, instance=None):
        """
        Get the parent form based on the app label and model name.

        :param app_label: App label of the parent model.
        :param model_name: Name of the parent model.
        :param instance: Instance of the parent model (optional).
        :return: Form class for the parent model.
        :rtype: class
        """
        model_config = get_object_or_404(ModelConfiguration, model_name=model_name)
        if instance:
            form = generate_dynamic_form(
                model_config.app.name, model_config.model_name, self.request.user
            )
            return form(
                data=self.request.POST if self.request.method == "POST" else None,
                instance=instance,
            )
        else:
            return generate_dynamic_form(
                model_config.app.name, model_config.model_name, self.request.user
            )

    def get_child_formsets(self, app_label, parent_model, child_models, instance=None):
        """
        Get the formsets for the child models based on the parent model.

        :param app_label: App label of the parent model.
        :param parent_model: Parent model class.
        :param child_models: List of child model classes.
        :param instance: Instance of the parent model (optional).
        :return: List of formsets for the child models.
        :rtype: list
        """
        formsets = []
        for child_model in child_models:
            child_model_config = get_object_or_404(
                ModelConfiguration, model_name=child_model.__name__
            )
            formset_class = generate_inline_formset(
                child_model_config.app.name,
                parent_model,
                child_model,
                child_model_config.model_name,
                self.request.user,
            )
            if instance:
                formset = formset_class(
                    self.request.POST if self.request.method == "POST" else None,
                    instance=instance,
                )
            else:
                formset = formset_class(
                    self.request.POST if self.request.method == "POST" else None
                )
            formsets.append((child_model._meta.verbose_name_plural, formset))
        return formsets

    def render_form(self, parent_form, child_formsets, app_label, model_name):
        """
        Render the form for the parent and child models.

        :param parent_form: Form instance for the parent model.
        :param child_formsets: List of formsets for the child models.
        :param app_label: App label of the parent model.
        :param model_name: Name of the parent model.
        :return: Rendered form.
        :rtype: HttpResponse
        """
        model_config = get_object_or_404(ModelConfiguration, model_name=model_name)
        context = {
            "parent_form": parent_form,
            "child_formsets": child_formsets,
            "model_name": model_name,
            "app_label": app_label,
            "return_url": model_name.lower() + "-list",
            "apps": nav_helper(),
            "config": model_config,
        }
        return render(self.request, self.template_name, context)

    def handle_post(self, parent_form, child_formsets):
        """
        Handle the POST request for the form submission.

        :param parent_form: Form instance for the parent model.
        :param child_formsets: List of formsets for the child models.
        :return: HttpResponse object.
        :rtype: HttpResponse
        """
        if isinstance(parent_form, type):
            parent_form = parent_form(data=self.request.POST)

        formset_valid = all(formset.is_valid() for _, formset in child_formsets)

        if parent_form.is_valid() and formset_valid:
            parent_instance = parent_form.save()
            for _, formset in child_formsets:
                formset.instance = parent_instance
                formset.save()
            return redirect(self.success_url)

        return self.render_form(
            parent_form,
            child_formsets,
            self.kwargs["app_label"],
            self.kwargs["model_name"],
        )


class MasterDetailCreateView(MasterDetailBaseView, CreateView):
    """
    View for creating a master-detail form with parent and child models.
    """

    def get(self, request, app_label, model_name):
        """
        Handle GET request for the view.

        :param request: HTTP request object.
        :param app_label: App label of the parent model.
        :param model_name: Name of the parent model.
        :return: Rendered form for the view.
        :rtype: HttpResponse
        """
        parent_model, child_models = self.get_parent_and_child_models(
            app_label, model_name
        )
        parent_form = self.get_parent_form(app_label, parent_model.__name__)
        child_formsets = self.get_child_formsets(app_label, parent_model, child_models)
        return self.render_form(
            parent_form, child_formsets, app_label, parent_model.__name__
        )

    def post(self, request, app_label, model_name):
        """
        Handle POST request for the view.

        :param request: HTTP request object.
        :param app_label: App label of the parent model.
        :param model_name: Name of the parent model.
        :return: Redirect or rendered form based on validation.
        :rtype: HttpResponse
        """
        parent_model, child_models = self.get_parent_and_child_models(
            app_label, model_name
        )
        parent_form = self.get_parent_form(app_label, parent_model.__name__)
        child_formsets = self.get_child_formsets(app_label, parent_model, child_models)
        return self.handle_post(parent_form, child_formsets)


class MasterDetailUpdateView(MasterDetailBaseView, UpdateView):
    """
    View for updating a master-detail form with parent and child models.
    """

    def get(self, request, app_label, model_name, pk):
        """
        Handle GET request for the view.

        :param request: HTTP request object.
        :param app_label: App label of the parent model.
        :param model_name: Name of the parent model.
        :param pk: Primary key of the parent model instance.
        :return: Rendered form for the view.
        :rtype: HttpResponse
        """
        parent_model, child_models = self.get_parent_and_child_models(
            app_label, model_name
        )
        instance = get_object_or_404(parent_model, pk=pk)
        parent_form = self.get_parent_form(
            app_label, parent_model.__name__, instance=instance
        )
        child_formsets = self.get_child_formsets(
            app_label, parent_model, child_models, instance=instance
        )
        return self.render_form(
            parent_form, child_formsets, app_label, parent_model.__name__
        )

    def post(self, request, app_label, model_name, pk):
        """
        Handle POST request for the view.

        :param request: HTTP request object.
        :param app_label: App label of the parent model.
        :param model_name: Name of the parent model.
        :param pk: Primary key of the parent model instance.
        :return: Redirect or rendered form based on validation.
        :rtype: HttpResponse
        """
        parent_model, child_models = self.get_parent_and_child_models(
            app_label, model_name
        )
        instance = get_object_or_404(parent_model, pk=pk)
        parent_form = self.get_parent_form(
            app_label, parent_model.__name__, instance=instance
        )
        child_formsets = self.get_child_formsets(
            app_label, parent_model, child_models, instance=instance
        )
        return self.handle_post(parent_form, child_formsets)


class HomeView(NavigationMixin, View):
    """
    View for rendering the home page.
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


class AddFormsetRowView(View):
    """
    View to dynamically add a formset row for inline forms.
    """

    def post(self, request, app_label, model_name):
        """
        Handle POST request to add a formset row.

        :param request: HTTP request object.
        :param app_label: App label of the parent model.
        :param model_name: Name of the parent model.
        :return: JSON response with the new formset row HTML.
        :rtype: JsonResponse
        """
        parent_model = apps.get_model(app_label, model_name)
        child_model_name = request.POST.get("child_model_name")
        child_model = apps.get_model(app_label, child_model_name)

        formset_class = generate_inline_formset(parent_model, child_model)
        formset = formset_class()

        form_idx = request.POST.get("form_idx")

        new_form = formset.empty_form
        new_form_html = new_form.as_p().replace("__prefix__", str(form_idx))

        return JsonResponse({"form_html": new_form_html})


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


class TemplateView(TemplateView, NavigationMixin):
    """
    View for rendering a template.
    """

    template_name = "home.html"
