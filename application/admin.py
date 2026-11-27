from django.contrib import admin

from .models import Stage


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("Nom_Prenom", "entreprise", "annee")
    list_filter = ("annee",)
    search_fields = ("Nom_Prenom", "entreprise")
    exclude = ("rapport_texte", "presentation_texte")
