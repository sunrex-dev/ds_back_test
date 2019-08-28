from django.core.management import BaseCommand
from django.db import transaction
from apps.dblogs.models import Process_Logs
from apps.tenants.utils import tenant_info
from apps.ds.models import History, Anken, Employee, Customer
from apps.apiv1.services.kintone_api import Kintone
from apps.apiv1.serializers.ds_history import DsHistorySerializer
from apps.apiv1.utils.common import *
from apps.apiv1.utils.counter import Counter
#from apps.apiv1.utils.dbutil import *

# PROCESS情報を設定(PROCESS管理テーブルに存在するID)
process_id = 3
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
dayminus = 14000

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
    #query= '更新日時 >= \"2012-02-03T09:00:00+0900\"'
    # DAYS：日単位, WEEKS：週単位, MONTHS：月単位, YEARS：年単位
    global dayminus
    dayminus = dayminus * -1
    query= '更新日時 >= FROM_TODAY({0}, DAYS)'.format(dayminus)
    records = []
    while True:
        ret, records, errmsg = Kintone.get_kintone_data(106, limit, offset, query)
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
        #break

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

        data['anken'] = None
        data['anken_no'] = nz(rec['案件レコード番号']['value'], defval=None)
        data['anken_name'] = nz(rec['案件名']['value'], defval=None)
        
        data['title'] = nz(rec['レコードタイトル']['value'])
        data['created_at_origin'] = rec['作成日時']['value']
        data['updated_at_origin'] = rec['更新日時']['value']
        data['employee_name'] = nz(rec['営業担当']['value'][0]['name'])
        data['customer_no'] = nz(rec['顧客Mレコード番号']['value'], defval=0)
        data['customer_name'] = nz(rec['顧客名']['value'])
        data['visit_plan_dt'] = nz(rec['訪問予定日時']['value'], defval=None)
        data['visit_plan_times'] = nz(rec['訪問予定時間']['value'], defval=None)
        data['visit_dt'] = nz(rec['実訪問日時']['value'], defval=None)
        data['visit_times'] = nz(rec['実訪問時間']['value'], defval=None)
        data['purpose'] = nz(rec['目的']['value'])
        data['meet_method'] = nz(rec['商談手段']['value'])
        data['meet_result'] = nz(rec['面談結果']['value'])
        data['result'] = nz(rec['結果']['value'])
        data['remarks'] = nz(rec['備考']['value'])
        data['future_issue'] = nz(rec['課題事項']['value'])
        data['next_action'] = nz(rec['次回設定']['value'])
        data['next_action_dt'] = nz(rec['次回アクション日時']['value'], defval=None)
        data['attention'] = nz(rec['注目']['value'])
        data['good_count'] = nz(rec['いいね数']['value'], defval=None)

        # 商談案件番号が空の場合は、以下のロジックで商談案件テーブルより取得
        if nz(data['anken_no'], defval=None) == None and \
           nz(data['customer_no'], defval=None) != None:
            if nz(data['anken_name'], defval=None) != None:
                ds_anken = Anken.objects.values('id','no')
                ds_anken = ds_anken.filter(customer_no=data['customer_no'])
                ds_anken = ds_anken.filter(name=data['anken_name'])
                if ds_anken.exists():
                    data['anken'] = ds_anken[0]['id']
                    data['anken_no'] = ds_anken[0]['no']
            else:
                taget_dt = None
                if nz(data['visit_dt'], defval=None) !=None:
                    taget_dt = nz(data['visit_dt'], defval=None)
                elif nz(data['visit_plan_dt'], defval=None) !=None:
                    taget_dt = nz(data['visit_plan_dt'], defval=None)
                elif nz(data['created_at_origin'], defval=None) !=None:
                    taget_dt = nz(data['created_at_origin'], defval=None)
                if taget_dt != None:
                    try:
                        taget_dt = dt.strptime(taget_dt, '%Y-%m-%dT%H:%M:%SZ')
                    except Exception:
                        taget_dt = None
                if taget_dt != None:
                    ds_anken = Anken.objects.values('id','no','name')
                    ds_anken = ds_anken.filter(customer_no=data['customer_no'])
                    ds_anken = ds_anken.filter(created_at_origin__lte=taget_dt)
                    ds_anken = ds_anken.filter(close_dt__gte=taget_dt)
                    ds_anken = ds_anken.order_by('-no')
                    if ds_anken.exists():
                        data['anken'] = ds_anken[0]['id']
                        data['anken_no'] = ds_anken[0]['no']
                        data['anken_name'] = ds_anken[0]['name']
                if taget_dt != None and nz(data['anken_no'], defval=None) == None:
                    ds_anken = Anken.objects.values('id','no','name')
                    ds_anken = ds_anken.filter(customer_no=data['customer_no'])
                    ds_anken = ds_anken.filter(created_at_origin__lte=taget_dt)
                    ds_anken = ds_anken.filter(close_plan_dt__gte=taget_dt)
                    ds_anken = ds_anken.order_by('-no')
                    if ds_anken.exists():
                        data['anken'] = ds_anken[0]['id']
                        data['anken_no'] = ds_anken[0]['no']
                        data['anken_name'] = ds_anken[0]['name']
                if taget_dt != None and nz(data['anken_no'], defval=None) == None:
                    ds_anken = Anken.objects.values('id','no','name')
                    ds_anken = ds_anken.filter(customer_no=data['customer_no'])
                    ds_anken = ds_anken.filter(created_at_origin__lte=taget_dt)
                    ds_anken = ds_anken.filter(updated_at_origin__gte=taget_dt)
                    ds_anken = ds_anken.order_by('-no')
                    if ds_anken.exists():
                        data['anken'] = ds_anken[0]['id']
                        data['anken_no'] = ds_anken[0]['no']
                        data['anken_name'] = ds_anken[0]['name']

        # 社員管理番号の取得
        data['employee'] = None
        data['employee_no'] = None
        if nz(data['employee_name'], defval=None) != None:
            ds_emp = Employee.objects.values('id','no')
            ds_emp = ds_emp.filter(name_search=data['employee_name'].replace(' ','').replace('　',''))
            ds_emp = ds_emp.order_by('-no')
            if ds_emp.exists():
                data['employee'] = ds_emp[0]['id']
                data['employee_no'] = ds_emp[0]['no']

        # 顧客管理IDの取得
        data['customer'] = None
        if nz(data['customer_no'], defval=None) != None:
            ds_cust = Customer.objects.values('id')
            ds_cust = ds_cust.filter(no=data['customer_no'])
            if ds_cust.exists():
                data['customer'] = ds_cust[0]['id']

        # シリアライザに値をセット
        try:
            ds_history = History.objects.get(no=data['no'])
        except History.DoesNotExist:
            ds_history = None
        ds_ser = DsHistorySerializer(instance=ds_history, data=data)
        # エラーチェックを実行
        if ds_ser.is_valid():
            if ds_history != None:
                check_dt = dt.strptime(data['updated_at_origin'], '%Y-%m-%dT%H:%M:%SZ')
                if ds_history.updated_at_origin >= check_dt:
                    # データの更新日時が既存のものと同じか古い場合はスキップ
                    counter.add_skip() # カウンターインクリメント
                    continue
            # 適切な場合は保存
            ds_ser.save()
            counter.add_ok() # カウンターインクリメント
        else:
            # エラー発生時
            counter.add_ng() # カウンターインクリメント
            error_logs.append('<<エラー発生>>inp_count{0}, no={1}, title={2}'.format(counter.inp ,data.get('no',''), data.get('title','')))
            for key,details in ds_ser.errors.items():
                value = ''
                if key in data:
                    value = data[key]
                for detail in details:
                    msg='[項目名]{0} [値]{1} [エラー内容]{2}'.format(key, value, detail)
                    error_logs.append(msg)

    result = True

    return result
