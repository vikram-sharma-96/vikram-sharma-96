"""Generate GitHub-safe animated SVGs. Daily refresh uses only Python stdlib."""
import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
BG, FG, MUTED, GREEN = '#0d1117', '#e6edf3', '#8b949e', '#7ee787'

def text(x, y, value, size=14, color=FG, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{html.escape(str(value))}</text>'

def svg(width, height, body, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title, quote=True)}">
<title>{html.escape(title)}</title>
<style>text{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}.reveal{{animation:appear .55s both}}@keyframes appear{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}@media(prefers-reduced-motion:reduce){{.reveal{{animation:none}}}}</style>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="14" fill="{BG}" stroke="#30363d"/>
{body}</svg>'''

def save(name, content):
    (ROOT / name).write_text(content, encoding='utf-8')

def card():
    body = text(26, 34, '$ neofetch', 13, GREEN)
    body += '<path d="M26 52H464" stroke="#30363d"/>'
    body += text(26, 90, CFG['name'], 27)
    body += text(26, 117, '@' + CFG['username'], 13, MUTED)
    rows = [('STATUS', CFG['role']), ('STACK', CFG['stack']), ('BUILDING', CFG['building']), ('PROJECT', CFG['project'])]
    for i, (label, value) in enumerate(rows):
        y = 161 + i * 55
        body += f'<g class="reveal" style="animation-delay:{.2+i*.18}s">' + text(26, y, label, 10, GREEN) + text(26, y+22, value, 14) + '</g>'
    body += ''.join(f'<rect x="{26+i*26}" y="379" width="20" height="8" rx="2" fill="{c}"/>' for i,c in enumerate(['#238636','#3fb950',GREEN,'#a5d6ff','#79c0ff','#d2a8ff']))
    save('info-card.svg', svg(490, 415, body, f"{CFG['name']} — {CFG['role']}. {CFG['stack']}"))

def portrait(path):
    # Pillow is needed only when changing the avatar, never for daily updates.
    from PIL import Image, ImageOps
    source = Image.open(path).convert('RGBA')
    canvas = Image.new('RGBA', source.size, 'white')
    canvas.alpha_composite(source)
    gray = ImageOps.autocontrast(canvas.convert('L')).resize((80, 43))
    ramp = ' .:-=+*#%@'
    body = text(20, 30, '$ cat avatar.txt', 12, GREEN)
    for y in range(43):
        line = ''.join(ramp[min(9, (255-gray.getpixel((x,y)))*10//256)] for x in range(80))
        body += f'<g class="reveal" style="animation-delay:{y*.035}s">' + text(19, 56+y*7.6, line, 6.7, '#c9d1d9', 'xml:space="preserve" textLength="332" lengthAdjust="spacingAndGlyphs"') + '</g>'
    body += text(20, 397, 'avatar loaded // ready', 10, MUTED)
    save('avatar-ascii.svg', svg(370, 415, body, 'Animated ASCII version of the GitHub avatar'))

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days, self.tips, self.active = {}, {}, None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('data-date') and a.get('data-level') is not None:
            self.days[a['id']] = {'date': a['data-date'], 'level': int(a['data-level'])}
        if tag == 'tool-tip' and a.get('for'):
            self.active = a['for']
            self.tips[self.active] = ''
    def handle_data(self, data):
        if self.active:
            self.tips[self.active] += data
    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            self.active = None

def heatmap(local=None):
    if local:
        raw = Path(local).read_text(encoding='utf-8')
    else:
        req = urllib.request.Request(f"https://github.com/users/{CFG['username']}/contributions", headers={'User-Agent':'github-profile-art','Accept-Language':'en-US'})
        with urllib.request.urlopen(req, timeout=45) as response:
            raw = response.read().decode('utf-8')
    parser = Calendar()
    parser.feed(raw)
    days = []
    for key, day in parser.days.items():
        tip = parser.tips.get(key, '').strip()
        match = re.match(r'(No|[\d,]+) contributions?\b', tip)
        if not match:
            raise ValueError(f'Unrecognized contribution tooltip for {day["date"]}: {tip}')
        day['count'] = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
        if day['level'] not in range(5):
            raise ValueError('Unsupported GitHub contribution level')
        days.append(day)
    days.sort(key=lambda d: d['date'])
    if not 350 <= len(days) <= 371 or len({d['date'] for d in days}) != len(days):
        raise ValueError('Incomplete contribution calendar; keeping previous SVG')
    start = dt.date.fromisoformat(days[0]['date'])
    origin = start - dt.timedelta(days=(start.weekday()+1)%7)
    total = sum(day['count'] for day in days)
    body = text(26, 34, '$ ./contributions.sh', 13, GREEN)
    body += text(26, 67, f'{total:,} contributions', 23)
    body += text(26, 90, days[0]['date'] + ' — ' + days[-1]['date'], 11, MUTED)
    colors = ['#161b22','#0e4429','#006d32','#26a641','#39d353']
    for label, row in [('Mon',1),('Wed',3),('Fri',5)]:
        body += text(26, 124+row*14, label, 9, MUTED)
    for day in days:
        offset = (dt.date.fromisoformat(day['date'])-origin).days
        col, row = divmod(offset,7)
        body += f'<rect class="reveal" style="animation-delay:{(col+row)*.016:.3f}s" x="{65+col*14}" y="{115+row*14}" width="10" height="10" rx="2" fill="{colors[day["level"]]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>'
    body += text(26, 242, 'Real activity. Refreshed daily.', 11, MUTED)
    body += text(671, 242, 'Less', 10, MUTED)
    for i,c in enumerate(colors):
        body += f'<rect x="{704+i*14}" y="232" width="10" height="10" rx="2" fill="{c}"/>'
    body += text(779,242,'More',10,MUTED)
    (ROOT / 'data').mkdir(exist_ok=True)
    save('data/contributions.json', json.dumps({'username':CFG['username'],'total':total,'days':days},indent=2)+'\n')
    save('contrib-heatmap.svg', svg(860, 268, body, f'{total} GitHub contributions from {days[0]["date"]} to {days[-1]["date"]}'))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--calendar-html')
    ap.add_argument('--avatar')
    ap.add_argument('--heatmap-only', action='store_true')
    args = ap.parse_args()
    if not args.heatmap_only:
        card()
        if args.avatar:
            portrait(args.avatar)
    heatmap(args.calendar_html)
