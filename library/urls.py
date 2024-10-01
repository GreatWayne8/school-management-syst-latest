from django.urls import path
from .views import (
    library_view,
    ebook_list,
    upload_ebook,
    manage_library_view,
    library_categories_view,
    download_ebook,
    ebook_detail,
    edit_ebook,  
    delete_ebook, 
)

urlpatterns = [
    path('', library_view, name='library'), 
    path('manage/', manage_library_view, name='manage_library'), 
    path('categories/', library_categories_view, name='library_categories'),  
    path('category/<int:category_id>/', ebook_list, name='ebook_list_by_category'),
    path('ebooks/', ebook_list, name='all_ebooks'),  
    path('upload/', upload_ebook, name='upload_ebook'),  
    path('download/<int:ebook_id>/', download_ebook, name="download_ebook"),
    path('ebook/<int:ebook_id>/', ebook_detail, name='ebook_detail'),  
    path('edit/<int:ebook_id>/', edit_ebook, name='edit_ebook'), 
    path('delete/<int:ebook_id>/', delete_ebook, name='delete_ebook'),  
]

