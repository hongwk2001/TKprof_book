import os

path = r"d:\git_repo\TKprof_book\books\frankenstein\chapters\ch_01_ko.txt"
with open(path, "rb") as f:
    raw_bytes = f.read()

try:
    decoded_utf8 = raw_bytes.decode('utf-8')
    print("Decoded directly as UTF-8 (repr first 200 chars):")
    print(repr(decoded_utf8[:200]))
except Exception as e:
    print("Direct UTF-8 decode failed:", e)

try:
    # Let's try reading as cp1252 and encoding back to bytes, then decoding as utf-8
    text_cp1252 = raw_bytes.decode('cp1252')
    bytes_recovered = text_cp1252.encode('cp1252')
    decoded_recovered = bytes_recovered.decode('utf-8')
    print("Recovered via cp1252 (repr first 200 chars):")
    print(repr(decoded_recovered[:200]))
except Exception as e:
    print("cp1252 recovery failed:", e)

try:
    # Let's try latin-1
    text_latin1 = raw_bytes.decode('latin-1')
    bytes_recovered = text_latin1.encode('latin-1')
    decoded_recovered = bytes_recovered.decode('utf-8')
    print("Recovered via latin-1 (repr first 200 chars):")
    print(repr(decoded_recovered[:200]))
except Exception as e:
    print("latin-1 recovery failed:", e)
