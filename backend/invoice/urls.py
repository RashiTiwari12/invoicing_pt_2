from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("signup/", (SignupView.as_view()), name="user-signup"),
    path("login/", (LoginView.as_view()), name="user-signin"),
    path("invoices/", (InvoiceView.as_view()), name="invoices"),
    path("invoices/new/", (InvoiceView.as_view()), name="post-invoices"),
    path("invoices/<int:id>/", (SpecificInvoice.as_view()), name="post-invoices"),
    path("invoices/<int:invoice_id>/items/", (AddItem.as_view()), name="post-invoices"),
    # path(
    #     "invoices/<int:id>/",
    #     csrf_exempt(SpecificInvoice.as_view()),
    #     name="specific-invoices",
    # ),
    # path(
    #     "invoices/<int:invoice_id>/items",
    #     csrf_exempt(AddItemview.as_view()),
    #     name="add-item",
    # ),
]
