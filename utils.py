import pickle
import re

import string
import pandas as pd
import numpy
from urllib.parse import urlparse
from tld import get_tld


clf = pickle.load(open("models/clf.pkl", "rb"))


def having_ip_address(url):
    match = re.search(
        "(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\."
        "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|"  # IPv4
        "((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)"  # IPv4 in hexadecimal
        "(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}",
        url,
    )  # Ipv6
    if match:
        # print match.group()
        return 1
    else:
        # print 'No matching pattern found'
        return 0


def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count("/")


def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return len(urlpath.split("/")[1])
    except:
        return 0


def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1


def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits


def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters

    # def process_url(url){
    #     df['use_of_ip'] = having_ip_address(url)
    #     df['abnormal_url'] =  abnormal_url(url)
    #     df['count.'] =  url.count('.')
    #     df['count-www'] = url.count('www')
    #     df['count@'] = url.count('@')
    #     df['count_dir'] = no_of_dir(url)
    #     df['count_embed_domian'] = no_of_embed(url)
    #     df['short_url'] = shortening_service(url)
    #     df['count-https'] = url.count('https')
    #     df['count-http'] = url.count('http')
    #     df['count%'] = url.count('%')
    #     df['count?'] = url.count('?')
    #     df['count-'] = url.count('-')
    #     df['count='] = url.count('=')
    #     df['url_length'] = len(str(url))
    #     df['hostname_length'] = len(urlparse(url).netloc)
    #     df['sus_url'] = suspicious_words(url)
    #     df['fd_length'] = fd_length(url)
    #     df['tld'] = get_tld(url,fail_silently=True)
    #     df['tld_length'] = df['tld'].apply(lambda i: tld_length(i))
    #     df = df.drop("tld",axis = 1)
    #     df['count-digits']= digit_count(url)
    #     df['count-letters']= letter_count(url)

    # }


def model_predict(url):
    if url == "":
        return ""
    df = pd.DataFrame([url], columns=["url"])

    df["use_of_ip"] = having_ip_address(url)
    # df["abnormal_url"] = abnormal_url(url)
    df["count."] = url.count(".")
    df["count-www"] = url.count("www")
    df["count@"] = url.count("@")
    df["count_dir"] = no_of_dir(url)
    df["path_length"] = len(urlparse(url).path)
    # df["count_embed_domian"] = no_of_embed(url)
    # df["short_url"] = shortening_service(url)
    df["count-https"] = url.count("https")
    df["count-http"] = url.count("http")
    df["count%"] = url.count("%")
    df["count?"] = url.count("?")
    df["count-"] = url.count("-")
    df["count="] = url.count("=")
    df["url_length"] = len(str(url))
    df["hostname_length"] = len(urlparse(url).netloc)
    # df["sus_url"] = suspicious_words(url)
    df["fd_length"] = fd_length(url)
    df["tld"] = get_tld(url, fail_silently=True)
    df["tld_length"] = df["tld"].apply(lambda i: tld_length(i))
    df = df.drop("tld", axis=1)
    df["count-digits"] = digit_count(url)
    df["count-letters"] = letter_count(url)
    df.drop("url", axis=1)

    X = df[
        [
            "hostname_length",
            "path_length",
            "fd_length",
            "tld_length",
            "count-",
            "count@",
            "count?",
            "count%",
            "count.",
            "count=",
            "count-http",
            "count-https",
            "count-www",
            "count-digits",
            "count-letters",
            "count_dir",
            "use_of_ip",
        ]
    ]

    prediction = clf.predict(X)

    prediction = 1 if prediction == 1 else -1
    return prediction
