#!/usr/bin/env python3
"""
Pobiera zdjęcia i filmy z domeny publicznej / wolnych licencji do folderu "media"
i zapisuje media/media.js z informacjami o autorach i licencjach.

Źródła: Wikimedia Commons (API), awaryjnie Internet Archive (tylko pliki
oznaczone jako public domain / Creative Commons).

Użycie:   python3 pobierz_media.py            (pobiera brakujące pliki)
          python3 pobierz_media.py --force    (pobiera wszystko od nowa)

Wymaga tylko Pythona 3.8+. Jeśli w systemie jest ffmpeg, filmy zostaną
przycięte do ~40 s, żeby folder nie był zbyt duży.

Wyniki wyszukiwania są automatyczne – po pobraniu warto przejrzeć prezentację
(klawisz I pokazuje listę źródeł) i podmienić nietrafione pliki ręcznie:
wystarczy wrzucić do media/ plik o nazwie <id>.jpg / <id>.webm / <id>.mp4.
"""
import json, os, re, shutil, subprocess, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "media")
UA = "CuriePresentation/1.0 (educational slideshow; python-urllib)"
COMMONS = "https://commons.wikimedia.org/w/api.php"
MAX_VIDEO_MB = 80
CLIP_SECONDS = 40

# id: (rodzaj, [dokładne tytuły plików do sprawdzenia najpierw], [zapytania wyszukiwania])
SLOTS = {
    # --- zdjęcia ---
    "portret_1920":      ("img", ["File:Marie Curie c1920.jpg"], ["Marie Curie portrait 1920"]),
    "portret_mlody":     ("img", ["File:Mariecurie.jpg", "File:Marie Curie c. 1903.jpg"], ["Marie Curie 1903 portrait"]),
    "portret_nobel":     ("img", ["File:Marie Curie (Nobel-Chem).jpg", "File:Marie Curie 1911.jpg"], ["Marie Curie Nobel 1911 portrait"]),
    "rodzina":           ("img", [], ["Władysław Skłodowski córki", "Skłodowski daughters", "Wladyslaw Sklodowski daughters"]),
    "ojciec":            ("img", [], ["Władysław Skłodowski", "Wladyslaw Sklodowski"]),
    "irene":             ("img", [], ["Irène Joliot-Curie portrait", "Irene Curie 1920s"]),
    "eve":               ("img", [], ["Ève Curie portrait", "Eve Curie"]),
    "matka":             ("img", [], ["Bronisława Skłodowska Boguska", "Bronislawa Sklodowska mother Marie Curie"]),
    "maria_uczennica":   ("img", [], ["Maria Skłodowska 1883", "Marie Sklodowska 16 years", "Maria Skłodowska młodość"]),
    "warszawa_kamienice":("img", [], ["Warszawa Stare Miasto XIX wiek", "Warsaw Old Town 19th century photograph", "Rynek Starego Miasta Warszawa 1890"]),
    "szczuki":           ("img", [], ["Szczuki dwór Żorawskich", "Szczuki Skłodowska"]),
    "bronislawa":        ("img", [], ["Bronisława Dłuska", "Bronislawa Dluska"]),
    "piotr":             ("img", ["File:Pierre Curie by Dujardin c1906.jpg"], ["Pierre Curie portrait"]),
    "slub_rowery":       ("img", [], ["Pierre Marie Curie bicycles", "Marie Pierre Curie 1895 wedding"]),
    "elektrometr":       ("img", [], ["Curie electrometer", "Curie piezoelectric quartz electrometer"]),
    "laboratorium_curie":("img", ["File:Pierre and Marie Curie.jpg"], ["Pierre Marie Curie laboratory"]),
    "castaigne":         ("img", ["File:Curie and radium by Castaigne.jpg"], ["Curie radium Castaigne"]),
    "corki":             ("img", [], ["Marie Curie daughters Irène Ève", "Marie Curie with her daughters 1908"]),
    "maria_1906":        ("img", [], ["Marie Curie laboratory 1906", "Marie Curie laboratory Sorbonne"]),
    "instytut_paryz":    ("img", [], ["Institut du Radium Paris Pavillon Curie", "Institut Curie Pavillon Curie"]),
    "panteon":           ("img", [], ["Panthéon Paris façade", "Pantheon Paris"]),
    # --- filmy ---
    "film_warszawa_dawna":   ("video", [], ["Warszawa filetype:video 1910", "Warsaw filetype:video 1915", "Warszawa filetype:video"]),
    "film_paryz_lumiere":    ("video", [], ["Lumière Paris filetype:video", "Paris 1896 filetype:video", "Paris 1890s filetype:video"]),
    "film_paryz_1900":       ("video", [], ["Exposition Universelle 1900 filetype:video", "Paris 1900 filetype:video"]),
    "film_laboratorium":     ("video", [], ["chemistry laboratory 1920s filetype:video", "laboratory 1910s filetype:video", "laboratory film 1920 filetype:video"]),
    "film_promieniotworczosc":("video", [], ["radium filetype:video", "radioactivity filetype:video", "cloud chamber filetype:video"]),
    "film_curie_archiwum":   ("video", [], ["Marie Curie filetype:video", "Curie Institut du Radium filetype:video"]),
    "film_wojna":            ("video", [], ["World War I ambulance filetype:video", "World War I field hospital filetype:video", "Western Front 1916 filetype:video"]),
    "film_rtg":              ("video", [], ["X-ray 1896 filetype:video", "X-ray machine filetype:video", "radiography history filetype:video"]),
    "film_usa_1921":         ("video", [], ["Marie Curie 1921 filetype:video", "Madame Curie America filetype:video", "Marie Curie Harding filetype:video"]),
    "film_warszawa_1930":    ("video", [], ["Warszawa 1930 filetype:video", "Warsaw 1930s filetype:video", "Warszawa 1938 filetype:video"]),
}
# Zapytania awaryjne w Internet Archive (dla filmów, których nie ma na Commons)
IA_QUERIES = {
    "film_warszawa_dawna": "Warsaw 1910",
    "film_paryz_lumiere": "Lumiere Paris",
    "film_paryz_1900": "Paris 1900 exposition",
    "film_laboratorium": "chemistry laboratory 1920s",
    "film_promieniotworczosc": "radium",
    "film_curie_archiwum": "Marie Curie",
    "film_wojna": "World War I ambulance",
    "film_rtg": "x-ray history",
    "film_usa_1921": "Madame Curie 1921",
    "film_warszawa_1930": "Warsaw 1930s",
}


