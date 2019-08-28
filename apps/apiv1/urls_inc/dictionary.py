from django.urls import path, include, re_path
from ..views.dictionary import dictionary_list

urlpatterns = [
    # [辞書]機能
    # [一覧]
    path('list', dictionary_list.DictionaryListView.as_view()),
    # [詳細]
#    path('detail/create', rulebook_detail.RulebookDetaiCreatelView.as_view()),
    # 表示・変更・削除
#    path('detail/<int:pk>/', rulebook_detail.RulebookDetailView.as_view()),

]
