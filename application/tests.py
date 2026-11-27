from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .extraction import extract_text
from .models import Stage


def make_stage(**kw):
    data = dict(Nom_Prenom="Alice Test", entreprise="Acme", annee=2024)
    data.update(kw)
    return Stage.objects.create(**data)


class PagesTests(TestCase):
    def test_pages_load(self):
        for name in ["accueil", "liste_stages", "recherche_stages", "importer_fichier", "statistiques"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_statistics_are_computed_from_database(self):
        make_stage(annee=2023)
        make_stage(annee=2024, entreprise="Beta")
        make_stage(annee=2024)
        response = self.client.get(reverse("statistiques"))
        self.assertEqual(response.context["total_stages"], 3)
        by_year = {row["annee"]: row["n"] for row in response.context["stages_par_annee"]}
        self.assertEqual(by_year, {2023: 1, 2024: 2})


class SearchTests(TestCase):
    def test_keyword_search_in_extracted_text(self):
        make_stage(Nom_Prenom="A", rapport_texte="Clause SLA de disponibilité 99,9 %")
        make_stage(Nom_Prenom="B", rapport_texte="Autre sujet")
        response = self.client.get(reverse("recherche_stages"), {"q": "sla"})
        names = [s.Nom_Prenom for s in response.context["filter"].qs]
        self.assertEqual(names, ["A"])

    def test_partial_name_search(self):
        make_stage(Nom_Prenom="Yassine Ahrimch")
        response = self.client.get(reverse("recherche_stages"), {"Nom_Prenom": "ahri"})
        self.assertEqual(response.context["filter"].qs.count(), 1)


class DeleteTests(TestCase):
    def test_delete_requires_post(self):
        stage = make_stage()
        url = reverse("supprimer_stage", args=[stage.id])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(Stage.objects.count(), 1)
        self.client.post(url)
        self.assertEqual(Stage.objects.count(), 0)

    def test_delete_unknown_returns_404(self):
        response = self.client.post(reverse("supprimer_stage", args=[9999]))
        self.assertEqual(response.status_code, 404)


class ExtractionTests(TestCase):
    def test_unreadable_file_returns_empty_string(self):
        fake = SimpleUploadedFile("cassé.pdf", b"ceci n'est pas un pdf")
        self.assertEqual(extract_text(fake), "")

    def test_unsupported_extension_returns_empty_string(self):
        self.assertEqual(extract_text(SimpleUploadedFile("note.txt", b"bonjour")), "")
