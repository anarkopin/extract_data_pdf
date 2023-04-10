from django.urls import path

from . import apis

urlpatterns = [
    path("extract_data/", apis.extract_data_pdf.as_view(), name="extract data pdf"),
    path("get_data/", apis.getDataProccess.as_view(), name="get data pdf"),
]