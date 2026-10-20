from pathlib import Path
from urllib.parse import quote
import json
import re


ROOT = Path(__file__).parent
LASTMOD = "2026-10-20"
ASSET_VERSION = "20261020-3"
SOCIAL_IMAGE = "https://eduline.kr/og-image.png"
PHONE = "010-2928-3614"

DISTRICTS = [
    ("jung-gu", "중구", ["연안동", "신포동", "신흥동", "도원동", "율목동", "동인천동", "개항동", "영종동", "영종1동", "영종2동", "운서1동", "운서2동", "용유동"]),
    ("dong-gu", "동구", ["만석동", "화수1·화평동", "화수2동", "송현1·2동", "송현3동", "송림1동", "송림2동", "송림3·5동", "송림4동", "송림6동", "금창동"]),
    ("michuhol-gu", "미추홀구", ["숭의1·3동", "숭의2동", "숭의4동", "용현1·4동", "용현2동", "용현3동", "용현5동", "학익1동", "학익2동", "도화1동", "도화2·3동", "주안1동", "주안2동", "주안3동", "주안4동", "주안5동", "주안6동", "주안7동", "주안8동", "관교동", "문학동"]),
    ("yeonsu-gu", "연수구", ["옥련1동", "옥련2동", "선학동", "연수1동", "연수2동", "연수3동", "청학동", "동춘1동", "동춘2동", "동춘3동", "송도1동", "송도2동", "송도3동", "송도4동", "송도5동"]),
    ("namdong-gu", "남동구", ["구월1동", "구월2동", "구월3동", "구월4동", "간석1동", "간석2동", "간석3동", "간석4동", "만수1동", "만수2동", "만수3동", "만수4동", "만수5동", "만수6동", "장수서창동", "서창2동", "남촌도림동", "논현1동", "논현2동", "논현고잔동"]),
    ("bupyeong-gu", "부평구", ["부평1동", "부평2동", "부평3동", "부평4동", "부평5동", "부평6동", "산곡1동", "산곡2동", "산곡3동", "산곡4동", "청천1동", "청천2동", "갈산1동", "갈산2동", "삼산1동", "삼산2동", "부개1동", "부개2동", "부개3동", "일신동", "십정1동", "십정2동"]),
    ("gyeyang-gu", "계양구", ["효성1동", "효성2동", "계산1동", "계산2동", "계산3동", "계산4동", "작전1동", "작전2동", "작전서운동", "계양1동", "계양2동", "계양3동"]),
    ("seo-gu", "서구", ["검암경서동", "연희동", "청라1동", "청라2동", "청라3동", "가정1동", "가정2동", "가정3동", "신현원창동", "석남1동", "석남2동", "석남3동", "가좌1동", "가좌2동", "가좌3동", "가좌4동", "검단동", "불로대곡동", "원당동", "당하동", "오류왕길동", "마전동", "아라1동", "아라2동"]),
    ("ganghwa-gun", "강화군", ["강화읍", "선원면", "불은면", "길상면", "화도면", "양도면", "내가면", "하점면", "양사면", "송해면", "교동면", "삼산면", "서도면"]),
    ("ongjin-gun", "옹진군", ["북도면", "연평면", "백령면", "대청면", "덕적면", "자월면", "영흥면"]),
]

GUIDE_LEADS = [
    "같은 수학과외라도 학년과 목표에 따라 필요한 수학수업은 달라집니다. 초등 기초수학부터 중등 수학내신, 고등 수능대비까지 단계별로 연결합니다.",
    "현재 학년에서 꼭 잡아야 할 개념과 다음 과정의 준비를 함께 봅니다. 초등 수학공부 습관부터 고등 수능수학까지 학생별로 설계합니다.",
    "학교 진도와 시험 일정, 학생의 목표를 확인한 뒤 수업을 시작합니다. 기초수학 보완과 수학내신, 수능대비를 한 흐름으로 이어갑니다.",
]


def encoded(value):
    return quote(value, safe="")


