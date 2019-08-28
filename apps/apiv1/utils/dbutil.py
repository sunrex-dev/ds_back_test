#from django.db.models import TextField
#from django.db.models.functions import Length
from django.db import connection
from datetime import datetime as dt

#TextField.register_lookup(Length, 'len')

def get_sysdate():
    cursor = connection.cursor()
    sql = cursor.execute("select DATE_FORMAT(now() , '%Y-%m-%d %T') from dual")
    result = cursor.fetchone()
    rdt = dt.strptime(result[0], '%Y-%m-%d %H:%M:%S')
    return rdt
