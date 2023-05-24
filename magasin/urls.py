from django.urls import path
from . import views
from .views import CategoryAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('mesProduits/', views.mesProduits, name='mesProduits'),
    path('fournisseur_list/', views.fournisseur_list, name='fournisseur_list'),
    path('commande/', views.passer_commande, name='commande'),
    path('register/',views.register, name = 'register'),
    path('api/categorie/', CategoryAPIView.as_view()),
    path('api/produits/', views.ProduitAPIView.as_view()),
   # path('api/produit/<int:categorie>', views.ProduitAPIView.as_view()),
]

