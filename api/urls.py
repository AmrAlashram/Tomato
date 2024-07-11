from django.urls import path
from .views import *

urlpatterns = [
    ######################## Ristoranti ########################
    path('ristoranti/creare/', creare_un_ristorante, name='creare-un-ristorante'),
    path('ristoranti/aggiornare/<str:nome_di_ristorante>/', aggiornare_un_ristorante, name='aggiornare-un-ristorante'),
    path('ristoranti/eliminare/<str:nome_di_ristorante>/', eliminare_un_ristorante, name='eliminare-un-ristorante'),
    path('ristoranti/', ristoranti_tutti, name='list-ristoranti'),
    path('ristoranti/per-ricetta/<str:nome_di_ricetta>/', ristoranti_per_ricetta, name='ristoranti-per-ricetta'),

    ######################## Ricette ########################
    path('ricette/creare/', creare_una_ricetta, name='creare-una-ricetta'),
    path('ricette/aggiornare/<str:nome_di_ricetta>/', aggiornare_una_ricetta, name='aggiornare-una-ricetta'),
    path('ricette/eliminare/<str:nome_di_ricetta>/', eliminare_una_ricetta, name='eliminare-una-ricetta'),
    path('ricette/', ricette_tutte, name='list-ricette'),
    path('ricette/per-ristorante/<str:nome_di_ristorante>/', ricette_per_ristorante, name='ricette-per-ristorante'),
    path('ricette/per-ingrediente/<str:nome_di_ingrediente>/', ricette_per_ingrediente, name='ricette-per-ingrediente'),

    ######################## Ingredienti ########################
    path('ingredienti/creare/', creare_un_ingrediente, name='creare-un-ingrediente'),
    path('ingredienti/aggiornare/<str:nome_di_ingrediente>/', aggiornare_un_ingrediente, name='aggiornare-un-ingrediente'),
    path('ingredienti/eliminare/<str:nome_di_ingrediente>/', eliminare_un_ingrediente, name='eliminare-un-ingrediente'),
    path('ingredienti/', ingredienti_tutti, name='list-ingredienti'),
    path('ingredienti/per-ricetta/<str:nome_di_ricetta>/', ingredienti_per_ricetta, name='ingredienti-per-ricetta'),
    path('ingredienti/per-ristorante/<str:nome_di_ristorante>/', ingredienti_per_ristorante, name='ingredienti-per-ristorante'),
]