def grade_guide(area, variant=0, section_id="curriculum"):
    cards = [
        ("초등", f"{area} 초등 수학", f"{area} 초3 · 초4 · 초5 · 초6 수학과외",
         f"{area} 초등 수학수업은 연산 정확도와 교과 개념을 다지는 기초수학에서 시작합니다. 문장제와 서술형 풀이를 함께 연습해 혼자서도 이어지는 수학공부 습관을 만들고 중학교 수학을 준비합니다.",
         ["초등 기초수학 · 연산 정확도", "초등 수학공부 습관 만들기", "예비중1 수학 준비"]),
        ("중등", f"{area} 중등 수학", f"{area} 중1 · 중2 · 중3 수학과외",
         f"{area} 중등 수학수업은 학교 진도와 시험 범위에 맞춘 수학내신 대비가 중심입니다. 개념이 흔들리는 학생은 중등 기초수학부터 다시 정리하고, 기출과 서술형 연습으로 수학공부의 방향을 잡습니다.",
         ["중등 수학내신 · 서술형 대비", "중등 기초수학 취약 단원 보완", "예비고1 공통수학 연결"]),
        ("고등", f"{area} 고등 수학", f"{area} 고1 · 고2 · 고3 수학과외",
         f"{area} 고등 수학수업은 학교별 수학내신과 수능대비를 목표에 맞춰 설계합니다. 고등 기초수학이 부족하면 개념부터 다시 세우고, 수능수학은 기출 분석과 실전 풀이로 시간 관리까지 준비합니다.",
         ["고등 수학내신 · 학교별 기출", "수능대비 · 수능수학 실전", "고등 기초수학 재정비"]),
    ]
    articles = "".join(
        f'<article class="value reveal"><strong>{label}</strong><h3>{title}</h3><p class="grade-tags">{tags}</p><p>{body}</p>'
        f'<ul class="grade-points">{"".join(f"<li>{point}</li>" for point in points)}</ul></article>'
        for label, title, tags, body, points in cards
    )
    return (
        f'<section class="areas section grade-guide" id="{section_id}"><div class="areas-heading reveal"><div><p class="kicker">MATH BY GRADE</p>'
        f'<h2>{area} 초등·중등·고등<br>수학과외 안내</h2></div><p>{GUIDE_LEADS[variant % len(GUIDE_LEADS)]}</p></div>'
        f'<div class="values">{articles}</div></section>'
    )


def faq_items(area):
    return [
        (f"{area} 수학과외는 어떤 학년이 받을 수 있나요?",
         "초등학생부터 고등학교 3학년까지 1:1로 진행합니다. 초등 기초수학, 중등 수학내신, 고등 수능대비까지 학년과 목표에 맞춰 수학수업을 구성합니다."),
        ("수학 기초가 많이 부족해도 시작할 수 있나요?",
         "가능합니다. 첫 상담에서 현재 실력을 진단하고 막힌 단원부터 기초수학을 다시 정리합니다. 학교 진도와 병행해 내신 공백이 생기지 않도록 합니다."),
        ("중등·고등 수학내신 대비는 어떻게 진행하나요?",
         "학교 진도와 시험 범위, 기출 유형을 확인한 뒤 개념 정리, 유형 연습, 서술형과 실전 점검 순서로 준비합니다."),
        ("고3 수능수학 대비도 가능한가요?",
         "가능합니다. 목표 등급에 맞춰 개념 보완, 기출 분석, 실전 모의 풀이와 시간 배분 연습으로 수능대비를 진행합니다."),
        (f"{area} 수학과외 상담은 어떻게 신청하나요?",
         f"{PHONE}로 전화 주시면 {area} 수업 가능 일정과 학생에게 맞는 수업 방향을 안내해 드립니다."),
    ]


def faq_section(area):
    items = "".join(f"<details><summary>{question}</summary><p>{answer}</p></details>" for question, answer in faq_items(area))
    return (
        '<section class="faq section" id="faq"><div class="section-heading reveal"><p class="kicker">FAQ</p>'
        f'<h2>{area} 수학과외<br>자주 묻는 질문</h2></div><div class="faq-list reveal">{items}</div></section>'
    )


def faq_schema(area):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in faq_items(area)
        ],
    }


def breadcrumb_schema(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": position, "name": name, "item": url}
            for position, (name, url) in enumerate(items, start=1)
        ],
    }


