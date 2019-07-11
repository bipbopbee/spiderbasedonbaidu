import os
url = "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8"
name = tmp.mp4
ffmpeg -i "https://zy.zxziyuan-yun.com/20180107/hv8I41wD/index.m3u8" -vcodec copy -acodec copy -absf aac_adtstoasc output.mp4
command = "ffmpeg -i " + url + "-vcodec copy -acodec copy -absf aac_adtstoasc" + name
output = os.popen(command)