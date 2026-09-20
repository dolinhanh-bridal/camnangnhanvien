# Dựng TOÀN BỘ bản chạy thật của cẩm nang trên web chính (dolinhanhbridal.com/nv-k9m3x7/)
#   python3 scripts/build_web.py <thu-muc-ra>          -> dựng
#   python3 scripts/build_web.py <thu-muc-ra> --up     -> dựng rồi FTP đè lên hosting
# Chạy TRONG repo camnangnhanvien.
#
# Quy ước từ 20/09/2026: file `<ten>-goc.html` trong repo là NGUỒN để sửa;
# `<ten>.html` trên GitHub chỉ là trang chuyển hướng — đừng sửa nội dung vào đó.
# Riêng cẩm nang: nguồn là `cam-nang-dla.html`, ra `index.html`.
# Bản artifact chị duyệt VẪN dựng từ `cam-nang-dla.html` gốc (giữ base64) — không dùng file này.
import re, sys, base64, hashlib, pathlib, subprocess

MOI  = 'https://dolinhanhbridal.com/nv-k9m3x7'
CU   = 'https://dolinhanh-bridal.github.io/camnangnhanvien'
CU2  = 'https://dolinhanh-bridal.github.io/web-thu'
ADIR = 'anh-cn'
FTP  = 'ftp://hf61-22156.azdigihost.com/nv-k9m3x7'
NETRC = str(pathlib.Path.home() / '.dla-azdigi.netrc')

TRANG = ['link', 'tiktok', 'checklist-do', 'gui-clip', 'duyet']   # <ten>-goc.html -> <ten>.html
EXT = {'jpeg':'jpg','jpg':'jpg','png':'png','gif':'gif','webp':'webp','svg+xml':'svg'}


def doi_link(s):
    s = s.replace(CU + '/', MOI + '/')          # mọi thứ đã chuyển sang web chính
    s = s.replace(CU2 + '/', 'https://dolinhanhbridal.com/')
    return s


def them_noindex(s):
    if '<meta name="robots"' in s:
        return s
    return re.sub(r'(<head[^>]*>)', r'\1\n<meta name="robots" content="noindex, nofollow">', s, count=1)


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

    def lazy(m):                      # ảnh popup chào phải hiện ngay, còn lại tải sau
        t = m.group(0)
        return t if ('loading=' in t or 'chao-img' in t) else t[:4] + ' loading="lazy" decoding="async"' + t[4:]

    return re.sub(r'<img\b[^>]*>', lazy, s), len(seen)


def dung_camnang(src, vo):
    nav = src.index('<nav class="topbar">')
    j = src.rindex('</style>', 0, nav) + len('</style>')
    duoi = src[j:]
    assert duoi[0] == '\n'
    return vo + src[:j] + '</head><body>' + duoi[1:] + '</body></html>'


ra = pathlib.Path(sys.argv[1]); ra.mkdir(parents=True, exist_ok=True)

# vỏ <!doctype…<body> lấy đúng y bản GitHub đã kiểm chứng (commit có index.html đầy đủ)
hs = subprocess.check_output(['git', 'show', 'fa5b43e:cam-nang-dla.html']).decode()
hi = subprocess.check_output(['git', 'show', 'fa5b43e:index.html']).decode()
vo = hi[:hi.find(hs[:200])]
assert dung_camnang(hs, vo) == hi, 'công thức vỏ lệch — dừng lại, đừng đẩy lên'
assert 'noindex' in vo, 'thiếu thẻ noindex'

# 1) cẩm nang
goc = pathlib.Path('cam-nang-dla.html').read_text()
than, n = tach_anh(doi_link(goc), ra / ADIR)
out = dung_camnang(than, vo)
(ra / 'index.html').write_text(out)
print(f'index.html    {len(goc)/1048576:5.2f} MB -> {len(out)/1048576:5.2f} MB  ({n} ảnh tách ra)')
con = out.count(CU)
print(f'              còn link GitHub: {con}' + ('' if con == 0 else '   ⚠️ KIỂM LẠI'))

# 2) các trang phụ
for t in TRANG:
    s = them_noindex(doi_link(pathlib.Path(f'{t}-goc.html').read_text()))
    (ra / f'{t}.html').write_text(s)
    print(f'{t+".html":14s}{len(s)/1024:5.0f} KB   noindex ' + ('ok' if 'noindex' in s else '⚠️ THIẾU')
          + f'   còn link GitHub: {s.count(CU)}')

# 3) .htaccess chặn con bọ tìm kiếm cho CẢ thư mục (kể cả ảnh, clip)
(ra / '.htaccess').write_text(
    '# Thư mục nội bộ nhân viên — không cho công cụ tìm kiếm lập chỉ mục\n'
    '<IfModule mod_headers.c>\n'
    '  Header set X-Robots-Tag "noindex, nofollow, noarchive, nosnippet"\n'
    '</IfModule>\n'
    'Options -Indexes\n')

if '--up' in sys.argv:
    import shlex
    print('\n--- đẩy lên hosting ---')
    for f in sorted(ra.rglob('*')):
        if f.is_dir():
            continue
        r = f.relative_to(ra)
        cmd = ['curl', '-s', '--netrc-file', NETRC, '--ftp-create-dirs', '-T', str(f),
               f'{FTP}/{r}', '-w', '%{http_code}', '--max-time', '600']
        code = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
        print(f'{str(r):34s} {code}' + ('' if code == '226' else '   ⚠️ LỖI'))
    print('xong')
