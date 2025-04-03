from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('courses/', include('apps.courses.urls')),
    path('ielts/', include('apps.ielts.urls')),
    path('general-english/', include('apps.general_english.urls')),
    path('auth/', include('apps.auths.urls')),
    path('users/', include('apps.users.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

if settings.DEBUG:
    urlpatterns += [
        path("_schema", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger",
        ),
    ]