def json_ld(graph):
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def set_schema(html, schema):
    tag = f'<script type="application/ld+json">{schema}</script>'
    return re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: tag, html, count=1, flags=re.S)


def set_seo_block(html, block):
    block = f"<!-- SEO_GUIDE_START -->{block}<!-- SEO_GUIDE_END -->"
    if "<!-- SEO_GUIDE_START -->" in html:
        return re.sub(r"<!-- SEO_GUIDE_START -->.*?<!-- SEO_GUIDE_END -->", lambda _: block, html, flags=re.S)
    return html.replace('<section class="steps section"', block + '\n<section class="steps section"', 1)


def set_meta(html, title, description):
    html = re.sub(r"<title>.*?</title>", lambda _: f"<title>{title}</title>", html, count=1)
    html = re.sub(r'<meta name="description" content="[^"]*">', lambda _: f'<meta name="description" content="{description}">', html, count=1)
    html = re.sub(r'<meta property="og:title" content="[^"]*">', lambda _: f'<meta property="og:title" content="{title}">', html, count=1)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', lambda _: f'<meta property="og:description" content="{description}">', html, count=1)
    return html


def render_page(slug, district, locality, index, localities):
    canonical = f"https://eduline.kr/{slug}/{encoded(locality)}/"
    district_url = f"https://eduline.kr/{slug}/"
    rural = locality.endswith(("읍", "면"))
    area_copy = (
        f"{locality}의 이동 여건과 학교 일정, 학생의 학습 목표를 함께 확인해 가능한 수업 일정과 방식을 안내합니다."
        if rural else
        f"{locality} 학생의 학교 진도와 최근 시험, 풀이 습관을 확인해 복습·현행·선행의 균형을 정합니다."
    )
    action_copy = "수업 가능 지역 상담" if rural else "무료 학습 상담"
    area_label = f"{locality} 지역별 상담" if rural else f"{locality} 맞춤 수업"
    number = str(index + 1).zfill(2)
    title = f"인천 {locality} 수학과외 | 초등·중등·고등 수학 내신·수능대비"
    description = f"인천 {district} {locality} 수학과외 - 초등 기초수학, 중등 수학내신, 고등 수능대비·수능수학까지 학년별 1:1 맞춤 수학수업. 무료 학습 상담 {PHONE}"
    schema = json_ld([
        {
            "@type": "Service", "name": f"인천 {locality} 수학과외", "url": canonical,
            "serviceType": "1:1 수학과외", "telephone": "+82-10-2928-3614", "areaServed": f"인천광역시 {district} {locality}",
            "description": f"인천 {district} {locality} 초등·중등·고등 1:1 수학과외. 기초수학, 수학내신, 수능대비 수학수업.",
            "provider": {"@type": "EducationalOrganization", "name": "인천 수학과외 EDULINE", "url": "https://eduline.kr/"},
        },
        breadcrumb_schema([("인천 수학과외", "https://eduline.kr/"), (f"{district} 수학과외", district_url), (f"{locality} 수학과외", canonical)]),
        faq_schema(locality),
    ])
    nearby = "".join(f'<a href="../{encoded(name)}/">{name} 수학과외</a>' for name in localities if name != locality)
    nearby_section = (
        '<section class="locality-directory section" aria-labelledby="nearby-title"><div class="areas-heading reveal"><div><p class="kicker">NEARBY AREA</p>'
        f'<h2 id="nearby-title">{district} 다른 지역<br>수학과외 안내</h2></div><p>가까운 지역의 초등·중등·고등 수학과외 안내도 확인해 보세요.</p></div>'
        f'<div class="locality-grid nearby-grid">{nearby}</div></section>'
    )
    return f'''<!doctype html><html lang="ko"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description" content="{description}"><meta name="theme-color" content="#14362f"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SOCIAL_IMAGE}"><meta property="og:image:secure_url" content="{SOCIAL_IMAGE}"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="인천 수학과외 - 배운 만큼 풀리는 1:1 수업"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SOCIAL_IMAGE}"><meta name="twitter:image:alt" content="인천 수학과외 - 배운 만큼 풀리는 1:1 수업"><link rel="canonical" href="{canonical}"><link rel="icon" href="../../favicon.svg" type="image/svg+xml"><title>{title}</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="../../styles.css?v={ASSET_VERSION}"><script type="application/ld+json">{schema}</script></head><body>
<header class="site-header" id="top"><a class="brand" href="../../" aria-label="인천 수학과외 홈"><span class="brand-symbol" aria-hidden="true">∫</span><span>{locality} 수학과외<small>EDULINE</small></span></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="메뉴 열기"><span></span><span></span><span></span></button><nav class="primary-nav" id="primary-nav" aria-label="주요 메뉴"><a href="#approach">수업 안내</a><a href="#curriculum">학년별 수업</a><a href="#faq">자주 묻는 질문</a><a href="../">{district} 지역</a><a class="nav-contact" href="#contact">상담 신청</a></nav></header>
<main><section class="hero" aria-labelledby="hero-title"><div class="hero-image" role="img" aria-label="선생님과 함께 수학 문제를 공부하는 학생"></div><div class="hero-overlay"></div><div class="hero-content"><p class="kicker light">{slug.upper()} {number} MATH TUTORING</p><h1 id="hero-title">인천 {locality} 수학과외,<br><em>학생에게 맞는 1:1 수업</em></h1><p class="hero-text">{area_copy}<br class="desktop-only"> 이해한 내용을 스스로 풀어낼 때까지 꼼꼼하게 이어갑니다.</p><div class="hero-actions"><a class="button button-coral" href="#contact">{action_copy} <span aria-hidden="true">↗</span></a><a class="phone" href="tel:01029283614"><small>전화 상담</small><strong>010-2928-3614</strong></a></div></div><div class="hero-note" aria-hidden="true"><span>{number}</span><i></i><span>{area_label}</span></div></section>
<section class="intro section" id="approach"><div class="section-heading reveal"><p class="kicker">PERSONAL MATH LESSON</p><h2>현재 실력에서<br>필요한 공부부터</h2></div><div class="intro-copy reveal"><p class="lead">정해진 진도보다<br><strong>학생의 이해를 먼저 봅니다.</strong></p><p>{area_copy} 개념 이해도와 계산 정확도, 문제 해석 과정을 살핀 뒤 학생이 소화할 수 있는 순서로 수업합니다.</p></div><div class="values"><article class="value reveal"><span>01</span><strong>진단</strong><h3>개념 빈틈 확인</h3><p>최근 시험과 오답에서 막히는 지점을 찾습니다.</p></article><article class="value reveal"><span>02</span><strong>설계</strong><h3>개인별 진도 구성</h3><p>학교 일정과 목표에 맞춰 학습 순서를 정합니다.</p></article><article class="value reveal"><span>03</span><strong>관리</strong><h3>복습과 오답 점검</h3><p>배운 내용을 혼자서도 풀 수 있게 관리합니다.</p></article></div></section>
{grade_guide(locality, index)}
<section class="steps section"><div class="steps-heading reveal"><p class="kicker light">HOW WE BEGIN</p><h2>충분히 살펴보고<br>맞는 수업을 시작합니다</h2></div><ol class="step-list"><li class="reveal"><span>01</span><strong>학습 상담</strong><p>지역과 목표 확인</p></li><li class="reveal"><span>02</span><strong>실력 진단</strong><p>개념과 습관 점검</p></li><li class="reveal"><span>03</span><strong>학습 설계</strong><p>개인별 계획 제안</p></li><li class="reveal"><span>04</span><strong>수업 관리</strong><p>복습과 오답 확인</p></li></ol></section>
{faq_section(locality)}
{nearby_section}
<section class="contact" id="contact"><div class="contact-copy reveal"><p class="kicker">START YOUR WAY</p><h2>{locality} 수학과외<br>상담 신청</h2><p>전화 주시면 학생의 학년과 목표에 맞춰 상담을 도와드립니다.</p><a href="tel:01029283614"><small>전화 상담</small>010-2928-3614</a></div></section></main>
<footer class="site-footer"><a class="brand" href="../../"><span class="brand-symbol" aria-hidden="true">∫</span><span>인천 수학과외<small>EDULINE</small></span></a><div><p>{district} {locality} 초·중·고 1:1 수학과외</p><p>상담 문의 <a href="tel:01029283614">010-2928-3614</a></p></div><p>© <span id="year"></span> EDULINE. ALL RIGHTS RESERVED.</p></footer><a class="floating-contact" href="#contact" aria-label="상담 신청"><span>상담</span><span aria-hidden="true">↗</span></a><script src="../../script.js?v={ASSET_VERSION}"></script></body></html>'''


