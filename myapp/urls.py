from django.contrib import admin
from django.urls import include, path

urlpatterns = [
  path('textclassification/', include('textclassification.urls')),    
  path('admin/', admin.site.urls),
]
