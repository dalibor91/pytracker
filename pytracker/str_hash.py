import hashlib

def md5_hash(data):
    h = hashlib.md5();
    h.update(data);
    return h.hexdigest();
