from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('inventory.urls'))
]

admin.site.index_title = "Inventory Management"
admin.site.site_header = "Inventory Management Admin"