def get_json(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    tmp = path + ".part"
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f, 1 << 16)
    os.replace(tmp, path)


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def commons_info(titles=None, search=None, kind="img"):
    p = {"action": "query", "format": "json", "prop": "imageinfo|videoinfo",
         "iiprop": "url|mime|size|extmetadata", "iiurlwidth": 1600,
         "viprop": "url|mime|size|extmetadata|derivatives"}
    if titles:
        p["titles"] = "|".join(titles)
    else:
        p.update(generator="search", gsrnamespace=6, gsrlimit=12, gsrsearch=search)
    pages = get_json(COMMONS, p).get("query", {}).get("pages", {})
    pages = sorted(pages.values(), key=lambda x: x.get("index", 0))
    out = []
    for pg in pages:
        info = (pg.get("videoinfo") or pg.get("imageinfo") or [None])[0]
        if not info:
            continue
        mime = info.get("mime", "")
        if kind == "img" and not mime.startswith("image/"):
            continue
        if kind == "video" and not (mime.startswith("video/") or mime == "application/ogg"):
            continue
        out.append((pg["title"], info))
    return out


def pick_video_url(info):
    """Wybiera wersję webm/mp4 ≤720p (przeglądarki nie zawsze grają ogv)."""
    ders = info.get("derivatives") or []
    good = [d for d in ders if ("webm" in d.get("type", "") or "mp4" in d.get("type", ""))]
    good.sort(key=lambda d: (abs((d.get("height") or 480) - 480)))
    if good:
        return good[0]["src"]
    if info.get("mime") in ("video/webm", "video/mp4"):
        return info["url"]
    return None


def meta(info, title, source):
    em = info.get("extmetadata", {})
    g = lambda k: strip_html(em.get(k, {}).get("value", ""))
    return {"title": g("ObjectName") or title.replace("File:", ""),
            "author": g("Artist")[:120] or "autor nieznany",
            "license": g("LicenseShortName") or "domena publiczna",
            "source": source}


def free_license(m):
    l = m["license"].lower()
    return any(k in l for k in ("public domain", "pd", "cc0", "cc by", "cc-by", "domena", "no restrictions"))


def from_commons(sid, kind, titles, queries, used):
    cands = []
    if titles:
        try:
            cands += commons_info(titles=titles, kind=kind)
        except Exception as e:
            print("   ! Commons:", e)
    for q in queries:
        try:
            cands += commons_info(search=q, kind=kind)
        except Exception as e:
            print("   ! Commons:", e)
    for title, info in cands:
        if title in used:
            continue
        src_page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
        m = meta(info, title, src_page)
        if not free_license(m):
            continue
        if kind == "img":
            url = info.get("thumburl") or info["url"]
            ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower() or ".jpg"
            if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                ext = ".jpg"
        else:
            url = pick_video_url(info)
            if not url:
                continue
            ext = ".mp4" if "mp4" in url else ".webm"
        return title, url, ext, m
    return None