def update_parent(slug, district, localities):
    file_path = ROOT / slug / "index.html"
    canonical = f"https://eduline.kr/{slug}/"
    html = file_path.read_text(encoding="utf-8")
    html = re.sub(r'href="\.\./styles\.css(?:\?v=[^"]+)?"', f'href="../styles.css?v={ASSET_VERSION}"', html)
    html = re.sub(r'src="\.\./script\.js(?:\?v=[^"]+)?"', f'src="../script.js?v={ASSET_VERSION}"', html)
    if 'property="og:image"' not in html:
        social_meta = (
            f'<meta property="og:image" content="{SOCIAL_IMAGE}">'
            f'<meta property="og:image:secure_url" content="{SOCIAL_IMAGE}">'
            '<meta property="og:image:type" content="image/png">'
            '<meta property="og:image:width" content="1200">'
            '<meta property="og:image:height" content="630">'
            '<meta property="og:image:alt" content="인천 수학과외 - 배운 만큼 풀리는 1:1 수업">'
            '<meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:image" content="{SOCIAL_IMAGE}">'
            '<meta name="twitter:image:alt" content="인천 수학과외 - 배운 만큼 풀리는 1:1 수업">'
        )
        html = html.replace('<link rel="canonical"', social_meta + '<link rel="canonical"', 1)
    html = set_meta(
        html,
        f"인천 {district} 수학과외 | 초등·중등·고등 수학 내신·수능대비",
        f"인천 {district} 수학과외 - {'·'.join(localities[:3])} 등 {district} 전 지역 초등 기초수학, 중등 수학내신, 고등 수능대비·수능수학 1:1 맞춤 수학수업. 무료 학습 상담 {PHONE}",
    )
    html = set_schema(html, json_ld([
        {
            "@type": "Service", "name": f"인천 {district} 수학과외", "url": canonical, "serviceType": "1:1 수학과외",
            "telephone": "+82-10-2928-3614", "areaServed": f"인천광역시 {district}",
            "provider": {"@type": "EducationalOrganization", "name": "인천 수학과외 EDULINE", "url": "https://eduline.kr/"},
        },
        breadcrumb_schema([("인천 수학과외", "https://eduline.kr/"), (f"{district} 수학과외", canonical)]),
        faq_schema(district),
    ]))
    html = set_seo_block(html, grade_guide(district, 0, "grade-guide") + faq_section(district))
    links = "".join(f'<a href="{encoded(locality)}/">{locality} 수학과외</a>' for locality in localities)
    section = (
        '<!-- LOCALITY_LINKS_START --><section class="locality-directory section" aria-labelledby="locality-title">'
        f'<div class="areas-heading"><div><p class="kicker">LOCAL AREA GUIDE</p><h2 id="locality-title">{district} 동·읍·면별<br>수학과외 안내</h2></div>'
        '<p>거주 지역을 선택하면 해당 지역의 초등·중등·고등 1:1 수학과외 안내를 확인할 수 있습니다.</p></div>'
        f'<div class="locality-grid">{links}</div></section><!-- LOCALITY_LINKS_END -->'
    )
    if "<!-- LOCALITY_LINKS_START -->" in html:
        html = re.sub(r"<!-- LOCALITY_LINKS_START -->.*?<!-- LOCALITY_LINKS_END -->", lambda _: section, html, flags=re.S)
    else:
        html = html.replace('<section class="contact" id="contact">', section + '\n<section class="contact" id="contact">')
    file_path.write_text(html, encoding="utf-8")


