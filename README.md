# InfoStage : archivage et recherche des rapports de stage

Application web Django pour **archiver les stages d'une école** : on importe le rapport et la présentation de chaque stagiaire, le **texte est extrait automatiquement** (PDF et Word), puis on peut **rechercher par nom, entreprise, année ou mot-clé** dans le contenu des rapports et consulter des **statistiques**.

## Fonctionnalités

- Import d'un stage : nom, entreprise, année, rapport (PDF/DOCX) et présentation (PDF/PPTX/DOCX), avec contrôle du format et de la taille
- **Extraction automatique du texte** des PDF (pdfminer.six) et des documents Word (python-docx) à l'import
- Recherche multicritères : nom, entreprise, année, et **mot-clé dans le contenu des rapports**
- Liste des stages, suppression sécurisée (requête POST avec confirmation)
- Statistiques calculées à partir de la base : total, stages par année, stages par entreprise

## Installation

```bash
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # puis adaptez les valeurs
python manage.py migrate
python manage.py createsuperuser  # facultatif : accès à /admin
python manage.py runserver
```

Ouvrez http://127.0.0.1:8000. Tests : `python manage.py test`.

## Structure

```
projetstage/            configuration Django (variables d'environnement)
application/
├── extraction.py       extraction du texte des PDF et Word
├── models.py           Stage (avec texte extrait), Statistique
├── views.py            import, liste, recherche, suppression, statistiques
├── filters.py          filtres de recherche (dont mot-clé)
├── forms.py            formulaire d'import avec validation
├── templates/          pages HTML (Bootstrap)
└── tests.py            tests
```

## Limites et pistes d'amélioration

- L'extraction ne gère pas les PDF scannés (images) : il faudrait ajouter de l'OCR.
- Les présentations PowerPoint (.pptx) sont acceptées mais leur texte n'est pas extrait.
- Pas d'authentification : à ajouter avant tout usage réel (les rapports peuvent contenir des données personnelles).
- Pistes : recherche plein texte plus avancée (PostgreSQL ou SQLite FTS), OCR, graphiques dans les statistiques.

## Auteurs

Omar Benghannou et Yassine Ahrimch.
