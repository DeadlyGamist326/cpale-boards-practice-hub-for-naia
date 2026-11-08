"""Encrypt a crops pack (rfbt-crops JSON) into per-card files for the public repo.
usage: enc.py PACK.json PASSWORD OUTDIR PACKLABEL
- PBKDF2-HMAC-SHA256(password, salt, ITER) -> 64 bytes: [0:32] AES-256-GCM key, [32:64] HMAC key for file names.
- crop file  OUTDIR/<hmac(jpeg)[:20]>.bin  = iv(12) | AES-GCM(jpeg bytes)
- manifest   OUTDIR/m-<hmac(manifest)[:20]>.bin = iv | AES-GCM(json {cardkey: [name, ref]})
- OUTDIR/meta.json (plain): salt, iter, manifest name, pack label
Unchanged crops keep their file name, so an update only adds the changed files. Salt is reused while the password is the same."""
import sys, os, json, base64, hmac, hashlib, secrets, glob
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
pack, pw, out, label = sys.argv[1:5]
ITER = 600000
os.makedirs(out, exist_ok=True)
mp = os.path.join(out, "meta.json")
meta = json.load(open(mp)) if os.path.exists(mp) else {}
salt = base64.b64decode(meta["salt"]) if meta.get("salt") else secrets.token_bytes(16)
dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, ITER, 64)
aes, hk = AESGCM(dk[:32]), dk[32:]
# same password? (old manifest must decrypt) else start fresh with a new salt
if meta.get("m"):
    try:
        b = open(os.path.join(out, meta["m"]), "rb").read(); aes.decrypt(b[:12], b[12:], None)
    except Exception:
        print("password changed: re-encrypting everything with a new salt")
        for f in glob.glob(os.path.join(out, "*.bin")): os.remove(f)
        salt = secrets.token_bytes(16); dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, ITER, 64); aes, hk = AESGCM(dk[:32]), dk[32:]
def enc(data): iv = secrets.token_bytes(12); return iv + aes.encrypt(iv, data, None)
def name(data): return hmac.new(hk, data, hashlib.sha256).hexdigest()[:20]
crops = json.load(open(pack))["crops"]
man, keep, new = {}, set(), 0
for ck, c in sorted(crops.items()):
    jpg = base64.b64decode(c["img"].split(",", 1)[1])
    n = name(jpg) + ".bin"; man[ck] = [n, c["ref"]]; keep.add(n)
    p = os.path.join(out, n)
    if not os.path.exists(p): open(p, "wb").write(enc(jpg)); new += 1
mb = json.dumps(man, separators=(",", ":"), sort_keys=True).encode()
mn = "m-" + name(mb) + ".bin"; keep.add(mn)
if not os.path.exists(os.path.join(out, mn)): open(os.path.join(out, mn), "wb").write(enc(mb))
gone = [f for f in glob.glob(os.path.join(out, "*.bin")) if os.path.basename(f) not in keep]
for f in gone: os.remove(f)
json.dump({"v": 1, "kdf": "PBKDF2-SHA256", "iter": ITER, "salt": base64.b64encode(salt).decode(), "m": mn, "pack": label, "n": len(man)}, open(mp, "w"))
tot = sum(os.path.getsize(f) for f in glob.glob(os.path.join(out, "*.bin")))
print(f"{len(man)} crops, {new} new files, {len(gone)} removed, total {tot/1e6:.1f} MB, manifest {mn}")
