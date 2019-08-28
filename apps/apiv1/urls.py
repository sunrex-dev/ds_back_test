from django.urls import path, include

urlpatterns = [
    # [案件カルテ]機能
    path('anken_karte/', include('apps.apiv1.urls_inc.anken_karte')),
    # [ルールブック]機能
    path('rulebook/', include('apps.apiv1.urls_inc.rulebook')),
    # [辞書]機能
    path('dictionary/', include('apps.apiv1.urls_inc.dictionary')),
]
