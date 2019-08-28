from django.core.management import BaseCommand
from django.db import transaction
from apps.dblogs.models import Process_Logs
from apps.tenants.utils import tenant_info
from apps.ds.models import Anken, Employee, Customer
from apps.apiv1.services.kintone_api import Kintone
from apps.apiv1.serializers.ds_anken import DsAnkenSerializer
from apps.apiv1.utils.common import *
from apps.apiv1.utils.counter import Counter

# PROCESS情報を設定(PROCESS管理テーブルに存在するID)
process_id = 2
# 処理対処のTENANT IDを設定（複数テナントで利用する場合は起動時の引数で渡す等の変更が必要）
tenant_id = 1
# ログ設定
error_logs = []
import logging
logger = logging.getLogger('bgjob')
# ex.
# logger.debug("debug message")
# logger.warning("warning message")
# logger.error("error message")
# logger.critical("critical message")
# カウンター設定
counter = Counter()
# PROCESS実行履歴の設定
prclog = Process_Logs()
prclog.process_id = process_id
# 引数取得変数の設定
dayminus = None

# 起動処理
class Command(BaseCommand):
    # help = 'ここにコマンドの説明を書けます。'

    def handle(self, *args, **options):
        try:
            # 引数を取得
            # tenant_id = options['tenant_id']
            if options['dayminus'] != None:
                global dayminus
                dayminus = options['dayminus']
            # メイン処理の実行
            main(self)
        except Exception as exerr:
            import traceback
            logger.exception(traceback.format_exc())

    def add_arguments(self, parser):
        # parser.add_argument('--tenant_id', type=int, required=True, help='処理対象となる TENANT ID を指定')
        parser.add_argument('--dayminus', type=int, help='更新日の取得対象日の調整（例）5=5日前、10=10日前')
        pass

# メイン処理
def main(self):
    try:
        # スレッド変数に tenant_id を保存
        tenant_info.set_current_tenant_by_id(tenant_id)
        # PROCESS実行履歴
        prclog.tenant_id = tenant_id
        prclog.save()
        logger.info('========== > {0}(id={1}) Start =========='.format(prclog.process_name, prclog.process_id))
        logger.info('tenant_id = {0}'.format(tenant_id))
        global dayminus
        if dayminus == None:
            dayminus = 14
        if dayminus != None:
            logger.info('dayminus = {0}'.format(dayminus))

        # Kintone APIよりデータを取得して、DBへ登録する。
        if kintone_to_db():
            prclog.set_status('I')
        else:
            prclog.set_status('E')

    except Exception as exerr:
        import traceback
        logger.exception(traceback.format_exc())
        prclog.set_status('C')
        prclog.append_process_log(traceback.format_exc())

    finally:
        logger.info("========== > {0}(id={1}) End   ==========".format(prclog.process_name, prclog.process_id))
        prclog.save()
        # スレッド変数を初期化
        tenant_info.set_current_tenant(None)

# Kintone APIよりデータを取得して、DBへ登録
@transaction.atomic
def kintone_to_db():
    result = True

    # Kintone APIよりデータを取得(1回あたりの受信がMAX500なので繰り替えし処理を実行)
    offset = 0
    limit = 500
    query = None
    global dayminus
    if dayminus != None:
        dayminus = dayminus * -1
        query= '更新日時 >= FROM_TODAY({0}, DAYS)'.format(dayminus)
    records = []
    while True:
        ret, records, errmsg = Kintone.get_kintone_data(105, limit, offset, query)
        if not ret:
            # 取得失敗
            error_logs.append(errmsg)
            result = False
            break
        elif records == []:
            break
        else:
            offset += limit
            # DBへ登録
            if not db_insert(records):
                # 登録失敗
                result = False

    # エラーログの出力
    for errmsg in error_logs:
        logger.error(errmsg)
        prclog.append_process_log(errmsg)

    # インフォログの出力
    cnt_info = []
    cnt_info.append('[入力件数]{0}'.format(counter.inp))
    cnt_info.append('[登録件数]{0}'.format(counter.ok))
    cnt_info.append('[エラー件数]{0}'.format(counter.ng))
    cnt_info.append('[スキップ件数]{0}'.format(counter.skip))
    for infmsg in cnt_info:
        logger.info(infmsg)
        prclog.append_process_log(infmsg)

    return result

