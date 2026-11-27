from django.urls import path
from .views import liste_stages, importer_fichier, recherche_stages , accueil ,supprimer_stage ,statistiques
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', accueil, name='accueil'),
    path('liste_stages/', liste_stages, name='liste_stages'),
    path('importer_fichier/', importer_fichier, name='importer_fichier'),
    path('recherche_stages/', recherche_stages, name='recherche_stages'),
    path('supprimer_stage/<int:stage_id>/', supprimer_stage, name='supprimer_stage'),
    path('statistiques/', statistiques , name='statistiques')
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)