"""Honorbrook Onyx: the two public phone numbers, set in one place. Call 301, text 571.

CALL (301) 615-8289: the Honorbrook line, the owner's Google Voice Pro auto attendant ("Jessica").
TEXT (571) 354-0146: the owner's work number, still active for texts. An auto attendant cannot take texts.
Owner, Nov 20 2026: "confirm everywhere on the site that phone numbers listed are +1 301-615-8289", then
"text 5713540146 is still active ... so it should be call 301 text 571".

The live source (site/) and the older page generators still carry (571) 354-0146 as the call number. This pass rewrites every
written form of it in the built site to the call number. The text number is written by the build through the two tokens below,
and only as a text link or after the word "text". 1-800-MEDICARE (1-800-633-4227) is the only other number and is left alone.
To change a number, edit NEW (call) or TEXT_NUM (text) and rebuild."""
import glob
import os
import re

OLD = ('571', '354', '0146')
NEW = ('301', '615', '8289')
DISPLAY = '(%s) %s-%s' % NEW        # how it reads on the page
DASHED = '%s-%s-%s' % NEW           # schema writes +1-301-615-8289
DIGITS = '%s%s%s' % NEW             # tel:+1... links
TEXT_NUM = ('571', '354', '0146')   # the text line
TEXT_DISPLAY = '(%s) %s-%s' % TEXT_NUM
TEXT_HREF = 'sms:+1%s%s%s' % TEXT_NUM
T_NUM, T_HREF = '[[HB_TEXT]]', '[[HB_SMS]]'   # written by the build, filled in after the call number is rewritten
TEXT = ('.html', '.js', '.css', '.txt', '.xml', '.json', '.webmanifest', '.svg', '.md')
_LEFT = re.compile(r'%s\D{0,6}%s\D{0,4}%s' % OLD)
# the only places the text number may appear: a text link, or right after the word "text"
_OK = re.compile(r'<a [^>]*href="sms:[^"]*"[^>]*>[^<]*</a>|sms:\+1%s%s%s|[Tt]ext:? \(%s\) %s-%s' % (TEXT_NUM + TEXT_NUM))


def swap(s):
    s = s.replace('(%s) %s-%s' % OLD, DISPLAY)
    s = s.replace('%s-%s-%s' % OLD, DASHED)
    return re.sub(r'(?<![0-9])(1?)%s%s%s(?![0-9])' % OLD, lambda m: m.group(1) + DIGITS, s)


def _files(out):
    for f in glob.glob(os.path.join(out, '**', '*'), recursive=True):
        if '/assets/video' in f or os.path.islink(f) or not os.path.isfile(f): continue   # assets/video links back to the live source
        if f.endswith(TEXT) or os.path.basename(f) in ('_headers', '_redirects'): yield f


def apply(out):
    """Rewrite the call number everywhere in the built site and fill in the text number. Returns (files changed, call numbers changed, files where 571 shows as anything but the text number)."""
    files = n = 0
    for f in _files(out):
        s = open(f, encoding='utf-8', errors='surrogateescape').read()
        t = swap(s).replace(T_NUM, TEXT_DISPLAY).replace(T_HREF, TEXT_HREF)
        if t != s:
            n += len(_LEFT.findall(s)); files += 1
            open(f, 'w', encoding='utf-8', errors='surrogateescape').write(t)
    left = [f for f in _files(out) if _LEFT.search(_OK.sub('', open(f, encoding='utf-8', errors='surrogateescape').read()))]
    return files, n, left
