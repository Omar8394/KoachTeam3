# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from modules.registration import views
from modules.registration.views import enrollment
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    
    path("registration/", include("modules.registration.urls")),
    path("academic/", include("modules.academic.urls")),
    path("communication/", include("modules.communication.urls")),
    path("planning/", include("modules.planning.urls")),
    path("help_app/", include("modules.helping.urls")),
    path("", include("modules.security.urls")),
    
                                                         # Auth routes - login / register
    path('admin/', admin.site.urls),                     # Django admin route
    path("", include("modules.app.urls")),            
       # UI Kits Html files
   
  

]+ static(settings.UPLOAD_URL, document_root=settings.UPLOAD_ROOT)


