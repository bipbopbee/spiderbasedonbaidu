#输出log位置的文件名、函数名、行号
#coding=utf-8
import inspect

def getLineFileFunc():
    callerframerecord = inspect.stack()[2]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    return ' - line:' + bytes(info.lineno) + ' - ' +info.function + '() - ' +  info.filename