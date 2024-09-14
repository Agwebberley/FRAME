from django.conf import settings
from django.apps import apps


def cfg_assets_root(request):
    return {"ASSETS_ROOT": settings.ASSETS_ROOT}


def cfg_version(request):
    return {
        "APP_VERSION": settings.APP_VERSION,
        "FRAME_VERSION": settings.FRAME_VERSION,
    }


def current_app(request):
    func = request.resolver_match.func
    module = func.__module__

    for app in apps.get_app_configs():
        if module.startswith(app.name):
            print(app.label)
            return {"CURRENT_APP": app.label}

    return {"CURRENT_APP": None}