def update_home():
    file_path = ROOT / "index.html"
    html = file_path.read_text(encoding="utf-8")
    html = set_meta(
        html,
        "인천 수학과외 | 초등·중등·고등 1:1 수학 내신·수능대비 EDULINE",
        f"인천 수학과외 EDULINE - 연수구·남동구·부평구·서구 등 인천 전 지역 초등 기초수학, 중등 수학내신, 고등 수능대비·수능수학까지 학년별 1:1 맞춤 수학수업. 무료 학습 상담 {PHONE}",
    )
    html = re.sub(r'href="styles\.css(?:\?v=[^"]+)?"', f'href="styles.css?v={ASSET_VERSION}"', html)
    html = re.sub(r'src="script\.js(?:\?v=[^"]+)?"', f'src="script.js?v={ASSET_VERSION}"', html)
    if 'type="application/rss+xml"' not in html:
        html = html.replace('<link rel="icon"', '<link rel="alternate" type="application/rss+xml" title="인천 수학과외 EDULINE" href="https://eduline.kr/rss.xml">\n  <link rel="icon"', 1)
    html = set_schema(html, json_ld([
        {
            "@type": "EducationalOrganization", "name": "인천 수학과외 EDULINE", "alternateName": "인천 수학과외", "url": "https://eduline.kr/",
            "telephone": "+82-10-2928-3614", "areaServed": "인천광역시", "image": SOCIAL_IMAGE,
            "description": "인천 초등·중등·고등 학생을 위한 1:1 맞춤 수학과외. 기초수학, 수학내신, 수능대비 수학수업.",
        },
        {"@type": "WebSite", "name": "인천 수학과외 EDULINE", "url": "https://eduline.kr/", "inLanguage": "ko-KR"},
        faq_schema("인천"),
    ]))
    html = set_seo_block(html, grade_guide("인천", 0, "grade-guide") + faq_section("인천"))
    file_path.write_text(html, encoding="utf-8")


