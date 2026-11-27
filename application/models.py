from django.db import models


class Stage(models.Model):
    Nom_Prenom = models.CharField(max_length=300)
    entreprise = models.CharField(max_length=300)
    annee = models.IntegerField()
    rapport = models.FileField(upload_to="rapports/", null=True, blank=True)
    presentation = models.FileField(upload_to="presentations/", null=True, blank=True)
    # Texte extrait automatiquement des fichiers à l'import (sert à la recherche par mot-clé)
    rapport_texte = models.TextField(blank=True, default="")
    presentation_texte = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.Nom_Prenom} - {self.entreprise} ({self.annee})"


class Statistique(models.Model):
    total_stages = models.IntegerField()
    stages_par_annee = models.JSONField()
