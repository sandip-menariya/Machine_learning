"""
URL configuration for sent_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
# from . import sent_app

urlpatterns = [
    # The line `from . import sent_app` in the URL configuration file is importing the `sent_app` module
    # from the current package or directory. This allows you to include the URLs defined in the `sent_app`
    # module in the main URL configuration of your Django project. By using `include("sent_app.urls")` in
    # the urlpatterns list, you are including the URLs defined in the `sent_app.urls` file in the main URL
    # patterns of your project. This helps in organizing and modularizing your URL configurations in
    # Django.
    path('admin/', admin.site.urls),
    path('sent_ana/', include("sent_app.urls")),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)