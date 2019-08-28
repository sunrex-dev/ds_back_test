#from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import serializers
from apps.tenants.utils import tenant_info
from apps.ds.models.anken import Anken
from apps.apiv1.utils.common import *

class AnkenKarteListSerializer(serializers.Serializer):
    anken_id = serializers.ReadOnlyField(help_text='案件管理ID')
    result_kbn = serializers.ReadOnlyField(help_text='商談結果区分')
    customer_id = serializers.ReadOnlyField(help_text='顧客管理ID')
    customer_name = serializers.ReadOnlyField(help_text='顧客名')
    employee_id = serializers.ReadOnlyField(help_text='社員管理ID')
    employee_name = serializers.ReadOnlyField(help_text='営業担当社員名')
    anken_name = serializers.ReadOnlyField(help_text='案件名')
    last_visit_dt = serializers.ReadOnlyField(help_text='最終訪問日（yyyy-MM-dd）')
    close_plan_total = serializers.ReadOnlyField(help_text='成約金額合計')
    advice_flg = serializers.ReadOnlyField(help_text='アドバイス有無区分')
    alert_flg = serializers.ReadOnlyField(help_text='アラート有無区分')

class AnkenKarteListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteListSerializer
    # ordering可能な項目の設定
    ordering_fields = ['anken_id', 'result_kbn', 'customer_id', 'customer_name']
    ordering_fields += ['employee_id', 'employee_name', 'anken_name', 'last_visit_dt']
    ordering_fields += ['close_plan_total', 'advice_flg', 'alert_flg']

    def get_queryset(self):

        # TENANT IDの取得
        tenant_id = -1
        tenant = tenant_info.get_current_tenant()
        if tenant != None:
            tenant_id = tenant.id

        # 条件パラメータの取得
        p_dict = {}
        p_result_kbn = self.request.GET.get('result_kbn','')
        p_keyword = self.request.GET.get('keyword','')
        p_customer_name = self.request.GET.get('customer_name','')
        p_anken_name = self.request.GET.get('anken_name','')
        p_employee_name = self.request.GET.get('employee_name','')
        p_last_visit_dt_str=self.request.GET.get('last_visit_dt_str','')
        p_last_visit_dt_end=self.request.GET.get('last_visit_dt_end','')
        p_advice_flg = self.request.GET.get('advice_flg','')
        p_alert_flg = self.request.GET.get('alert_flg','')
        p_success_rate_str = self.request.GET.get('success_rate_str','')
        p_success_rate_end = self.request.GET.get('success_rate_end','')
        p_close_plan_rank = self.request.GET.get('close_plan_rank','')
        p_close_plan_dt_str = self.request.GET.get('close_plan_dt_str','')
        p_close_plan_dt_end = self.request.GET.get('close_plan_dt_end','')

        sql = "select x.* from "
        sql += "( "
        
        if p_result_kbn != '0':
            # 商談案件ありデータ
            sql += "select "
            sql += "0 as id, "
            sql += "a.id as anken_id, "
            #sql += "a.no as anken_no, "
            sql += "a.result_kbn, "
            sql += "a.customer_id, "
            sql += "max(a.customer_name) as customer_name, "
            sql += "h.employee_id, "
            sql += "max(h.employee_name) as employee_name, "
            sql += "max(a.name) as anken_name, "
            sql += "max(cast(h.visit_dt as date)) as last_visit_dt, "
            sql += "a.close_plan_total, "
            sql += "cast(a.close_plan_dt as date) as close_plan_dt, "
            sql += "0 as advice_flg, 0 as alert_flg, 50 as success_rate "
            sql += "from ds_anken as a "
            sql += "inner join ds_history as h "
            sql += "on a.tenant_id = h.tenant_id and a.no = h.anken_no "
            sql += "where a.tenant_id = " + str(tenant_id) + " "
            sql += "and   h.anken_no is not null "
            sql += "group by "
            sql += "a.id, a.result, a.customer_id, a.close_plan_total, a.close_plan_dt, "
            sql += "h.employee_id "

        else:
            # 未案件データ
            sql += "select "
            sql += "max(h.id) as id, "
            #sql += "0 as anken_no, "
            sql += "0 as anken_id, "
            sql += "0 as result_kbn, "
            sql += "h.customer_id, "
            sql += "max(h.customer_name) as customer_name, "
            sql += "h.employee_id, "
            sql += "max(h.employee_name) as employee_name, "
            sql += "'' as anken_name, "
            sql += "max(cast(h.visit_dt as date)) as last_visit_dt, "
            sql += "0 as close_plan_total, "
            sql += "null as close_plan_dt, "
            sql += "0 as advice_flg, 0 as alert_flg, 0 as success_rate "
            sql += "from ds_history as h "
            sql += "where h.tenant_id = " + str(tenant_id) + " "
            sql += "and   h.anken_no is null "
            sql += "group by "
            sql += "h.customer_id, h.employee_id "

        sql += ") as x "
        #sql += "order by x.last_visit_dt desc "

        # 条件の指定
        sql += "where 1=1 "
        if not p_result_kbn in ['0','1','2','3']:
            p_result_kbn = -1
        #p_dict['result_kbn'] = p_result_kbn.split(',')
        #sql += "and result_kbn in %(result_kbn)s "
        p_dict['result_kbn'] = p_result_kbn
        sql += "and result_kbn = %(result_kbn)s "

        # キーワード
        if p_keyword != '':
            p_dict['keyword'] = '%' + str(p_keyword) + '%'
            sql += "and ( "
            sql += "x.customer_name like %(keyword)s "
            sql += "or "
            sql += "x.anken_name like %(keyword)s "
            sql += "or "
            sql += "x.employee_name like %(keyword)s "
            sql += ") "
        # 顧客名
        if p_customer_name != '':
            p_dict['customer_name'] = '%' + str(p_customer_name) + '%'
            sql += "and x.customer_name like %(customer_name)s "
        # 案件名
        if p_anken_name != '':
            p_dict['anken_name'] = '%' + str(p_anken_name) + '%'
            sql += "and x.anken_name like %(anken_name)s "
        # 社員名
        if p_employee_name != '':
            p_dict['employee_name'] = '%' + str(p_employee_name) + '%'
            sql += "and x.employee_name like %(employee_name)s "
        # 最終面談日
        if p_last_visit_dt_str != '' and isDate(p_last_visit_dt_str):
            p_dict['last_visit_dt_str'] = str(p_last_visit_dt_str)
            sql += "and x.last_visit_dt >= %(last_visit_dt_str)s "
        if p_last_visit_dt_end != '' and isDate(p_last_visit_dt_end):
            p_dict['last_visit_dt_end'] = str(p_last_visit_dt_end)
            sql += "and x.last_visit_dt <= %(last_visit_dt_end)s "
        # アドバイス
        if p_advice_flg != '':
            p_dict['advice_flg'] = p_advice_flg
            sql += "and x.advice_flg like %(advice_flg)s "
        # アラート
        if p_alert_flg != '':
            p_dict['alert_flg'] = p_alert_flg
            sql += "and x.alert_flg like %(alert_flg)s "
        # 成約確率
        if p_success_rate_str != '':
            p_dict['success_rate_str'] = str(p_success_rate_str)
            sql += "and x.success_rate >= %(success_rate_str)s "
        if p_success_rate_end != '':
            p_dict['success_rate_end'] = str(p_success_rate_end)
            sql += "and x.success_rate <= %(success_rate_end)s "
        # 成約予定金額ラング
        if p_close_plan_rank != '':
            if p_close_plan_rank.upper() == 'A':
                sql += "and x.close_plan_total >= 10000000 "
            elif p_close_plan_rank.upper() == 'B':
                sql += "and x.close_plan_total between 1000000 and 9999999 "
            elif p_close_plan_rank.upper() == 'C':
                sql += "and x.close_plan_total between 100000 and 999999 "
            elif p_close_plan_rank.upper() == 'D':
                sql += "and x.close_plan_total < 100000 "
        # 成約予定日
        if p_close_plan_dt_str != '' and isDate(p_close_plan_dt_str):
            p_dict['close_plan_dt_str'] = str(p_close_plan_dt_str)
            sql += "and x.close_plan_dt >= %(close_plan_dt_str)s "
        if p_close_plan_dt_end != '' and isDate(p_close_plan_dt_end):
            p_dict['close_plan_dt_end'] = str(p_close_plan_dt_end)
            sql += "and x.close_plan_dt <= %(close_plan_dt_end)s "

        # 並び順の指定
        sql += "order by "
        if 'ordering' in self.request.query_params:
            orderby = self.request.GET['ordering']
            orderby = orderby.split(',')
            if ''.join(orderby)=='':
                sql += "last_visit_dt desc "
            else:
                #try:
                tmpsql = ""
                for odr in orderby:
                    if tmpsql != "":
                        tmpsql += ", "
                    if odr[:1] == '-':
                        odr = odr[1:]
                        tmpsql += odr + " desc "
                    else:
                        tmpsql += odr + " "
                    if not odr in ordering_fields:
                        tmpsql = "last_visit_dt desc "
                        break
                sql += tmpsql
                #except:
                #    sql += "last_visit_dt desc "
        else:
            sql += "last_visit_dt desc "
        #print(sql)
        query = Anken.objects
        query = query.raw(sql, p_dict)

        #print(query.query)
        return query

    @swagger_auto_schema(operation_summary="[案件カルテ]の[一覧]取得", manual_parameters=[
        openapi.Parameter('result_kbn', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='商談結果区分(0:未案件,1:継続,2:成約,3:敗戦)'),
        openapi.Parameter('keyword', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索するキーワードの文字列'),
        openapi.Parameter('customer_name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索する顧客名称の文字列'),
        openapi.Parameter('anken_name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索する案件名の文字列'),
        openapi.Parameter('employee_name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索する営業担当名称の文字列'),
        openapi.Parameter('last_visit_dt_str', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索する最終訪問日（開始値）の日付（yyyy-MM-dd形式）'),
        openapi.Parameter('last_visit_dt_end', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索する最終訪問日（終了値）の日付（yyyy-MM-dd形式）'),
        openapi.Parameter('advice_flg', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='検索するアドバイス有無の区分（1:有り）'),
        openapi.Parameter('alert_flg', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='検索するアラート有無の区分（1:有り）'),
        openapi.Parameter('success_rate_str', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='検索する成約確率（開始値）の整数値'),
        openapi.Parameter('success_rate_end', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='検索する成約確率（終了値）の整数値'),
        openapi.Parameter('close_plan_rank', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索する顧客ランクの値（A,B,C,D）'),
        openapi.Parameter('close_plan_dt_str', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索する成約予定日（開始値）の日付（yyyy-MM-dd形式）'),
        openapi.Parameter('close_plan_dt_end', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='検索する成約予定日（開始値）の日付（yyyy-MM-dd形式）'),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[一覧]取得
        """
        return super().get(request, *args, **kwargs)
