import os
from django.urls import path, re_path
from django.conf.urls.static import static
from django.views.static import serve

from queenBackend import settings
from queenBackend import settings
from .views import (
    CustomLoginView, CustomLogoutView, add_copying, add_customer, add_cv, add_selled_item, add_storage, add_writing,
    all_deliveries, delete_copying, delete_customer, delete_cv, delete_storage, delete_writing, edit_copying,
    edit_cv, edit_writing, index, admin_only_view, view_customers, view_entries,
    add_entry, delete_entry, view_selled_items, view_storage,
)

urlpatterns = [
    path('', index, name='index'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('admin-only/', admin_only_view, name='admin_only'),

    path('entries/', view_entries, name='view_entries'),
    path('entries/add/', add_entry, name='add_entry'),
    path('entries/delete/<int:entry_id>/', delete_entry, name='delete_entry'),

    path('deliveries/', all_deliveries, name='all_deliveries'),
    path('deliveries/add/cv/', add_cv, name='add_cv'),
    path('deliveries/add/writing/', add_writing, name='add_writing'),
    path('deliveries/add/copying/', add_copying, name='add_copying'),
    path('deliveries/delete/cv/<int:cv_id>/', delete_cv, name='delete_cv'),
    path('deliveries/delete/writing/<int:writing_id>/', delete_writing, name='delete_writing'),
    path('deliveries/delete/copying/<int:copying_id>/', delete_copying, name='delete_copying'),
    path('deliveries/edit/cv/<int:cv_id>/', edit_cv, name='edit_cv'),
    path('deliveries/edit/writing/<int:writing_id>/', edit_writing, name='edit_writing'),
    path('deliveries/edit/copying/<int:copying_id>/', edit_copying, name='edit_copying'),

    path('customers/add', add_customer, name='add_customer'),
    path('customers/', view_customers, name='view_customers'),
    path('customers/delete/<int:customer_id>/', delete_customer, name='delete_customer'),

    path('storage/', view_storage, name='view_storage'),
    path('storage/add', add_storage, name='add_storage'),
    path('storage/delete/<int:storage_id>/', delete_storage, name='delete_storage'),

    path('selledItems/', view_selled_items, name='view_selled_items'),
    path('selledItems/add', add_selled_item, name='add_selled_item'),
]

urlpatterns += static('deliveries/', document_root=os.path.join(settings.BASE_DIR, ''))
