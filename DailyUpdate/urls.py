from django.urls import path, include
from django.conf.urls import url
from DailyUpdate import views
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    url(r'homepage', views.show_homepage),
    url(r'import_data', views.import_newest_data),
    url(r'import_location', views.import_coordinate),
    url(r'delete', views.delete_data),
    url(r'query', views.query_data),
    url(r'charts', views.draw_charts)

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
