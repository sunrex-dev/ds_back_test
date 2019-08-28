from django.core.management import BaseCommand
from apps.dblogs.models import Process_Logs
#import pykintone

# PROCESS情報を設定(PROCESS管理テーブルに存在するID)
process_id = 1

# ログ設定
import logging
logger = logging.getLogger('bgjob')

# PROCESS実行履歴の設定
prclog = Process_Logs()
prclog.process_id = process_id

class Command(BaseCommand):
    help = 'ここにコマンドの説明を書けます。'

    def handle(self, *args, **options):
        try:
            # 引数を取得
            tenant_id = options['tenant_id']
            # PROCESS実行履歴
            prclog.tenant_id = tenant_id
            prclog.save()
            logger.info('========== > {0} Start =========='.format(prclog.process_name))
            # メイン処理の実行
            main(self)
        except Exception as exerr:
            import traceback
            logger.exception(traceback.format_exc())
            prclog.set_status('C')
            prclog.process_log += traceback.format_exc()
        finally:
            logger.info("========== > {0} End   ==========".format(prclog.process_name))
            prclog.save()

    def add_arguments(self, parser):
        # コマンドのオプションを実装します。
        parser.add_argument('--tenant_id', type=int, required=True, help='処理対象となる TENANT ID を指定')
        # 引数を必要としない場合は、この関数の実装は必要ありません。
        # parser.add_argument('opt1', help='必須オプション')
        # parser.add_argument('--opt2', help='任意オプション')
        pass

def main(self):
    # ここに実行したいコマンドを記述

    logger.debug("debug message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    #f = open('sample.txt', 'r')
    prclog.set_status('I')
    prclog.process_log = 'ここにプロセス処理のログを記述'
#    try:
#        import math
#        math.log(-1)
#    except ValueError as err:
#        logger.exception('Raise Exception: %s', err)

    pass
