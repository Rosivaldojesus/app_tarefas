
from django.contrib import admin
from django.urls import path,  include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tarefas/', include('apps.tasks.urls', namespace='tasks')),
    path('contas/', include('apps.accounts.urls', namespace='accounts')),
    path('', include('apps.core.urls', namespace='core')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
