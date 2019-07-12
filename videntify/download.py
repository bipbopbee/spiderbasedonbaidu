import os
import datetime
import traceback
import subprocess
import tempfile
import sys
import threading
url = "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8"
name = "tmp.mp4"
#ffmpeg -i "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8" -vcodec copy -acodec copy -absf aac_adtstoasc output.mp4


def fingerprint_query(desc72file, headers):
    pass
def desc72_generate(filename):
    try:
        command = "desc_tools " +  filename + " " + filename + ".desc72"
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 10 * 1000)
        fileno = outtemp.fileno()
        fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        fd.wait()
        outtemp.seek(0)
        lines = outtemp.readlines()
        print lines
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()
def thread_download(url, nowtime):
    try:
        command = "ffmpeg -i " + url + " -vcodec copy -acodec copy -absf aac_adtstoasc " + nowtime + ".mp4"
        outtemp =tempfile.SpooledTemporaryFile(bufsize = 10 * 1000)
        fileno = outtemp.fileno()
        fd = subprocess.Popen(command, stdout=fileno, stderr=fileno, shell=False)
        fd.wait()
        outtemp.seek(0)
        lines = outtemp.readlines()
        print lines
    except Exception, e:
        print traceback.format_exc()
    finally:
        if outtemp:
            outtemp.close()

if __name__ == "__main__":
    nowtime = str(datetime.datetime.now().microsecond)
    print nowtime
    t = threading.Thread(target=thread_download, args=(url, nowtime))
    t.start()
    pass