def build_sitemap():
    urls = [
        f"  <url><loc>https://eduline.kr/{slug}/</loc><lastmod>{LASTMOD}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        for slug, _, _ in DISTRICTS
    ]
    urls.extend(
        f"  <url><loc>https://eduline.kr/{slug}/{encoded(locality)}/</loc><lastmod>{LASTMOD}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>"
        for slug, _, localities in DISTRICTS for locality in localities
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://eduline.kr/</loc><lastmod>{LASTMOD}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
{chr(10).join(urls)}
</urlset>
'''


def build_rss():
    items = [("인천 수학과외 | 초등·중등·고등 1:1 수학 내신·수능대비", "https://eduline.kr/", "인천 전 지역 초등 기초수학, 중등 수학내신, 고등 수능대비 1:1 수학과외")]
    items.extend(
        (f"인천 {district} 수학과외", f"https://eduline.kr/{slug}/", f"인천 {district} 초등·중등·고등 1:1 수학과외 안내")
        for slug, district, _ in DISTRICTS
    )
    items.extend(
        (f"인천 {locality} 수학과외", f"https://eduline.kr/{slug}/{encoded(locality)}/", f"인천 {district} {locality} 초등 기초수학, 중등 수학내신, 고등 수능대비 수학수업 안내")
        for slug, district, localities in DISTRICTS for locality in localities
    )
    pub_date = "Tue, 20 Oct 2026 09:00:00 +0900"
    body = "\n".join(
        f"    <item><title>{title}</title><link>{link}</link><guid>{link}</guid><description>{text}</description><pubDate>{pub_date}</pubDate></item>"
        for title, link, text in items
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>인천 수학과외 EDULINE</title>
    <link>https://eduline.kr/</link>
    <description>인천 초등·중등·고등 1:1 맞춤 수학과외 지역별 안내</description>
    <language>ko</language>
    <lastBuildDate>{pub_date}</lastBuildDate>
{body}
  </channel>
</rss>
'''


page_count = 0
for district_slug, district_name, locality_names in DISTRICTS:
    update_parent(district_slug, district_name, locality_names)
    for locality_index, locality_name in enumerate(locality_names):
        directory = ROOT / district_slug / locality_name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(
            render_page(district_slug, district_name, locality_name, locality_index, locality_names), encoding="utf-8"
        )
        page_count += 1

update_home()
(ROOT / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8")
(ROOT / "rss.xml").write_text(build_rss(), encoding="utf-8")
print(f"Generated {page_count} locality pages across {len(DISTRICTS)} districts.")
