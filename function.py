#-*- coding: utf-8 -*-
'''
def xAssert(boolean):
    if not boolean:
        raise AssertionError("Assertion Failed At: %s: %s" %
                             (sys._getframe().f_back.f_code.co_name,
                              sys._getframe().f_back.f_lineno))
'''

def pformat(label, value):
    print("%-20s %s" % (label, value))

def formatDateTime(secs):
    import time
    if secs is None:
        return "None"
    if secs == 0:
        return "Unknown"
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs))

def formatSize(size):
    if size is None:
        return "None"
    if size > 1024**3:
        return "%.2f GiB" % (size / 1024**3,)
    elif size > 1024**2:
        return "%.2f MiB" % (size / 1024**2,)
    elif size > 1024:
        return "%.2f KiB" % (size / 1024,)
    return str(size)

def formatSize2(size):
    if size is None:
        return "None"
    if size > 1024**3:
        return "%s (%.2f GiB)" % (size, size / 1024**3)
    elif size > 1024**2:
        return "%s (%.2f MiB)" % (size, size / 1024**2)
    elif size > 1024:
        return "%s (%.2f KiB)" % (size, size / 1024)
    return str(size)
