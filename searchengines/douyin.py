#coding=utf8
import requests
import sys
import os
import io
import time
if __name__ == "__main__":
    headers={}
    headers["accept-encoding"] = "gzip"
    headers["x-ss-req-ticket"] = "1563955514509"
    headers["x-tt-token"] = "00d2407d3890c914e3722c00b394ef7e4f4193bff9cf1f2e838ad5d983361fca43d2df49e0160afe0f474fa1df2f74279462"
    headers["sdk-version"] = "1"
    headers["x-ss-stub"] = "16F3387E61D25662274247C20FE2084C"
    headers["user-agent"] = "com.ss.android.ugc.aweme/400 (Linux; U; Android 4.4.2; zh_CN; OPPO R11; Build/NMF26X; Cronet/58.0.2991.0)"
    headers["x-gorgon"] = "0300fe56000092d0946479a32a260617a423aa5fc0add543b7d4"
    headers["x-khronos"] = "1563955514"
    headers['content-type'] = "application/x-www-form-urlencoded; charset=UTF-8"


    cookies={}
    cookies["odin_tt"] = "39e75ba6630c35f0122eefa42a187ec07ef0d28830b9e0b75513dbf38dfff9e649d246e4d1ae3c85f37c13eb6195d70ef6674a5a10e0fc1172ba959af9cadf10"
    cookies["sid_tt"] = "d2407d3890c914e3722c00b394ef7e4f"
    cookies["sessionid"] = "d2407d3890c914e3722c00b394ef7e4f"
    cookies["qh[360]"] = "1"

    data={
        "keyword":"车祸",
        "offset":"0",
        "count":"10",
        "is_pull_refresh":"0",
        "search_source":"normal_search",
        "hot_search":"0",
        "latitude":"31.93758",
        "longtiude":"118.744453",
        "search_id":"",
        "query_correct_type":"1"
    }
    url = "https://aweme-hl.snssdk.com/aweme/v1/general/search/single/?os_api=25&device_type=M6%20Note&ssmix=a&manifest_version_code=721&dpi=480&js_sdk_version=1.19.4.8&uuid=86764803183702&app_name=aweme&version_name=7.2.1&ts="
    ts = str(int(time.time() * 1000))
    ticket = str(int(time.time() * 1000))
    url = url + ts + "&ac=wifi&app_type=normal&channel=meizu&update_version_code=7204&_rticket=" + ticket + "&device_platform=android&iid=79564990350&version_code=721&openudid=1b4b57f9e789e4c8&device_id=60270533422&resolution=1080*1920&device_brand=Meizu&language=zh&os_version=7.1.2&aid=1128&mcc_mnc=46011"
    print ts
    print ticket
    res = requests.post(url, headers = headers, data = data, cookies = cookies, verify=False)
    str = res.text
    f = open('a.json', 'w')
    f.write(str)

