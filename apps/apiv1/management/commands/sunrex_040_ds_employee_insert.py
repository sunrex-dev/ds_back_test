from django.core.management import BaseCommand
from django.db import transaction
from apps.dblogs.models import Process_Logs
from apps.tenants.utils import tenant_info
from apps.ds.models import Employee
from apps.apiv1.services.kintone_api import Kintone
from apps.apiv1.serializers.ds_employee import DsEmployeeSerializer
from apps.apiv1.utils.common import *
from apps.apiv1.utils.counter import Counter

# PROCESS情報を設定(PROCESS管理テーブルに存在するID)
process_id = 4
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

    # 顧客マスタを入替えするため全件削除
    global dayminus
    if dayminus == None:
        #Ds_Customer.objects.all().delete()
        pass

    # Kintone APIよりデータを取得(1回あたりの受信がMAX500なので繰り替えし処理を実行)
    offset = 0
    limit = 500
    query = None
    if dayminus != None:
        dayminus = dayminus * -1
        query= '更新日時 >= FROM_TODAY({0}, DAYS)'.format(dayminus)
    records = []
    while True:
        ret, records, errmsg = Kintone.get_kintone_data(179, limit, offset, query)
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
        data['code'] = rec['社員コード']['value']
        data['code_short'] = nz(rec['社員コード3桁']['value'],defval=None)
        data['name'] = nz(rec['社員名']['value'])
        data['name_kana'] = nz(rec['社員名カナ']['value'])
        data['name_search'] = data['name'].replace(' ','').replace('　','')
        data['department'] = nz(rec['所属']['value'])
        data['created_at_origin'] = nz(rec['作成日時']['value'])
        data['updated_at_origin'] = nz(rec['更新日時']['value'])
        data['deleted_kbn'] = nz(rec['廃止区分']['value'])
        data['deleted_at'] = nz(rec['廃止日時']['value'], defval=None)

        # シリアライザに値をセット
        try:
            ds_emp = Employee.objects.get(no=data['no'])
        except Employee.DoesNotExist:
            ds_emp = None
        ds_ser = DsEmployeeSerializer(instance=ds_emp, data=data)
        # エラーチェックを実行
        if ds_ser.is_valid():
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
