# Dựng lại các trang CHUYỂN HƯỚNG trên GitHub (giữ nguyên ?query và #hash).
#   python3 scripts/lam_chuyen_huong.py      — chạy trong repo
import pathlib
MOI = 'https://dolinhanhbridal.com/nv-k9m3x7'
TRANG = {'index.html': '/', 'link.html': '/link.html', 'tiktok.html': '/tiktok.html',
         'checklist-do.html': '/checklist-do.html',
         'gui-clip.html': '/gui-clip.html', 'duyet.html': '/duyet.html'}
MAU = '''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Cẩm nang DLA</title>
<style>
  body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#fff;
       font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;color:#2b2b2b}}
  .h{{text-align:center;padding:28px 22px;max-width:420px}}
  .t{{font-size:19px;font-weight:600;color:#7B2D3B;margin:0 0 10px}}
  .p{{font-size:15px;line-height:1.6;margin:0 0 20px;color:#555}}
  .b{{display:inline-block;background:#7B2D3B;color:#fff;text-decoration:none;
      padding:13px 26px;border-radius:999px;font-size:15px;font-weight:600}}
</style>
</head>
<body>
<div class="h">
  <p class="t">Đã chuyển sang địa chỉ mới</p>
  <p class="p">Đang mở giúp bạn… Trang mới nhanh hơn nhiều.<br>Nhớ lưu lại link mới nhé.</p>
  <a class="b" id="di" href="{dich}">Mở trang →</a>
</div>
<script>
  var d = "{dich}" + location.search + location.hash;
  document.getElementById('di').href = d;
  location.replace(d);
</script>
</body>
</html>
'''
for f, duong in TRANG.items():
    pathlib.Path(f).write_text(MAU.format(dich=MOI + duong))
print('đã dựng', len(TRANG), 'trang chuyển hướng')
