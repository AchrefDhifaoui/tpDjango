from django.db import models
from datetime import date
class Categorie(models.Model):
    TYPE_CHOICES = [
        ('Al', 'Alimentaire'),
        ('Mb', 'Meuble'),
        ('Sn', 'Sanitaire'),
        ('Vs', 'Vaisselle'),
        ('Vt', 'Vêtement'),
        ('Jx', 'Jouets'),
        ('Lg', 'Linge de Maison'),
        ('Bj', 'Bijoux'),
        ('Dc', 'Décor'),
        ('El', 'Electroménager'),
        ('Fr', 'Frais')
    ]
    name = models.CharField(max_length=50, default='Alimentaire')
    category_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='Al')

    def __str__(self):
        return f"{self.name} ({self.category_type})"


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField(default='')
    email = models.EmailField(default='')
    telephone = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.nom} ({self.adresse}) : {self.email} ({self.telephone})"

class Produit(models.Model):
    TYPE_CHOICES=[('fr','frais'),('cs','conserve'),('em','emballe')]
    libelle = models.CharField(max_length=100)
    description = models.TextField(default='non  definie')
    prix = models.DecimalField(max_digits=10,decimal_places=3,default=0.000)
    type = models.CharField(max_length=10,choices=TYPE_CHOICES,default='em')
    Img = models.ImageField(blank=True)
    catégorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.libelle} ({self.type}) : {self.description} ({self.prix}€)"

class ProduitNC(Produit):
        duree_garantie = models.CharField(max_length=100)

        def __str__(self):
            return f"({self.libelle} ({self.description}) - {self.prix}$ - {self.type} - {self.duree_garantie})"

class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    produits = models.ManyToManyField('Produit')

    def __str__(self):
        return f"Commande {self.id} ({self.dateCde}) : {self.totalCde}€"
