# -*- coding: utf-8 -*-
"""
File Name:    curl
Author:       Cone
Date:         2022/3/15
"""
from cone.utils.network import curl



if __name__ == '__main__':
    a = curl.curl_to_request_kwargs('''
        curl 'https://www.toutiao.com/a7075223078497681923/?log_from=8783dc629c7aa_1647331371128' \
  -H 'authority: www.toutiao.com' \
  -H 'pragma: no-cache' \
  -H 'cache-control: no-cache' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-user: ?1' \
  -H 'sec-fetch-dest: document' \
  -H 'referer: https://www.toutiao.com/' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'cookie: __ac_signature=_02B4Z6wo00f01D2JOJgAAIDDqV9jlsxXMFg9qTwAAG1t77; ttcid=62ce170b60824fb58f01260b5ee2efe014; tt_webid=7050003492509648421; csrftoken=268d5801b4f5c4c8918dae96f0ece274; _S_WIN_WH=1440_789; _S_DPR=2; _S_IPAD=0; passport_csrf_token_default=37e1e5a62575773f8ae57cfe03e906ab; passport_csrf_token=37e1e5a62575773f8ae57cfe03e906ab; _ga=GA1.2.1634366833.1644831025; local_city_cache=%E6%9D%AD%E5%B7%9E; s_v_web_id=verify_l0qgioj4_ZQpZcbQW_QNXG_4H3T_82fi_0Tny9mOBvf22; _tea_utm_cache_24=undefined; MONITOR_WEB_ID=34ce6355-b275-4995-a3a5-58097c34b98f; tt_scid=PDoxXb72oKUZ0CQBAtB8fpIp0LvA7tYlL2YsZWFCsYNNVBi0Jv2rhD87-rVU0Xd60ea2; ttwid=1%7C28Aw7TdVZbwJ4ayoEpMCQPQMLe2jVTl-2qCena6_E3k%7C1647331373%7C6edfffe1f9986db4e5302365e05128da65ca5e44c7bd92949aff311cbb51e5f1' \
  --compressed
    ''')
    import requests
    response = requests.request(**a)
    print(response.text)
    print(response.status_code)