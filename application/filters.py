import django_filters
from django.db.models import Q

from .models import Stage


class StageFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_keyword", label="Mot-clé (dans les rapports)")
    Nom_Prenom = django_filters.CharFilter(lookup_expr="icontains", label="Nom Prénom")
    entreprise = django_filters.CharFilter(lookup_expr="icontains", label="Entreprise")

    class Meta:
        model = Stage
        fields = ["annee", "Nom_Prenom", "entreprise"]

    def filter_keyword(self, queryset, name, value):
        value = value.strip()
        if not value:
            return queryset
        return queryset.filter(
            Q(rapport_texte__icontains=value) | Q(presentation_texte__icontains=value)
        )
