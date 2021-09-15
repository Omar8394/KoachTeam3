# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),                     # Django admin route
    path("", include("modules.security.urls")),    # Auth routes - login / register
    path("", include("modules.app.urls")),               # UI Kits Html files
    path("", include("modules.academic.urls")),
    path("", include("modules.communication.urls")),
    path("", include("modules.planning.urls")),
    path("", include("modules.registration.urls")),
    path("", include("modules.security.urls")),
]
