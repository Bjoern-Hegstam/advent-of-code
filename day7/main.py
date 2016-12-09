#!/usr/bin/env python

import fileinput

tls_count = 0

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

if __name__ == '__main__':
    for line in fileinput.input():
        ip_parts = split_ip(line)

        if supports_tls(ip_parts):
            tls_count += 1

    print(tls_count)
