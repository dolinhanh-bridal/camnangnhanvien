# Dựng BẢN WEB CHÍNH của cẩm nang (dolinhanhbridal.com) — chạy TRONG repo camnangnhanvien.
#   python3 scripts/build_web.py <thu-muc-ra>
# Khác bản GitHub 2 chỗ: (1) ảnh base64 tách ra file riêng + tải sau (lazy)
#                        (2) link các trang đã chuyển nhà trỏ về host mới
# Bản artifact chị duyệt VẪN dựng từ cam-nang-dla.html gốc (giữ base64) — đừng dựng từ file này.
import re, sys, base64, hashlib, pathlib, subprocess

MOI = 'https://dolinhanhbridal.com/nv-k9m3x7'
CU  = 'https://dolinhanh-bridal.github.io/camnangnhanvien'
ADIR = 'anh-cn'

# trang đã chuyển sang web chính (còn lại vẫn ở GitHub: clip, PDF, timeline, checklist-do, form, duyet, gui-clip)
DA_CHUYEN = []   # link.html / tiktok.html van o GitHub (phien khac hay sua) — khong doi link
EXT = {'jpeg':'jpg','jpg':'jpg','png':'png','gif':'gif','webp':'webp','svg+xml':'svg'}


def tach_anh(s, d):
    d.mkdir(parents=True, exist_ok=True)
    seen = {}

    def thay(m):
        raw = base64.b64decode(re.sub(r'\s+', '', m.group(2)))
        h = hashlib.sha1(raw).hexdigest()[:12]
        if h not in seen:
            seen[h] = f"{h}.{EXT.get(m.group(1), 'bin')}"
            (d / seen[h]).write_bytes(raw)
        return f"{ADIR}/{seen[h]}"

    s = re.sub(r'data:image/(png|jpeg|jpg|gif|webp|svg\+xml);base64,([A-Za-z0-9+/=\s]+)', thay, s)

    def lazy(m):                      # ảnh popup chào hiện ngay, còn lại tải sau
        t = m.group(0)
        return t if ('loading=' in t or 'chao-img' in t) else t[:4] + ' loading="lazy" decoding="async"' + t[4:]

    return re.sub(r'<img\b[^>]*>', lazy, s), len(seen)


def doi_link(s):
    for f in DA_CHUYEN:
        s = s.replace(f'{CU}/{f}', f'{MOI}/{f}')
    s = s.replace(f'href="{CU}/"', f'href="{MOI}/"')
    # web-thu trên GitHub -> web chính (cùng nội dung, nhanh hơn ~45 lần)
    s = s.replace('https://dolinhanh-bridal.github.io/web-thu/', 'https://dolinhanhbridal.com/')
    return s


def dung(src, vo):
    nav = src.index('<nav class="topbar">')
    j = src.rindex('</style>', 0, nav) + len('</style>')
    duoi = src[j:]
    assert duoi[0] == '\n'
    return vo + src[:j] + '</head><body>' + duoi[1:] + '</body></html>'


ra = pathlib.Path(sys.argv[1]); ra.mkdir(parents=True, exist_ok=True)

# lấy phần vỏ <!doctype…<body> đúng y bản GitHub đang chạy
hs = subprocess.check_output(['git', 'show', 'HEAD:cam-nang-dla.html']).decode()
hi = subprocess.check_output(['git', 'show', 'HEAD:index.html']).decode()
vo = hi[:hi.find(hs[:200])]
assert dung(hs, vo) == hi, 'công thức vỏ lệch với HEAD — dừng lại, đừng đẩy lên'
assert 'noindex' in vo, 'thiếu thẻ noindex'

goc = pathlib.Path('cam-nang-dla.html').read_text()
than, n = tach_anh(doi_link(goc), ra / ADIR)
out = dung(than, vo)
(ra / 'index.html').write_text(out)

print(f'ảnh tách ra : {n} file')
print(f'cam-nang-dla: {len(goc)/1048576:.2f} MB  ->  index.html {len(out)/1048576:.2f} MB')
print(f'còn base64  : {out.count("data:image")} chỗ')
