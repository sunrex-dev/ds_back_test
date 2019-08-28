from django.urls import path, include, re_path
from ..views.rulebook import rulebook_list, rulebook_detail

urlpatterns = [
    # [ルールブック]機能
    # [一覧]
    path('list', rulebook_list.RulebookListView.as_view()),
    # [詳細]
    path('detail/create', rulebook_detail.RulebookDetaiCreatelView.as_view()),
    # 表示・変更・削除
    path('detail/<int:pk>/', rulebook_detail.RulebookDetailView.as_view()),

]