# DBへ登録
def db_insert(records):
    result = False

    data={}
    for rec in records:
        counter.add_inp() # カウンターインクリメント
        print(counter.inp)

        data.clear()
        data['tenant'] = tenant_id
        data['no'] = rec['レコード番号']['value']
        data['name'] = nz(rec['案件名']['value'])
        data['title'] = nz(rec['レコードタイトル']['value'])
        data['created_at_origin'] = nz(rec['作成日時']['value'])
        data['updated_at_origin'] = nz(rec['更新日時']['value'])
        data['employee_name'] = nz(rec['営業担当']['value'][0]['name'])
        data['customer_no'] = nz(rec['顧客Mレコード番号']['value'], defval=0)
        data['customer_name'] = nz(rec['顧客名']['value'])
        data['section_name'] = nz(rec['商談部署名']['value'])
        data['section_tel_type'] = nz(rec['商談部署TEL種類']['value'])
        data['section_tel'] = nz(rec['商談部署TEL']['value'])
        data['customer_person'] = nz(rec['商談担当者名']['value'])
        data['close_plan_dt'] = nz(rec['成約予定日']['value'], defval=None)
        data['close_plan_total'] = nz(rec['成約予定金額合計']['value'], defval=0)
        data['close_plan_profit'] = nz(rec['成約予定粗利合計']['value'], defval=0)
        data['close_plan_mamount'] = nz(rec['成約予定月額合計']['value'], defval=0)
        data['close_dt'] = nz(rec['成約計上日']['value'], defval=None)
        data['sales_plan_dt'] = nz(rec['売上予定日_1回目']['value'], defval=None)
        data['sales_plan_profit'] = nz(rec['売上予定粗利合計']['value'], defval=0)
        data['sales_plan_mamount'] = nz(rec['売上予定月額合計']['value'], defval=0)
        data['result'] = nz(rec['結果']['value'])
        data['result_analysis'] = nz(rec['結果分析']['value'])
        data['remarks'] = nz(rec['備考']['value'])
        data['salse_probability'] = nz(rec['成約確率']['value'], defval=0)
        data['result_kbn'] = 0
        if data['result'] == '継続':
            data['result_kbn'] = 1
        elif data['result'] == '成約':
            data['result_kbn'] = 2
        elif data['result'] == '敗戦':
            data['result_kbn'] = 3

        # 社員管理番号の取得
        data['employee_no'] = None
        data['employee'] = None
        if nz(data['employee_name'], defval=None) != None:
            ds_emp = Employee.objects.values('id','no')
            ds_emp = ds_emp.filter(name_search=data['employee_name'].replace(' ','').replace('　',''))
            ds_emp = ds_emp.order_by('-no')
            if ds_emp.exists():
                data['employee_no'] = ds_emp[0]['no']
                data['employee'] = ds_emp[0]['id']

        # 顧客管理IDの取得
        data['customer'] = None
        if nz(data['customer_no'], defval=None) != None:
            ds_cust = Customer.objects.values('id')
            ds_cust = ds_cust.filter(no=data['customer_no'])
            if ds_cust.exists():
                data['customer'] = ds_cust[0]['id']

        # シリアライザに値をセット
        try:
            ds_anken = Anken.objects.get(no=data['no'])
        except Anken.DoesNotExist:
            ds_anken = None
        ds_ser = DsAnkenSerializer(instance=ds_anken, data=data)
        # エラーチェックを実行
        if ds_ser.is_valid():
            if ds_anken != None:
                check_dt = dt.strptime(data['updated_at_origin'], '%Y-%m-%dT%H:%M:%SZ')
                if ds_anken.updated_at_origin >= check_dt:
                    # データの更新日時が既存のものと同じか古い場合はスキップ
                    counter.add_skip() # カウンターインクリメント
                    continue
            # 適切な場合は保存
            ds_ser.save()
            counter.add_ok() # カウンターインクリメント
        else:
            # エラー発生時
            counter.add_ng() # カウンターインクリメント
            error_logs.append('<<エラー発生>>inp_count{0}, no={1}, name={2}'.format(counter.inp ,data.get('no',''), data.get('name','')))
            for key,details in ds_ser.errors.items():
                value = ''
                if key in data:
                    value = data[key]
                for detail in details:
                    msg='[項目名]{0} [値]{1} [エラー内容]{2}'.format(key, value, detail)
                    error_logs.append(msg)

    result = True

    return result
