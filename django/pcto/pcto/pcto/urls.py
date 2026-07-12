"""
URL configuration for pcto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import (
    homepage, profile, add_progetto, more_info_project,
    page_not_found, display_diario, constactUs
)
from django.contrib.auth import views as auth_views
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


class SafeLoginView(auth_views.LoginView):
    '''
    *   Ok, questa classe la uso per evitare casi di bruteforce.
    *   Una macchina puo' fare max 5 tentativi al minuto.
    *   Se l’IP supera la soglia, il middleware blocca
    *   la richiesta prima ancora che arrivi alla vista,
    *   restituendo direttamente HTTP 429 (Too Many Requests).
    '''
    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', homepage),
    path('profile/', profile, name='profile'),
    path("new_project/", add_progetto),
    path("progetto/n/<int:id_progetto>/", more_info_project, name="more_info_project"),
    path("diario/<int:diario_id>/", display_diario, name="display_diario"),
    path("page_not_found/", page_not_found, name="page_not_found"),
    path("contactUs", constactUs),
    # sistema login / logout
    path('login/', SafeLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # sistema recupero password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
