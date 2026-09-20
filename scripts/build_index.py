# Dung lai BAN DU PHONG day du tren GitHub (du-phong.html) tu cam-nang-dla.html.
# LUU Y 20/09/2026: index.html tren GitHub nay la TRANG CHUYEN HUONG — script nay
# KHONG duoc ghi vao index.html nua (ghi vao la mat trang chuyen huong).
# Ban chay that cua nhan vien dung bang scripts/build_web.py --up
import subprocess
def build(src, vo):
    nav = src.index('<nav class="topbar">'); j = src.rindex('</style>', 0, nav) + len('</style>')
    duoi = src[j:]; assert duoi[0] == '\n'
    return vo + src[:j] + '</head><body>' + duoi[1:] + '</body></html>'
# moc vo da kiem chung: commit fa5b43e con giu index.html day du
hs = subprocess.check_output(['git','show','fa5b43e:cam-nang-dla.html']).decode()
hi = subprocess.check_output(['git','show','fa5b43e:index.html']).decode()
vo = hi[:hi.find(hs[:200])]
assert build(hs, vo) == hi, 'cong thuc vo lech — dung lai'
open('du-phong.html','w',encoding='utf-8').write(build(open('cam-nang-dla.html',encoding='utf-8').read(), vo))
print('du-phong.html dung lai xong')
