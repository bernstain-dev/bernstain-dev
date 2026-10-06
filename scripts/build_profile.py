"""Generate a custom GitHub README hero and public stats with the standard library."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DISPLAY_NAME = "Bernstain O. Fangon"
DISPLAY_ROLE = "Full Stack Developer"
TAGLINE = "From the first pixel to the final query."
BG = "#0b1220"
PANEL = "#111e31"
LINE = "#25354c"
TEXT = "#eaf2ff"
MUTED = "#a6b6ce"
CYAN = "#54d7f5"
VIOLET = "#b99aff"
GREEN = "#63e5b5"
ROOT = Path(__file__).resolve().parents[1]


def label(x, y, value, size=14, color=TEXT, weight=400, mono=False):
    font = "'Courier New',monospace" if mono else "Arial,Helvetica,sans-serif"
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" font-family="{font}">{escape(str(value))}</text>')


def document(height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="980" height="{height}" viewBox="0 0 980 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M 28 0 L 0 0 0 28" fill="none" stroke="{LINE}" stroke-width="0.6" opacity="0.25"/></pattern>
  <linearGradient id="accent"><stop stop-color="{CYAN}"/><stop offset="0.55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient>
</defs>
<style>
 .cursor {{ animation: blink 1.3s steps(1) infinite; }}
 .status {{ animation: pulse 3s ease-in-out infinite; }}
 @keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}
 @keyframes pulse {{ 0%,100% {{ opacity:0.6 }} 50% {{ opacity:1 }} }}
 @media (prefers-reduced-motion: reduce) {{ .cursor,.status {{ animation:none; }} .packet {{ display:none; }} }}
</style>
<rect x="1" y="1" width="978" height="{height-2}" rx="22" fill="{BG}" stroke="{LINE}"/>
<rect x="2" y="2" width="976" height="{height-4}" rx="21" fill="url(#grid)"/>
{body}
</svg>'''


def hero():
    b = f'<rect x="34" y="32" width="5" height="32" rx="2" fill="url(#accent)"/>'
    b += label(53, 53, 'BERNSTAIN / THE BUILD LOG', 12, MUTED, 700, True)
    b += f'<circle class="status" cx="804" cy="49" r="4" fill="{GREEN}"/>'
    b += label(817, 53, 'BUILDING & LEARNING', 10, GREEN, 700, True)
    b += label(42, 123, DISPLAY_NAME, 49, TEXT, 700)
    b += label(44, 164, DISPLAY_ROLE, 23, CYAN, 700)
    b += label(44, 197, TAGLINE, 16, MUTED)
    b += f'<path d="M44 226 H936" stroke="{LINE}"/>'
    b += label(44, 252, 'ONE REQUEST. EVERY LAYER.', 11, MUTED, 700, True)
    for x, index, name, sub, accent in [
        (44, '01', 'FRONTEND', 'React / TypeScript', CYAN),
        (358, '02', 'BACKEND', 'Node.js / Express', VIOLET),
        (672, '03', 'DATABASE', 'PostgreSQL / Supabase', GREEN),
    ]:
        b += f'<rect x="{x}" y="273" width="264" height="128" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
        b += label(x+18, 297, index+' / '+name, 11, accent, 700, True)
        if index == '01':
            b += f'<rect x="{x+20}" y="312" width="32" height="25" rx="4" fill="none" stroke="{accent}" stroke-width="1.5"/><path d="M{x+20} 319 h32 M{x+31} 342 h10" stroke="{accent}"/>'
            b += label(x+64, 336, 'Design the experience', 14, TEXT, 700)
        elif index == '02':
            b += label(x+19, 337, '{ }', 25, accent, 700, True)
            b += label(x+64, 336, 'Connect the logic', 14, TEXT, 700)
        else:
            b += f'<ellipse cx="{x+36}" cy="316" rx="15" ry="5" fill="none" stroke="{accent}"/><path d="M{x+21} 316 v20 c0 7 30 7 30 0 v-20 M{x+21} 326 c0 7 30 7 30 0" fill="none" stroke="{accent}"/>'
            b += label(x+64, 336, 'Give data structure', 14, TEXT, 700)
        b += label(x+18, 375, sub, 13, MUTED, 400, True)
    for start in [308, 622]:
        b += f'<path d="M{start} 337 h50 m-7 -5 l7 5 -7 5" fill="none" stroke="{MUTED}" stroke-width="1.5"/>'
    b += f'<path d="M804 401 V429 H176 V401" fill="none" stroke="{LINE}" stroke-width="2"/>'
    b += f'<path d="M171 408 l5 -7 5 7" fill="none" stroke="{MUTED}"/>'
    b += f'<g transform="translate(308 337)"><circle class="packet" r="4" fill="{CYAN}"><animateMotion dur="6s" repeatCount="indefinite" path="M0 0 H50 M314 0 H364 M496 64 V92 H-132 V64"/></circle></g>'
    b += f'<rect x="413" y="420" width="154" height="18" rx="9" fill="{BG}"/>'
    b += label(427, 433, 'RESPONSE / 200 OK', 10, GREEN, 700, True)
    b += label(44, 479, '> understand. build. refine.', 13, MUTED, 400, True)
    b += f'<rect class="cursor" x="280" y="468" width="8" height="14" fill="{CYAN}"/>'
    b += label(730, 479, 'UI  /  API  /  DATA', 11, MUTED, 400, True)
    return document(510, f'{DISPLAY_NAME} — {DISPLAY_ROLE}',
                    'A stylized request and response moves between frontend, backend, and database layers. This is a decorative animation.', b)


def get_json(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'fullstack-profile-kit'}
    token = os.getenv('GH_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    with urlopen(Request('https://api.github.com' + path, headers=headers), timeout=25) as response:
        return json.load(response)


def load_public(username):
    user = get_json(f'/users/{username}')
    repos = []
    page = 1
    while True:
        batch = get_json(f'/users/{username}/repos?type=owner&per_page=100&page={page}')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    originals = [r for r in repos if not r.get('private') and not r.get('fork')
                 and r['owner']['login'].lower() == username.lower()]
    languages = Counter(r['language'] for r in originals if r.get('language'))
    return {'repos': user['public_repos'], 'followers': user['followers'],
            'stars': sum(r['stargazers_count'] for r in originals),
            'languages': languages.most_common(3)}


def stats(data, username):
    starter = data is None
    b = label(34, 39, 'BUILD TELEMETRY', 12, CYAN, 700, True)
    stamp = 'Awaiting first update' if starter else datetime.now(timezone.utc).strftime('Updated %Y-%m-%d / UTC')
    b += label(720, 39, stamp, 11, MUTED, 400, True)
    for x, title, value, note, accent in [
        (34, 'PUBLIC REPOSITORIES', '—' if starter else data['repos'], 'Includes public forks', CYAN),
        (343, 'GITHUB FOLLOWERS', '—' if starter else data['followers'], 'Public profile followers', VIOLET),
        (652, 'REPOSITORY STARS', '—' if starter else data['stars'], 'Owned public non-fork repos', GREEN),
    ]:
        b += f'<rect x="{x}" y="63" width="294" height="119" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
        b += label(x+18, 87, title, 10, MUTED, 700, True)
        b += label(x+18, 136, value, 40, accent, 700)
        b += label(x+18, 163, note, 11, MUTED)
    b += label(34, 216, 'PRIMARY LANGUAGES / REPOSITORY COUNTS', 11, MUTED, 700, True)
    languages = [] if starter else data['languages']
    if languages:
        for i, (name, count) in enumerate(languages):
            x = 34 + 309*i
            b += f'<rect x="{x}" y="234" width="294" height="38" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
            b += label(x+14, 258, str(name)[:25], 13, TEXT, 700)
            b += label(x+250, 258, count, 13, CYAN, 700, True)
    else:
        b += label(34, 254, 'Run the profile workflow to load your data.' if starter else 'No primary-language data in public non-fork repositories.', 13, MUTED)
    footer = 'Public data only. No sample statistics.' if starter else f'@{username} / Public data only / Refreshed daily'
    b += label(34, 303, footer, 11, MUTED, 400, True)
    return document(328, 'GitHub public profile statistics',
                    'Public repositories, followers, and stars. Languages are counted by primary language in owned public non-fork repositories. '+stamp, b)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', help='GitHub user whose public data should be displayed')
    parser.add_argument('--starter', action='store_true', help='Generate honest placeholders without network requests')
    args = parser.parse_args()
    if not args.starter and (not args.username or not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?', args.username)):
        parser.error('Provide a valid GitHub username or use --starter.')
    try:
        data = None if args.starter else load_public(args.username)
    except (HTTPError, URLError, TimeoutError, KeyError, ValueError) as error:
        # Do not overwrite good assets with invented numbers or partially fetched data.
        print(f'Profile refresh failed ({type(error).__name__}); existing assets preserved.', file=sys.stderr)
        return 1
    output = ROOT / 'assets'
    output.mkdir(exist_ok=True)
    for name, content in [('fullstack-banner.svg', hero()), ('github-stats.svg', stats(data, args.username))]:
        (output / name).write_text(content, encoding='utf-8')
    print('Generated banner and public statistics card.' if data is not None else 'Generated banner and starter statistics card.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
