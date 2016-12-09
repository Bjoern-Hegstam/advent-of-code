#!/usr/bin/env python

import fileinput

def split_ip(ip):
    parts = []
    if ip[0] == '[':
        left_idx = 1
    else:
        left_idx = 0

    for right_idx in range(1, len(ip)):
        if ip[right_idx] == '[':
            if left_idx == right_idx:
                left_idx = right_idx + 1
                continue

            parts.append((ip[left_idx:right_idx], False))
            left_idx = right_idx + 1
        elif ip[right_idx] == ']':
            parts.append((ip[left_idx:right_idx], True))
            left_idx = right_idx + 1
        elif right_idx == len(ip) - 1:
            parts.append((ip[left_idx:right_idx], False))

    return parts

def supports_tls(ip_parts):
    # Skip ip if any bracket part contains abba
    if any(contains_abba(p[0]) for p in ip_parts if p[1]):
        return False

    if any(contains_abba(p[0]) for p in ip_parts if not p[1]):
        return True

    return False

def contains_abba(s):
    for i in range(len(s) - 3):
        if s[i] != s[i + 1] and s[i] == s[i + 3] and s[i + 1] == s[i + 2]:
            return True

    return False

def supports_ssl(ip_parts):
    aba_s = [aba for part in ip_parts for aba in find_aba_s(part[0]) if not part[1]]
    bab_s = [aba for part in ip_parts for aba in find_aba_s(part[0]) if part[1]]

    invert_bab = lambda s: s[1] + s[0] + s[1]

    if any(invert_bab(bab) in aba_s for bab in bab_s):
        print(aba_s)
        print(bab_s)
        return True
    return False

def find_aba_s(s):
    res = []
    for i in range(len(s) - 2):
        if s[i] != s[i + 1] and s[i] == s[i + 2]:
            res.append(s[i:i+3])
    return res

if __name__ == '__main__':
    tls_count = 0
    ssl_count = 0

    for line in fileinput.input():
        ip_parts = split_ip(line)

        if supports_tls(ip_parts):
            tls_count += 1

        if supports_ssl(ip_parts):
            ssl_count += 1

    print('Supports TLS: %s' % tls_count)
    print('Supports SSL: %s' % ssl_count)
