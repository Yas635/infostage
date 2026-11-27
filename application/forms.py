from pathlib import Path

from django import forms
from django.conf import settings

from .models import Stage

RAPPORT_EXT = {".pdf", ".docx"}
PRESENTATION_EXT = {".pdf", ".pptx", ".docx"}


def _check(file, allowed):
    if not file:
        return file
    if Path(file.name).suffix.lower() not in allowed:
        raise forms.ValidationError("Format accepté : " + ", ".join(sorted(allowed)))
    if file.size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise forms.ValidationError(f"Fichier trop volumineux (max {settings.MAX_UPLOAD_SIZE_MB} Mo).")
    return file


class ImportationFichierForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ["Nom_Prenom", "entreprise", "annee", "rapport", "presentation"]

    def clean_rapport(self):
        return _check(self.cleaned_data.get("rapport"), RAPPORT_EXT)

    def clean_presentation(self):
        return _check(self.cleaned_data.get("presentation"), PRESENTATION_EXT)
