import re
import math
import tldextract
from urllib.parse import urlparse

def entropy(s):
    import collections
    p, l = collections.Counter(s), len(s)
    return -sum((count/l)*math.log2(count/l) for count in p.values())

def extract_url_features(url):
    parsed = urlparse(url)
    ext = tldextract.extract(url)
    domain = ext.domain + ('.' + ext.suffix if ext.suffix else '')
    feats = {
        "url_length": len(url),
        "domain_length": len(domain),
        "count_dots": url.count('.'),
        "count_hyphen": url.count('-'),
        "count_digits": sum(c.isdigit() for c in url),
        "has_ip": int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),
        "entropy": entropy(url),
    }
    for kw in ['login','secure','update','bank','free','verify','bonus']:
        feats[f'kw_{kw}'] = int(kw in url.lower())
    return feats
