import pykintone
from apps.ds.models import Kintone_Key

class Kintone():
    def get_kintone_data(app_id, limit=None, offset=None, query=None):
        result = False
        records = None
        errmsg = None
        ktn_key = None
        try:
            ktn_key = Kintone_Key.objects.get(app_id=app_id)
        except Kintone_Key.DoesNotExist:
            return result, records, errmsg

        if offset == None:
            offset = 0
        if limit == None:
            limit = 500
        if query == None:
            query = ''
        else:
            query += ' '
    
        r = pykintone.app(ktn_key.domain, ktn_key.app_id, ktn_key.api_token).select(query + "limit " + str(limit) + " offset " + str(offset))
        if not r.ok:
            errmsg = r.error
            return result, records, errmsg

        result = True
        records = r.records

        return result, records, errmsg
