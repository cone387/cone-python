# -*- coding: utf-8 -*-
"""
File Name:    curl
Author:       Cone
Date:         2022/3/15
"""
import argparse
import warnings
from shlex import split
from http.cookies import SimpleCookie
from urllib.parse import urlparse

# copy from scrapy
class CurlParser(argparse.ArgumentParser):
    def error(self, message):
        error_msg = f'There was an error parsing the curl command: {message}'
        raise ValueError(error_msg)


curl_parser = CurlParser()
curl_parser.add_argument('url')
curl_parser.add_argument('-H', '--header', dest='headers', action='append')
curl_parser.add_argument('-X', '--request', dest='method')
curl_parser.add_argument('-d', '--data', '--data-raw', dest='data')
curl_parser.add_argument('-u', '--user', dest='auth')


safe_to_ignore_arguments = [
    ['--compressed'],
    # `--compressed` argument is not safe to ignore, but it's included here
    # because the `HttpCompressionMiddleware` is enabled by default
    ['-s', '--silent'],
    ['-v', '--verbose'],
    ['-#', '--progress-bar']
]

for argument in safe_to_ignore_arguments:
    curl_parser.add_argument(*argument, action='store_true')


def _parse_headers_and_cookies(parsed_args):
    headers = {}
    cookies = {}
    for header in parsed_args.headers or ():
        name, val = header.split(':', 1)
        name = name.strip()
        val = val.strip()
        if name.title() == 'Cookie':
            for name, morsel in SimpleCookie(val).items():
                cookies[name] = morsel.value
        else:
            headers[name] = val

    return headers, cookies


def curl_to_request_kwargs(curl_command: str, ignore_unknown_options: bool = True) -> dict:
    """Convert a cURL command syntax to Request kwargs.

    :param str curl_command: string containing the curl command
    :param bool ignore_unknown_options: If true, only a warning is emitted when
                                        cURL options are unknown. Otherwise
                                        raises an error. (default: True)
    :return: dictionary of Request kwargs
    """

    curl_args = split(curl_command)

    if curl_args[0] != 'curl':
        raise ValueError('A curl command must start with "curl"')

    parsed_args, argv = curl_parser.parse_known_args(curl_args[1:])

    if argv:
        msg = f'Unrecognized options: {", ".join(argv)}'
        if ignore_unknown_options:
            warnings.warn(msg)
        else:
            raise ValueError(msg)

    url = parsed_args.url

    # curl automatically prepends 'http' if the scheme is missing, but Request
    # needs the scheme to work
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url

    method = parsed_args.method or 'GET'

    result = {'method': method.upper(), 'url': url}

    headers, cookies = _parse_headers_and_cookies(parsed_args)

    if headers:
        result['headers'] = headers
    if cookies:
        result['cookies'] = cookies
    if parsed_args.data:
        result['body'] = parsed_args.data
        if not parsed_args.method:
            # if the "data" is specified but the "method" is not specified,
            # the default method is 'POST'
            result['method'] = 'POST'

    return result



if __name__ == '__main__':
    a = curl_to_request_kwargs('''
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