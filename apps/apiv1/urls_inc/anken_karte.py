from django.urls import path, include, re_path
from ..views.anken_karte import anken_karte_list, anken_karte_customer, anken_karte_ankeninfo, anken_karte_visithistory
from ..views.anken_karte import anken_karte_ankenpast, anken_karte_ankennear, anken_karte_sucsrt
from ..views.anken_karte import anken_karte_advice, anken_karte_alert, anken_karte_sucscmt, anken_karte_sucshis
from ..views.anken_karte import anken_karte_keyword, anken_karte_keywordpthis, anken_karte_customernews

urlpatterns = [
    # [案件カルテ]機能
    # [一覧]
    path('list', anken_karte_list.AnkenKarteListView.as_view()),
    
    # [詳細]
    # 顧客情報
    path('customer/<int:pk>/', anken_karte_customer.AnkenKarteCustomerView.as_view()),
    # 案件情報
    path('ankeninfo/<int:pk>/', anken_karte_ankeninfo.AnkenKarteAnkeninfoView.as_view()),
    # 訪問履歴_一覧
    path('vishis_list', anken_karte_visithistory.AnkenKarteVisHisListView.as_view()),
    # 訪問履歴_詳細
    path('vishis/<int:pk>/', anken_karte_visithistory.AnkenKarteVisHisDetailView.as_view()),
    # 過去案件_一覧
    path('anpast_list/<int:customer_id>/', anken_karte_ankenpast.AnkenKarteAnkPastListView.as_view()),
    # 過去案件_一覧
    path('annear_list/<int:customer_id>/<int:anken_id>/', anken_karte_ankennear.AnkenKarteAnkNearListView.as_view()),
    # 案件分析_成約確率
    path('sucsrt/<int:anken_id>/', anken_karte_sucsrt.AnkenKarteSucsrtView.as_view()),
    # 案件分析_案件分析コメント
    path('sucscmt_list/<int:anken_id>/', anken_karte_sucscmt.AnkenKarteSucsCmtListView.as_view()),
    # 案件分析_成約確率履歴
    path('sucshis_list/<int:anken_id>/', anken_karte_sucshis.AnkenKarteSucsHisListView.as_view()),
    # アドバイス_一覧
    path('advice_list/<int:customer_id>/<int:anken_id>/', anken_karte_advice.AnkenKarteAdviceListView.as_view()),
    # アラート_一覧
    path('aleart_list/<int:customer_id>/<int:anken_id>/', anken_karte_alert.AnkenKarteAlertListView.as_view()),
    # キーワード_一覧
    path('keyword_list/<int:customer_id>/<int:anken_id>/', anken_karte_keyword.AnkenKarteKeywordListView.as_view()),
    # キーワードポイント履歴
    path('keywordpthis_list/<int:customer_id>/<int:anken_id>/', anken_karte_keywordpthis.AnkenKarteKeywordpthisListView.as_view()),
    # 顧客ニュース
    path('sucshis_list/<int:customer_id>/', anken_karte_customernews.AnkenKarteCustNewsListView.as_view()),

]
