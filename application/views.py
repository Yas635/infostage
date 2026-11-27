from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .extraction import extract_text
from .filters import StageFilter
from .forms import ImportationFichierForm
from .models import Stage


def accueil(request):
    return render(request, "index.html")


def importer_fichier(request):
    if request.method == "POST":
        form = ImportationFichierForm(request.POST, request.FILES)
        if form.is_valid():
            stage = form.save(commit=False)
            # Extraction automatique du texte (PDF / Word) pour la recherche par mot-clé
            if form.cleaned_data.get("rapport"):
                stage.rapport_texte = extract_text(form.cleaned_data["rapport"])
            if form.cleaned_data.get("presentation"):
                stage.presentation_texte = extract_text(form.cleaned_data["presentation"])
            stage.save()
            return redirect("liste_stages")
    else:
        form = ImportationFichierForm()
    return render(request, "importer_fichier.html", {"form": form})


def liste_stages(request):
    stages = Stage.objects.order_by("-annee", "Nom_Prenom")
    return render(request, "liste_stages.html", {"stages": stages})


def recherche_stages(request):
    stage_filter = StageFilter(request.GET, queryset=Stage.objects.order_by("-annee", "Nom_Prenom"))
    return render(request, "recherche_stages.html", {"filter": stage_filter})


@require_POST  # une suppression ne doit jamais se faire par simple lien (GET)
def supprimer_stage(request, stage_id):
    get_object_or_404(Stage, pk=stage_id).delete()
    return redirect("liste_stages")


def statistiques(request):
    context = {
        "total_stages": Stage.objects.count(),
        "stages_par_annee": Stage.objects.values("annee").annotate(n=Count("id")).order_by("-annee"),
        "stages_par_entreprise": (
            Stage.objects.values("entreprise").annotate(n=Count("id")).order_by("-n", "entreprise")[:10]
        ),
    }
    return render(request, "statistiques.html", context)
