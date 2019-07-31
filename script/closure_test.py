#!/usr/bin/env python
# coding=utf-8

g_login_url = "http://in.gpsoo.net/1/cardpool/account?method=login&login_name=root&passwd=goome@1703card&wechat_id=oex_1sxYp3OVkYBz0TlsWNhHLeS8"


def gen_url(**kw):
    base_url = "http://in.gpsoo.net/1/cardpool/account?method=login&"
    def concat_url(**kw):
        target_url = base_url
        for key in kw:
            target_url += key + '=' + kw[key] + '&'
        target_url = target_url[:-1]
        return target_url
    return concat_url

fun = gen_url()

dict_param = {'login_name':'root', 'passwd':'goome@1703card', 'wechat_id':'oex_1sxYp3OVkYBz0TlsWNhHLeS8'}
print(fun(**dict_param))