def from_archive(sid, query, used):
    q = f'({query}) AND mediatype:movies AND (licenseurl:*publicdomain* OR licenseurl:*creativecommons*)'
    try:
        res = get_json("https://archive.org/advancedsearch.php",
                       {"q": q, "fl[]": ["identifier", "title", "licenseurl", "creator"],
                        "rows": 8, "output": "json"})
    except Exception as e:
        print("   ! Archive:", e); return None
    for doc in res.get("response", {}).get("docs", []):
        ident = doc["identifier"]
        if ident in used:
            continue
        try:
            md = get_json(f"https://archive.org/metadata/{ident}")
        except Exception:
            continue
        files = [f for f in md.get("files", []) if f.get("name", "").lower().endswith((".mp4", ".webm"))]
        files = [f for f in files if int(f.get("size", 0) or 0) < MAX_VIDEO_MB * 1e6] or files
        if not files:
            continue
        files.sort(key=lambda f: int(f.get("size", 0) or 0))
        f = files[0]
        url = f"https://archive.org/download/{ident}/{urllib.parse.quote(f['name'])}"
        m = {"title": doc.get("title", ident), "author": (doc.get("creator") or "Internet Archive") if isinstance(doc.get("creator"), str) else "Internet Archive",
             "license": doc.get("licenseurl", "domena publiczna"), "source": f"https://archive.org/details/{ident}"}
        return ident, url, os.path.splitext(f["name"])[1].lower(), m
    return None


def trim(path):
    if not shutil.which("ffmpeg"):
        return
    tmp = path + ".trim" + os.path.splitext(path)[1]
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-t", str(CLIP_SECONDS), "-c", "copy", tmp])
    if r.returncode == 0 and os.path.getsize(tmp) > 0:
        os.replace(tmp, path)
    elif os.path.exists(tmp):
        os.remove(tmp)


def commons_names():
    """Zweryfikowane nazwy plików z media/commons.js – sprawdzane jako pierwsze."""
    path = os.path.join(OUT, "commons.js")
    out = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            m = re.match(r'\s*(\w+):\s*\{f:(\[.*?\])', line)
            if m:
                out[m.group(1)] = ("img", ["File:" + n for n in json.loads(m.group(2))])
                continue
            m = re.match(r'\s*(\w+):\s*\{f:"([^"]+)"', line)
            if m:
                out[m.group(1)] = ("video", ["File:" + m.group(2)])
    return out


def main():
    force = "--force" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    js_path = os.path.join(OUT, "media.js")
    db = {}
    if os.path.exists(js_path) and not force:
        txt = open(js_path, encoding="utf-8").read()
        m = re.search(r"window\.MEDIA\s*=\s*(\{.*\});?\s*$", txt, re.S)
        if m:
            db = json.loads(m.group(1))
    used = {v.get("_key") for v in db.values()}
    extra = commons_names()
    slots = dict(SLOTS)
    for sid, (kind, names) in extra.items():
        slots.setdefault(sid, (kind, [], []))
    for sid, (kind, titles, queries) in slots.items():
        first = extra.get(sid, (kind, []))[1]
        titles = first + [x for x in titles if x not in first]
        if sid in db and os.path.exists(os.path.join(OUT, db[sid]["file"])):
            print(f"✓ {sid} (już jest)"); continue
        print(f"→ {sid}")
        hit = from_commons(sid, kind, titles, queries, used)
        if not hit and kind == "video" and sid in IA_QUERIES:
            hit = from_archive(sid, IA_QUERIES[sid], used)
        if not hit:
            print("   – nie znaleziono, zostaje placeholder"); continue
        key, url, ext, m = hit
        fname = sid + ext
        try:
            download(url, os.path.join(OUT, fname))
        except Exception as e:
            print("   ! pobieranie nieudane:", e); continue
        if kind == "video":
            trim(os.path.join(OUT, fname))
        m.update(file=fname, _key=key)
        db[sid] = m; used.add(key)
        print(f"   ✓ {m['title'][:70]}  [{m['license']}]")
        with open(js_path, "w", encoding="utf-8") as f:
            f.write("window.MEDIA = " + json.dumps(db, ensure_ascii=False, indent=1) + ";\n")
    print(f"\nGotowe: {len(db)}/{len(slots)} materiałów w {OUT}")


if __name__ == "__main__":
    main()
