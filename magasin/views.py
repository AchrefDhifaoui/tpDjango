from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .models import Produit, Fournisseur
from .forms import ProduitForm, UserRegistrationForm, CommandeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from magasin.models import Categorie
from magasin.serializers import CategorySerializer
from magasin.serializers import ProduitSerializer
@login_required
def accueil(request):
    context = {'val': "Menu Acceuil"}
    return render(request, 'acceuil.html', context)

@login_required
def index(request):
    list = Produit.objects.all()
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        form = ProduitForm()  # créer formulaire vide
    return render(request, 'magasin/majProduits.html', {'form': form, 'list': list})

def mesProduits(request):
    template = loader.get_template('magasin/mesProduits.html')
    products = Produit.objects.all()
    context = {'products': products}
    return render(request, 'magasin/mesProduits.html', context)


def fournisseur_list(request):
    template = loader.get_template('magasin/mesProduits.html')
    fournisseurs = Fournisseur.objects.all()
    context = {'fournisseurs': fournisseurs}
    return render(request, 'magasin/fournisseur_list.html', context)


def passer_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            # Save the order to the database and redirect to a confirmation page
            form.save()
            return redirect('confirmation_commande')
    else:
        form = CommandeForm()
    return render(request, 'magasin/commande.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
class CategoryAPIView(APIView):
  def get(self, *args, **kwargs):
   categories = Categorie.objects.all()
   serializer = CategorySerializer(categories, many=True)
   return Response(serializer.data)

class ProduitAPIView(APIView):
    def get(self, *args, **kwargs):
        produits=Produit.objects.all()
        serializer= ProduitSerializer(produits,many=True)
        return Response(serializer.data)
    
class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduitSerializer
    def get_queryset(self):
        queryset = Produit.objects.all()
        category_id = self.request.GET.get('catégorie')
        if category_id:
            queryset = queryset.filter(catégorie=category_id)
        return queryset



