import re
import math
import ipaddress
from urllib.parse import urlsplit
from collections import Counter

import tldextract

# Gunakan public suffix list bawaan library
extract_domain = tldextract.TLDExtract(suffix_list_urls=None)


def calculate_entropy(text):
    """
    Menghitung Shannon entropy dari karakter URL.
    """
    if not text:
        return 0.0

    counts = Counter(text)
    total = len(text)

    entropy = 0.0

    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)

    return entropy


def extract_features(url):
    """
    Mengubah URL menjadi 22 fitur numerik
    sesuai urutan fitur training Random Forest.
    """

    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL tidak boleh kosong.")

    url = url.strip()

    # URL harus memiliki skema
    if not re.match(r"^https?://", url, re.IGNORECASE):
        raise ValueError("URL harus diawali http:// atau https://")

    parsed = urlsplit(url)

    hostname = parsed.hostname

    if not hostname:
        raise ValueError("Hostname URL tidak valid.")

    # ======================================
    # 1. DOMAIN EXTRACTION
    # ======================================

    try:
        ipaddress.ip_address(hostname)
        is_ip = 1
    except ValueError:
        is_ip = 0

    if is_ip:
        dom = hostname
        tld = ""
        subdomain = ""
    else:
        extracted = extract_domain(hostname)

        dom = ".".join(part for part in [extracted.domain, extracted.suffix] if part)

        tld = extracted.suffix
        subdomain = extracted.subdomain

        if not dom:
            dom = hostname

    # ======================================
    # 2. CHARACTER COUNTS
    # ======================================

    url_len = len(url)

    letter_cnt = sum(c.isalpha() for c in url)
    digit_cnt = sum(c.isdigit() for c in url)

    special_cnt = url_len - letter_cnt - digit_cnt

    eq_cnt = url.count("=")
    qm_cnt = url.count("?")
    amp_cnt = url.count("&")
    dot_cnt = url.count(".")
    dash_cnt = url.count("-")
    under_cnt = url.count("_")
    slash_cnt = url.count("/")

    # ======================================
    # 3. DOMAIN FEATURES
    # ======================================

    dom_len = len(dom)
    tld_len = len(tld)

    subdom_cnt = len(subdomain.split(".")) if subdomain else 0

    # ======================================
    # 4. RATIOS
    # ======================================

    letter_ratio = letter_cnt / url_len
    digit_ratio = digit_cnt / url_len
    spec_ratio = special_cnt / url_len

    # ======================================
    # 5. PROTOCOL
    # ======================================

    is_https = int(parsed.scheme.lower() == "https")

    # ======================================
    # 6. ENTROPY AND PATH
    # ======================================

    entropy = calculate_entropy(url)

    path_len = len(parsed.path)
    query_len = len(parsed.query)

    # ======================================
    # 7. SUSUN FITUR
    # ======================================

    features = {
        "url_len": url_len,
        "dom_len": dom_len,
        "is_ip": is_ip,
        "tld_len": tld_len,
        "subdom_cnt": subdom_cnt,
        "letter_cnt": letter_cnt,
        "digit_cnt": digit_cnt,
        "special_cnt": special_cnt,
        "eq_cnt": eq_cnt,
        "qm_cnt": qm_cnt,
        "amp_cnt": amp_cnt,
        "dot_cnt": dot_cnt,
        "dash_cnt": dash_cnt,
        "under_cnt": under_cnt,
        "letter_ratio": letter_ratio,
        "digit_ratio": digit_ratio,
        "spec_ratio": spec_ratio,
        "is_https": is_https,
        "slash_cnt": slash_cnt,
        "entropy": entropy,
        "path_len": path_len,
        "query_len": query_len,
    }

    return features
