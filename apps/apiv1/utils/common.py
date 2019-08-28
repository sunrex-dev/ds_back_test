from datetime import datetime as dt

"""
共通関数
"""

# 空白やNone時の変換処理
def nz(val, defval=''):
    if val is None or val =='':
        return defval
    return val

def getJsonVal(jsondata, arrayparam, defval=''):
    try:
        tmp = None
        for itm in arrayparam:
            if tmp is None:
                tmp = jsondata[itm]
            else:
                tmp = tmp[itm]
        retval = nz(tmp)
    except IndexError:
        retval = nz(defval)
    except KeyError:
        retval = nz(defval)
    return retval

# 日付の妥当性チェック
def isDate(val, format='%Y-%m-%d'):
    try:
        dt.strptime(str(val), format)
        return True
    except ValueError:
        return False
