from pathlib import Path
from html import escape as html_escape
from urllib.parse import quote
import json
import re


ROOT = Path(__file__).parent
LASTMOD = "2026-10-24"
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


def cards_section(section_id, kicker, heading, lead, cards):
    articles = "".join(
        f'<article class="value reveal"><strong>{label}</strong><h3>{title}</h3><p class="grade-tags">{tags}</p><p>{body}</p>'
        f'<ul class="grade-points">{"".join(f"<li>{point}</li>" for point in points)}</ul></article>'
        for label, title, tags, body, points in cards
    )
    return (
        f'<section class="areas section grade-guide" id="{section_id}"><div class="areas-heading reveal"><div><p class="kicker">{kicker}</p>'
        f'<h2>{heading}</h2></div><p>{lead}</p></div><div class="values">{articles}</div></section>'
    )


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
    return cards_section(section_id, "MATH BY GRADE", f"{area} 초등·중등·고등<br>수학과외 안내", GUIDE_LEADS[variant % len(GUIDE_LEADS)], cards)


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


def faq_section(area, items=None):
    items = "".join(f"<details><summary>{question}</summary><p>{answer}</p></details>" for question, answer in (items or faq_items(area)))
    return (
        '<section class="faq section" id="faq"><div class="section-heading reveal"><p class="kicker">FAQ</p>'
        f'<h2>{area} 수학과외<br>자주 묻는 질문</h2></div><div class="faq-list reveal">{items}</div></section>'
    )


def faq_schema(area, items=None):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in (items or faq_items(area))
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
{locality_school_section(slug, district, locality)}
<section class="steps section"><div class="steps-heading reveal"><p class="kicker light">HOW WE BEGIN</p><h2>충분히 살펴보고<br>맞는 수업을 시작합니다</h2></div><ol class="step-list"><li class="reveal"><span>01</span><strong>학습 상담</strong><p>지역과 목표 확인</p></li><li class="reveal"><span>02</span><strong>실력 진단</strong><p>개념과 습관 점검</p></li><li class="reveal"><span>03</span><strong>학습 설계</strong><p>개인별 계획 제안</p></li><li class="reveal"><span>04</span><strong>수업 관리</strong><p>복습과 오답 확인</p></li></ol></section>
{faq_section(locality)}
{nearby_section}
<section class="contact" id="contact"><div class="contact-copy reveal"><p class="kicker">START YOUR WAY</p><h2>{locality} 수학과외<br>상담 신청</h2><p>전화 주시면 학생의 학년과 목표에 맞춰 상담을 도와드립니다.</p><a href="tel:01029283614"><small>전화 상담</small>010-2928-3614</a></div></section></main>
<footer class="site-footer"><a class="brand" href="../../"><span class="brand-symbol" aria-hidden="true">∫</span><span>인천 수학과외<small>EDULINE</small></span></a><div><p>{district} {locality} 초·중·고 1:1 수학과외</p><p>상담 문의 <a href="tel:01029283614">010-2928-3614</a></p></div><p>© <span id="year"></span> EDULINE. ALL RIGHTS RESERVED.</p></footer><a class="floating-contact" href="#contact" aria-label="상담 신청"><span>상담</span><span aria-hidden="true">↗</span></a><script src="../../script.js?v={ASSET_VERSION}"></script></body></html>'''


SCHOOL_DATA = json.loads((ROOT / "data" / "incheon_schools.json").read_text(encoding="utf-8"))
SCHOOLS = SCHOOL_DATA["schools"]
SCHOOL_TYPES = ["초등학교", "중학교", "고등학교"]
SCHOOL_DISTRICTS = ["제물포구", "영종구", "미추홀구", "연수구", "남동구", "부평구", "계양구", "서해구", "검단구", "강화군", "옹진군"]
JEMULPO_DONG_GU = {"만석동", "화수동", "화평동", "송현동", "송림동", "창영동", "금곡동"}
GEOMDAN_LOCALITIES = {"검단동", "불로대곡동", "원당동", "당하동", "오류왕길동", "마전동", "아라1동", "아라2동"}
EXTRA_LEGAL_DONGS = {"금창동": ["창영동", "금곡동"], "개항동": ["북성동", "송학동", "항동"]}


def school_district(slug, locality=None):
    if slug == "jung-gu":
        if locality is None:
            return ["제물포구", "영종구"]
        return ["영종구"] if locality.startswith(("영종", "운서", "용유")) else ["제물포구"]
    if slug == "dong-gu":
        return ["제물포구"]
    if slug == "seo-gu":
        if locality is None:
            return ["서해구", "검단구"]
        return ["검단구"] if locality in GEOMDAN_LOCALITIES else ["서해구"]
    return [dict((s, d) for s, d, _ in DISTRICTS)[slug]]


def legal_base(dong):
    return re.sub(r"\d", "", re.sub(r"(동\d*가|동)$", "", dong))


def locality_bases(locality):
    if locality.endswith(("읍", "면")):
        return {locality}
    bases = set()
    for part in re.sub(r"동$", "", locality).split("·"):
        part = re.sub(r"\d", "", part)
        if len(part) == 4:
            bases.update({part[:2], part[2:]})
        elif part:
            bases.add(part)
    for extra in EXTRA_LEGAL_DONGS.get(locality, []):
        bases.add(legal_base(extra))
    return bases


def schools_in(districts, legal_dongs=None):
    return [
        school for school in SCHOOLS
        if school["district"] in districts and (legal_dongs is None or legal_base(school["dong"]) in legal_dongs or school["dong"] in legal_dongs)
    ]


def slug_schools(slug, locality=None):
    districts = school_district(slug, locality)
    if locality is None:
        schools = schools_in(districts)
        if slug == "dong-gu":
            return [school for school in schools if school["dong"] in JEMULPO_DONG_GU]
        if slug == "jung-gu":
            return [school for school in schools if school["dong"] not in JEMULPO_DONG_GU]
        return schools
    return schools_in(districts, locality_bases(locality))


def school_chips(schools):
    return "".join(f"<li>{html_escape(school['name'])}</li>" for school in schools)


def school_columns(schools):
    groups = []
    for school_type in SCHOOL_TYPES:
        items = [school for school in schools if school["type"] == school_type]
        if items:
            groups.append(f'<div class="school-group"><h3>{school_type} <small>{len(items)}곳</small></h3><ul>{school_chips(items)}</ul></div>')
    return f'<div class="school-groups">{"".join(groups)}</div>'


def school_section(heading, lead, body):
    return (
        '<section class="schools section" id="schools"><div class="areas-heading reveal"><div><p class="kicker">LOCAL SCHOOLS</p>'
        f'<h2>{heading}</h2></div><p>{lead}</p></div>{body}'
        f'<p class="school-source">학교 정보: {SCHOOL_DATA["source"]} 기준. 각 학교와 제휴 관계는 없으며, 학교별 진도와 시험 범위에 맞춘 수업을 안내합니다.</p></section>'
    )


def school_lead(area, schools):
    names = [school["name"] for school_type in ["중학교", "고등학교", "초등학교"] for school in schools if school["type"] == school_type][:3]
    example = f"{', '.join(names)} 등 " if names else ""
    return f"{example}{area} 학생의 학교별 진도와 시험 범위, 기출 유형을 확인해 초등 수학공부부터 중등·고등 수학내신, 수능대비까지 준비합니다."


def area_school_section(area, schools):
    return school_section(f"{area} 학교별<br>수학 내신 대비", html_escape(school_lead(area, schools)), school_columns(schools))


def locality_school_section(slug, district, locality):
    schools = slug_schools(slug, locality)
    if schools:
        return area_school_section(f"{locality} 인근", schools)
    districts = school_district(slug, locality)
    return area_school_section(f"{'·'.join(districts)}", schools_in(districts))


def grouped_school_section(heading, lead, school_types):
    blocks = []
    for district in SCHOOL_DISTRICTS:
        items = [school for school in SCHOOLS if school["district"] == district and school["type"] in school_types]
        if not items:
            continue
        inner = school_columns(items) if len(school_types) > 1 else f'<ul class="school-chips">{school_chips(items)}</ul>'
        blocks.append(f'<details class="school-district"><summary>인천 {district} <small>{len(items)}곳</small></summary>{inner}</details>')
    return school_section(heading, lead, f'<div class="school-district-list">{"".join(blocks)}</div>')


def locality_links(slug, names):
    return [(f"{name} 수학과외", f"../{slug}/{encoded(name)}/") for name in names]


DISTRICT_LINKS = [(f"{district} 수학과외", f"../{slug}/") for slug, district, _ in DISTRICTS]

AREA_GRADE_FAQ = [
    ("수학 기초가 많이 부족해도 시작할 수 있나요?",
     "가능합니다. 첫 상담에서 현재 실력을 진단하고 막힌 단원부터 기초수학을 다시 정리합니다. 학교 진도와 병행해 내신 공백이 생기지 않도록 합니다."),
    ("고3 수능수학 대비도 가능한가요?",
     "가능합니다. 목표 등급에 맞춰 개념 보완, 기출 분석, 실전 모의 풀이와 시간 배분 연습으로 수능대비를 진행합니다."),
]

LANDING_PAGES = [
    {
        "slug": "songdo", "area": "송도", "label": "송도국제도시",
        "title": "송도 수학과외 | 송도국제도시 초등·중등·고등 1:1 수학 내신·수능대비",
        "description": f"인천 송도 수학과외 - 송도1동~송도5동 송도국제도시 초등 기초수학, 중등 수학내신, 고등 수능대비·수능수학 1:1 맞춤 수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 송도 수학과외,", "em": "송도국제도시 1:1 수학 수업",
        "hero": "송도1동부터 송도5동까지, 학생의 학교 진도와 목표에 맞춰 공부의 순서를 설계합니다.",
        "intro_h2": "송도 학생에게<br>필요한 수학 공부", "lead": "학교마다 다른 진도와 시험,<br><strong>학생별로 따로 준비합니다.</strong>",
        "body": "송도국제도시는 학교와 학생에 따라 진도와 시험 범위, 선행 정도가 크게 다릅니다. 현재 학년의 수학내신을 먼저 안정시키고, 학생이 소화할 수 있는 속도로 다음 과정을 연결합니다. 선행은 했지만 개념이 흔들리는 학생은 기초수학부터 다시 점검합니다.",
        "faq": [
            ("송도 어느 지역까지 수업이 가능한가요?", "송도1동부터 송도5동까지 송도국제도시 전 지역 상담이 가능합니다. 주소와 희망 시간을 알려주시면 가능한 일정을 안내해 드립니다."),
            ("선행을 많이 했는데 수학내신 점수가 잘 안 나와요.", "선행 진도보다 현재 학년 개념의 정확도가 내신 점수를 좌우하는 경우가 많습니다. 오답과 풀이 과정을 진단해 빈틈을 먼저 메우고, 학교 기출 유형으로 실전 감각을 맞춥니다."),
        ],
        "schools": (["연수구"], {"송도"}),
        "links_title": "송도 동별<br>수학과외 안내",
        "links": locality_links("yeonsu-gu", ["송도1동", "송도2동", "송도3동", "송도4동", "송도5동"]) + [("연수구 수학과외", "../yeonsu-gu/")],
    },
    {
        "slug": "cheongna", "area": "청라", "label": "청라국제도시",
        "title": "청라 수학과외 | 청라국제도시 초등·중등·고등 1:1 수학 내신·수능대비",
        "description": f"인천 청라 수학과외 - 청라1동~청라3동 청라국제도시 초등 기초수학, 중등 수학내신, 고등 수능대비·수능수학 1:1 맞춤 수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 청라 수학과외,", "em": "청라국제도시 1:1 수학 수업",
        "hero": "청라1동부터 청라3동까지, 학생의 현재 실력과 목표에 맞춰 수업을 설계합니다.",
        "intro_h2": "청라 학생에게<br>필요한 수학 공부", "lead": "학원 진도를 따라가기 어렵다면<br><strong>1:1로 빈틈부터 채웁니다.</strong>",
        "body": "여러 명이 함께 듣는 수업에서는 놓친 개념을 다시 짚기 어렵습니다. 청라 학생의 최근 시험지와 오답을 함께 보고 막힌 단원부터 정리한 뒤, 학교 진도와 수학내신 일정에 맞춰 수업 순서를 정합니다.",
        "faq": [
            ("청라 어느 지역까지 수업이 가능한가요?", "청라1동부터 청라3동까지 청라국제도시 전 지역과 인근 가정동·연희동 상담이 가능합니다. 주소와 희망 시간을 알려주시면 가능한 일정을 안내해 드립니다."),
            ("학원과 1:1 수학과외를 함께 해도 되나요?", "가능합니다. 학원 진도는 유지하면서 이해가 부족한 단원과 오답을 1:1 수업에서 보완하는 방식으로 진행할 수 있습니다."),
        ],
        "schools": (["서해구"], {"청라"}),
        "links_title": "청라·인근 지역<br>수학과외 안내",
        "links": locality_links("seo-gu", ["청라1동", "청라2동", "청라3동", "연희동", "가정1동", "가정2동", "가정3동"]) + [("서구 수학과외", "../seo-gu/")],
    },
    {
        "slug": "geomdan-gu", "area": "검단구", "label": "검단신도시",
        "title": "검단 수학과외 | 인천 검단구 초등·중등·고등 1:1 수학 내신·수능대비",
        "description": f"인천 검단구 수학과외 - 검단신도시·원당·당하·마전·아라동 초등 기초수학, 중등 수학내신, 고등 수능대비·수능수학 1:1 맞춤 수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 검단구 수학과외,", "em": "검단신도시 1:1 수학 수업",
        "hero": "검단신도시와 원당·당하·마전·아라동 일대 학생의 학교 진도와 목표에 맞춰 수업합니다.",
        "intro_h2": "검단 학생에게<br>필요한 수학 공부", "lead": "새 학교, 새 환경에서도<br><strong>수학은 흔들리지 않게.</strong>",
        "body": "2026년 7월 서구 검단 지역이 검단구로 새롭게 출범했습니다. 전학이나 진학으로 학교가 바뀌면 진도와 시험 유형도 달라집니다. 검단구 학생의 현재 학교 진도를 확인해 빠진 단원을 메우고, 수학내신과 다음 학년 준비를 함께 이어갑니다.",
        "faq": [
            ("검단구는 기존 서구와 어떤 관계인가요?", "2026년 7월 행정구역 개편으로 기존 서구의 검단 지역이 검단구가 되었습니다. 검단동, 불로대곡동, 원당동, 당하동, 오류왕길동, 마전동, 아라동 등 검단 지역 상담이 가능합니다."),
            ("전학 후 진도가 달라 공백이 생겼어요.", "이전 학교와 현재 학교의 진도 차이를 확인해 빠진 단원부터 정리합니다. 이후 현재 학교의 시험 범위에 맞춰 수학내신을 준비합니다."),
        ],
        "schools": (["검단구"], None),
        "links_title": "검단 동별<br>수학과외 안내",
        "links": locality_links("seo-gu", ["검단동", "불로대곡동", "원당동", "당하동", "오류왕길동", "마전동", "아라1동", "아라2동"]),
    },
    {
        "slug": "yeongjong-gu", "area": "영종구", "label": "영종도",
        "title": "영종도 수학과외 | 인천 영종구 초등·중등·고등 1:1 수학 내신·수능대비",
        "description": f"인천 영종구 수학과외 - 영종동·운서동·용유동 영종도 초등 기초수학, 중등 수학내신, 고등 수능대비·수능수학 1:1 맞춤 수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 영종구 수학과외,", "em": "영종도 1:1 수학 수업",
        "hero": "영종동·운서동·용유동 학생의 학교 일정과 이동 여건을 함께 고려해 수업을 안내합니다.",
        "intro_h2": "영종도 학생에게<br>필요한 수학 공부", "lead": "이동 시간은 줄이고<br><strong>수업 시간은 알차게.</strong>",
        "body": "2026년 7월 중구의 영종·용유 지역이 영종구로 새롭게 출범했습니다. 섬 지역 특성상 학원 선택지와 이동 시간이 수학공부에 영향을 줍니다. 영종구 학생의 학교 일정과 학습 목표를 확인해 가능한 수업 일정과 방식을 안내합니다.",
        "faq": [
            ("영종도도 수업이 가능한가요?", "영종동, 영종1·2동, 운서1·2동, 용유동 등 영종구 지역의 수업 가능 일정과 방식을 상담 시 안내해 드립니다."),
            ("영종구는 기존 중구와 어떤 관계인가요?", "2026년 7월 행정구역 개편으로 기존 중구의 영종·용유 지역이 영종구가 되었습니다."),
        ],
        "schools": (["영종구"], None),
        "links_title": "영종도 동별<br>수학과외 안내",
        "links": locality_links("jung-gu", ["영종동", "영종1동", "영종2동", "운서1동", "운서2동", "용유동"]),
    },
    {
        "slug": "jemulpo-gu", "area": "제물포구", "label": "중구·동구 원도심",
        "title": "제물포구 수학과외 | 인천 제물포구 초등·중등·고등 1:1 수학 내신·수능대비",
        "description": f"인천 제물포구 수학과외 - 신포·동인천·송림·송현·화수동 등 옛 중구·동구 지역 초등 기초수학, 중등 수학내신, 고등 수능대비 1:1 맞춤 수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 제물포구 수학과외,", "em": "원도심 1:1 수학 수업",
        "hero": "옛 중구 내륙과 동구 지역 학생의 학교 진도와 목표에 맞춰 공부의 순서를 설계합니다.",
        "intro_h2": "제물포구 학생에게<br>필요한 수학 공부", "lead": "가까운 곳에서<br><strong>꼼꼼한 1:1 수학 수업.</strong>",
        "body": "2026년 7월 중구 내륙 지역과 동구가 합쳐져 제물포구가 출범했습니다. 제물포구 학생의 최근 시험과 풀이 습관을 확인해 기초수학 보완과 수학내신 대비, 다음 학년 준비의 균형을 정합니다.",
        "faq": [
            ("제물포구는 어느 지역인가요?", "2026년 7월 행정구역 개편으로 기존 중구 내륙 지역(신포동, 동인천동, 개항동 등)과 동구(송림동, 송현동, 화수동, 만석동, 금창동 등)가 합쳐진 지역입니다. 제물포구 전 지역 상담이 가능합니다."),
        ],
        "schools": (["제물포구"], None),
        "links_title": "제물포구 동별<br>수학과외 안내",
        "links": locality_links("jung-gu", ["연안동", "신포동", "신흥동", "도원동", "율목동", "동인천동", "개항동"])
        + locality_links("dong-gu", ["만석동", "화수1·화평동", "화수2동", "송현1·2동", "송현3동", "송림1동", "송림2동", "송림3·5동", "송림4동", "송림6동", "금창동"]),
    },
    {
        "slug": "seohae-gu", "area": "서해구", "label": "서해구",
        "title": "서해구 수학과외 | 인천 서해구 초등·중등·고등 1:1 수학 내신·수능대비",
        "description": f"인천 서해구 수학과외 - 청라·검암·가정·석남·가좌·신현·연희동 초등 기초수학, 중등 수학내신, 고등 수능대비·수능수학 1:1 맞춤 수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 서해구 수학과외,", "em": "청라부터 가좌까지 1:1 수학 수업",
        "hero": "청라·검암·가정·석남·가좌·신현·연희동 학생의 학교 진도와 목표에 맞춰 수업합니다.",
        "intro_h2": "서해구 학생에게<br>필요한 수학 공부", "lead": "동네마다 다른 학교 일정,<br><strong>학생에게 맞춰 준비합니다.</strong>",
        "body": "2026년 7월 행정구역 개편으로 검단 지역을 제외한 기존 서구가 서해구가 되었습니다. 청라국제도시부터 가정·석남·가좌동 원도심까지 학교마다 진도와 시험 유형이 다르기 때문에, 서해구 학생의 현재 학교 진도를 확인해 수학내신과 다음 학년 준비를 함께 설계합니다.",
        "faq": [
            ("서해구는 기존 서구와 어떤 관계인가요?", "2026년 7월 행정구역 개편으로 검단 지역이 검단구로 분리되고, 나머지 서구 지역이 서해구가 되었습니다. 청라, 검암경서, 연희, 가정, 신현원창, 석남, 가좌동 등 서해구 전 지역 상담이 가능합니다."),
        ],
        "schools": (["서해구"], None),
        "links_title": "서해구 동별<br>수학과외 안내",
        "links": locality_links("seo-gu", ["검암경서동", "연희동", "청라1동", "청라2동", "청라3동", "가정1동", "가정2동", "가정3동", "신현원창동", "석남1동", "석남2동", "석남3동", "가좌1동", "가좌2동", "가좌3동", "가좌4동"]),
    },
    {
        "slug": "elementary-math", "area": "인천 초등", "label": "초등 수학", "school_type": "초등학교",
        "title": "인천 초등 수학과외 | 초등 기초수학·수학공부 습관 1:1 수업",
        "description": f"인천 초등 수학과외 - 초등 기초수학, 연산, 문장제·서술형, 수학공부 습관부터 예비중1 준비까지 1:1 맞춤 초등 수학수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 초등 수학과외,", "em": "기초부터 탄탄한 1:1 수업",
        "hero": "연산과 교과 개념, 풀이 과정을 꼼꼼히 다져 중학교 수학까지 이어지는 힘을 만듭니다.",
        "intro_h2": "초등 수학,<br>지금 다져야 할 것", "lead": "초등의 작은 빈틈이<br><strong>중학교에서 크게 드러납니다.</strong>",
        "body": "분수, 소수, 비와 비율처럼 중학교 수학의 바탕이 되는 단원은 초등에서 정확히 이해해야 합니다. 학생이 어디에서 막히는지 진단하고, 기초수학과 연산 정확도를 다진 뒤 스스로 풀이 과정을 설명할 수 있도록 수업합니다.",
        "cards": [
            ("초3·4", "개념과 연산 기초", "인천 초3 · 초4 수학과외", "분수와 소수, 곱셈과 나눗셈처럼 이후 학년의 바탕이 되는 단원을 정확히 이해하고 실수 없는 연산 습관을 만듭니다.", ["초등 기초수학 · 연산 정확도", "분수·소수 개념 이해", "풀이 과정 쓰는 습관"]),
            ("초5·6", "문장제와 서술형", "인천 초5 · 초6 수학과외", "약분과 통분, 비와 비율, 도형의 넓이처럼 중학교 수학과 직접 연결되는 단원을 다지고 문제를 읽고 식을 세우는 힘을 기릅니다.", ["문장제 식 세우기", "서술형 풀이 연습", "혼자 하는 수학공부 습관"]),
            ("예비중1", "중학교 수학 준비", "인천 예비중1 수학과외", "정수와 유리수, 문자와 식 등 중1 첫 단원을 미리 익혀 중학교 첫 시험에서 흔들리지 않도록 준비합니다.", ["초등 과정 빈틈 점검", "중1 수학 개념 예습", "중학교 시험 형식 익히기"]),
        ],
        "faq": [
            ("초등학생도 1:1 수학과외가 필요한가요?", "연산이나 개념이 흔들리는 학생, 문장제와 서술형을 어려워하는 학생에게 특히 도움이 됩니다. 초등 시기의 기초수학 빈틈은 중학교에서 더 크게 드러나기 때문입니다."),
            ("초등 수학공부는 하루에 얼마나 해야 하나요?", "학년과 집중력에 따라 다르지만, 길게 하는 것보다 매일 일정한 시간 꾸준히 하는 습관이 중요합니다. 수업 때 학생에게 맞는 복습 분량을 함께 정합니다."),
            ("선행보다 복습이 먼저인가요?", "현재 학년 개념이 정확하지 않으면 선행 효과가 떨어집니다. 진단 후 복습과 선행의 비율을 학생에게 맞게 정합니다."),
        ],
    },
    {
        "slug": "middle-math", "area": "인천 중등", "label": "중등 수학", "school_type": "중학교",
        "title": "인천 중등 수학과외 | 중1·중2·중3 수학내신 1:1 대비",
        "description": f"인천 중등 수학과외 - 중1·중2·중3 학교별 수학내신, 서술형, 중등 기초수학 보완부터 예비고1 공통수학까지 1:1 맞춤 수학수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 중등 수학과외,", "em": "수학내신까지 잡는 1:1 수업",
        "hero": "학교 진도와 시험 범위에 맞춰 개념, 유형, 서술형을 순서대로 준비합니다.",
        "intro_h2": "중등 수학,<br>내신과 기초를 함께", "lead": "점수가 오르지 않는 이유는<br><strong>학생마다 다릅니다.</strong>",
        "body": "개념을 몰라서, 계산 실수가 잦아서, 서술형에서 감점되어서 등 중등 수학 점수가 오르지 않는 이유는 학생마다 다릅니다. 최근 시험지와 오답을 진단해 원인을 찾고, 학교별 시험 범위와 기출 유형에 맞춰 수학내신을 준비합니다.",
        "cards": [
            ("중1", "첫 시험 적응", "인천 중1 수학과외", "정수와 유리수, 일차방정식, 좌표와 그래프를 정확히 익히고 중학교 첫 지필고사의 형식과 서술형에 적응합니다.", ["중등 기초수학 정리", "첫 지필고사 대비", "서술형 답안 쓰기"]),
            ("중2", "방정식과 함수", "인천 중2 수학과외", "연립방정식과 일차함수, 도형의 성질, 확률처럼 난도가 오르는 단원을 유형별로 정리해 수학내신 점수를 안정시킵니다.", ["중2 수학내신 대비", "함수·도형 취약 단원 보완", "학교별 기출 분석"]),
            ("중3", "고등 수학 연결", "인천 중3 수학과외", "제곱근, 인수분해, 이차방정식과 이차함수를 고등 수학과 연결해 다지고 예비고1 공통수학을 준비합니다.", ["중3 수학내신 대비", "인수분해·이차함수 집중", "예비고1 공통수학 준비"]),
        ],
        "faq": [
            ("중등 수학내신 대비는 언제부터 시작하나요?", "평소에는 학교 진도에 맞춰 개념과 유형을 정리하고, 시험 4~5주 전부터 시험 범위 중심으로 기출과 서술형을 집중 연습합니다."),
            ("중3인데 중1·중2 기초가 부족해요.", "현재 진도를 놓치지 않으면서 고등 수학에 필요한 이전 학년 단원을 함께 보완합니다. 특히 방정식과 함수는 우선순위를 두고 정리합니다."),
            ("학교마다 시험 문제가 다른데 어떻게 준비하나요?", "학생의 학교 교과서와 시험 범위, 이전 기출 유형을 확인해 출제 경향에 맞춰 준비합니다."),
        ],
    },
    {
        "slug": "high-math", "area": "인천 고등", "label": "고등 수학", "school_type": "고등학교",
        "title": "인천 고등 수학과외 | 고1·고2·고3 수학내신·수능수학 1:1 대비",
        "description": f"인천 고등 수학과외 - 고1 공통수학, 고2 선택과목 수학내신, 고3 수능대비·수능수학, 고등 기초수학 보완까지 1:1 맞춤 수학수업. 무료 학습 상담 {PHONE}",
        "h1": "인천 고등 수학과외,", "em": "내신·수능 1:1 맞춤 수업",
        "hero": "학교별 수학내신과 수능수학, 학생의 목표 등급에 맞춰 공부의 우선순위를 정합니다.",
        "intro_h2": "고등 수학,<br>목표에 맞는 전략", "lead": "내신과 수능 사이에서<br><strong>지금 할 공부를 정합니다.</strong>",
        "body": "고등 수학은 학년과 목표에 따라 집중해야 할 공부가 달라집니다. 학교 시험 범위와 선택 과목, 모의고사 결과를 함께 보고 수학내신과 수능대비의 비중을 학생에게 맞게 정합니다. 개념이 흔들리는 학생은 고등 기초수학부터 다시 세웁니다.",
        "cards": [
            ("고1", "공통수학 내신", "인천 고1 수학과외", "다항식, 방정식과 부등식, 경우의 수, 행렬과 도형의 방정식 등 공통수학 개념을 다지고 첫 고등 내신을 준비합니다.", ["공통수학1·2 내신 대비", "고등 기초수학 재정비", "첫 모의고사 대비"]),
            ("고2", "선택과목 내신", "인천 고2 수학과외", "학교에서 배우는 선택 과목의 개념과 유형을 정리하고, 수학내신과 모의고사를 함께 대비합니다.", ["선택과목 수학내신", "학교별 기출 분석", "수능 개념 연결"]),
            ("고3", "수능수학 실전", "인천 고3 수학과외", "목표 등급에 맞춰 개념 빈틈을 메우고 기출 분석과 실전 모의 풀이로 수능대비를 진행합니다.", ["수능수학 기출 분석", "실전 모의고사 풀이", "시간 배분과 오답 관리"]),
        ],
        "faq": [
            ("고등학생인데 중학교 수학 기초가 부족해요.", "고등 수학에 필요한 중학교 단원만 골라 빠르게 보완하면서 현재 학교 진도를 함께 진행합니다."),
            ("내신과 수능 중 무엇을 먼저 해야 하나요?", "학년과 진학 목표에 따라 다릅니다. 고1·고2는 수학내신과 개념을 중심으로, 고3은 목표에 맞춰 수능수학 비중을 높이는 경우가 많습니다. 상담 때 학생에게 맞는 비중을 함께 정합니다."),
            ("고3 수능수학은 언제부터 준비하나요?", "개념 빈틈이 있다면 가능한 빨리 보완을 시작하는 것이 좋습니다. 이후 기출 분석과 실전 모의 풀이로 시간 관리까지 준비합니다."),
        ],
    },
]

LANDING_LINKS = [(page["title"].split(" | ")[0], page["slug"]) for page in LANDING_PAGES]

DISTRICT_HUBS = {
    "제물포구": "jemulpo-gu", "영종구": "yeongjong-gu", "미추홀구": "michuhol-gu", "연수구": "yeonsu-gu", "남동구": "namdong-gu",
    "부평구": "bupyeong-gu", "계양구": "gyeyang-gu", "서해구": "seohae-gu", "검단구": "geomdan-gu", "강화군": "ganghwa-gun", "옹진군": "ongjin-gun",
}
GRADE_SHORT = {"초등학교": ("초등", "elementary-math"), "중학교": ("중등", "middle-math"), "고등학교": ("고등", "high-math")}
GRADE_FOCUS = {
    "초등학교": "초등 기초수학·연산·서술형부터 예비중1 준비까지",
    "중학교": "중등 수학내신·서술형, 기초수학 보완부터 예비고1 준비까지",
    "고등학교": "고등 수학내신과 수능대비·수능수학까지",
}
GRADE_TEMPLATES = {page["school_type"]: page for page in LANDING_PAGES if "school_type" in page}


def district_grade_slug(district, school_type):
    return f"{DISTRICT_HUBS[district]}-{GRADE_SHORT[school_type][1]}"


def district_grade_links(districts, school_types=SCHOOL_TYPES, exclude=None, prefix="../"):
    return [
        (f"{district} {GRADE_SHORT[school_type][0]} 수학과외", f"{prefix}{district_grade_slug(district, school_type)}/")
        for district in districts for school_type in school_types
        if district_grade_slug(district, school_type) != exclude
    ]


def build_district_grade_pages():
    pages = []
    for district in SCHOOL_DISTRICTS:
        for school_type in SCHOOL_TYPES:
            template = GRADE_TEMPLATES[school_type]
            short, grade_slug = GRADE_SHORT[school_type]
            slug = district_grade_slug(district, school_type)
            schools = [school for school in SCHOOLS if school["district"] == district and school["type"] == school_type]
            name = f"인천 {district} {short} 수학과외"
            example = "·".join(school["name"] for school in schools[:2])
            pages.append({
                "slug": slug, "area": f"{district} {short}", "label": f"{district} {short} 수학",
                "school_type": school_type, "school_districts": [district],
                "title": f"{name} | {template['title'].split(' | ')[1]}",
                "description": f"{name} - {example} 등 {district} {school_type} {len(schools)}곳 학교별 {GRADE_FOCUS[school_type]} 1:1 맞춤 수학수업. 무료 학습 상담 {PHONE}",
                "h1": f"인천 {district} {short} 수학과외,", "em": template["em"], "hero": template["hero"],
                "intro_h2": f"{district} {short} 수학,<br>학교별로 준비합니다", "lead": template["lead"],
                "body": f"{district}에는 {school_type} {len(schools)}곳이 있고, 학교마다 진도와 시험 범위, 출제 유형이 다릅니다. {template['body']}",
                "cards": [(label, title, tags.replace("인천 ", f"{district} "), body, points) for label, title, tags, body, points in template["cards"]],
                "faq": template["faq"],
                "links_title": f"{district}·{short}<br>수학과외 더 보기",
                "links": district_grade_links([district], exclude=slug)
                + [(f"{district} 수학과외", f"../{DISTRICT_HUBS[district]}/"), (f"인천 {short} 수학과외", f"../{grade_slug}/")]
                + district_grade_links([other for other in SCHOOL_DISTRICTS if other != district], [school_type]),
            })
    return pages


DISTRICT_GRADE_PAGES = build_district_grade_pages()
ALL_LANDING_PAGES = LANDING_PAGES + DISTRICT_GRADE_PAGES


def render_landing(page, index):
    slug, area = page["slug"], page["area"]
    canonical = f"https://eduline.kr/{slug}/"
    grade_page = "cards" in page
    name = page["title"].split(" | ")[0]
    faq = page["faq"] + (AREA_GRADE_FAQ if not grade_page else []) + [
        (f"{name} 상담은 어떻게 신청하나요?", f"{PHONE}로 전화 주시면 학생에게 맞는 수업 방향과 가능한 일정을 안내해 드립니다.")
    ]
    if grade_page:
        guide = cards_section("curriculum", "MATH BY GRADE", f"{name}<br>학년별 수업 안내", page["description"].split(" - ")[1].split(". ")[0] + ".", page["cards"])
        school_type = page["school_type"]
        if "school_districts" in page:
            links, links_title, links_kicker = page["links"], page["links_title"], "MORE GUIDE"
            district_schools = [school for school in SCHOOLS if school["district"] in page["school_districts"] and school["type"] == school_type]
            schools = school_section(
                f"{area} 학교별<br>수학 내신 대비",
                html_escape(school_lead(area, district_schools)),
                f'<ul class="school-chips school-chips-wide">{school_chips(district_schools)}</ul>',
            )
        else:
            links = district_grade_links(SCHOOL_DISTRICTS, [school_type]) + [(title, f"../{target}/") for title, target in LANDING_LINKS if target != slug] + DISTRICT_LINKS
            links_title, links_kicker = "지역별·학년별<br>수학과외 안내", "MORE GUIDE"
            schools = grouped_school_section(
                f"인천 {school_type}별<br>수학 내신 대비",
                f"인천 {school_type} {sum(s['type'] == school_type for s in SCHOOLS)}곳의 학교별 진도와 시험 범위, 기출 유형에 맞춰 수업합니다. 구·군을 선택해 학교 목록을 확인해 보세요.",
                [school_type],
            )
    else:
        guide = grade_guide(area, index)
        links = page["links"] + district_grade_links(page["schools"][0]) + [(title, f"../{target}/") for title, target in LANDING_LINKS if target != slug and target.endswith("math")]
        links_title, links_kicker = page["links_title"], "LOCAL AREA GUIDE"
        schools = area_school_section(area, schools_in(*page["schools"]))
    link_html = "".join(f'<a href="{href}">{label}</a>' for label, href in links)
    schema = json_ld([
        {
            "@type": "Service", "name": name, "url": canonical, "serviceType": "1:1 수학과외",
            "telephone": "+82-10-2928-3614", "areaServed": "인천광역시", "description": page["description"],
            "provider": {"@type": "EducationalOrganization", "name": "인천 수학과외 EDULINE", "url": "https://eduline.kr/"},
        },
        breadcrumb_schema([("인천 수학과외", "https://eduline.kr/"), (name, canonical)]),
        faq_schema(area, faq),
    ])
    title, description = page["title"], page["description"]
    return f'''<!doctype html><html lang="ko"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description" content="{description}"><meta name="theme-color" content="#14362f"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SOCIAL_IMAGE}"><meta property="og:image:secure_url" content="{SOCIAL_IMAGE}"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="인천 수학과외 - 배운 만큼 풀리는 1:1 수업"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SOCIAL_IMAGE}"><meta name="twitter:image:alt" content="인천 수학과외 - 배운 만큼 풀리는 1:1 수업"><link rel="canonical" href="{canonical}"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><title>{title}</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="../styles.css?v={ASSET_VERSION}"><script type="application/ld+json">{schema}</script></head><body>
<header class="site-header" id="top"><a class="brand" href="../" aria-label="인천 수학과외 홈"><span class="brand-symbol" aria-hidden="true">∫</span><span>{name}<small>EDULINE</small></span></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="메뉴 열기"><span></span><span></span><span></span></button><nav class="primary-nav" id="primary-nav" aria-label="주요 메뉴"><a href="#approach">수업 안내</a><a href="#curriculum">학년별 수업</a><a href="#faq">자주 묻는 질문</a><a href="../">인천 전체</a><a class="nav-contact" href="#contact">상담 신청</a></nav></header>
<main><section class="hero" aria-labelledby="hero-title"><div class="hero-image" role="img" aria-label="선생님과 함께 수학 문제를 공부하는 학생"></div><div class="hero-overlay"></div><div class="hero-content"><p class="kicker light">{slug.upper()} MATH TUTORING</p><h1 id="hero-title">{page["h1"]}<br><em>{page["em"]}</em></h1><p class="hero-text">{page["hero"]}<br class="desktop-only"> 이해한 내용을 스스로 풀어낼 때까지 꼼꼼하게 이어갑니다.</p><div class="hero-actions"><a class="button button-coral" href="#contact">무료 학습 상담 <span aria-hidden="true">↗</span></a><a class="phone" href="tel:01029283614"><small>전화 상담</small><strong>010-2928-3614</strong></a></div></div><div class="hero-note" aria-hidden="true"><span>{str(index + 1).zfill(2)}</span><i></i><span>{page["label"]}</span></div></section>
<section class="intro section" id="approach"><div class="section-heading reveal"><p class="kicker">PERSONAL MATH LESSON</p><h2>{page["intro_h2"]}</h2></div><div class="intro-copy reveal"><p class="lead">{page["lead"]}</p><p>{page["body"]}</p></div><div class="values"><article class="value reveal"><span>01</span><strong>진단</strong><h3>개념 빈틈 확인</h3><p>최근 시험과 오답에서 막히는 지점을 찾습니다.</p></article><article class="value reveal"><span>02</span><strong>설계</strong><h3>개인별 진도 구성</h3><p>학교 일정과 목표에 맞춰 학습 순서를 정합니다.</p></article><article class="value reveal"><span>03</span><strong>관리</strong><h3>복습과 오답 점검</h3><p>배운 내용을 혼자서도 풀 수 있게 관리합니다.</p></article></div></section>
{guide}
{schools}
<section class="steps section"><div class="steps-heading reveal"><p class="kicker light">HOW WE BEGIN</p><h2>충분히 살펴보고<br>맞는 수업을 시작합니다</h2></div><ol class="step-list"><li class="reveal"><span>01</span><strong>학습 상담</strong><p>지역과 목표 확인</p></li><li class="reveal"><span>02</span><strong>실력 진단</strong><p>개념과 습관 점검</p></li><li class="reveal"><span>03</span><strong>학습 설계</strong><p>개인별 계획 제안</p></li><li class="reveal"><span>04</span><strong>수업 관리</strong><p>복습과 오답 확인</p></li></ol></section>
{faq_section(name.removesuffix(" 수학과외"), faq)}
<section class="locality-directory section" aria-labelledby="links-title"><div class="areas-heading reveal"><div><p class="kicker">{links_kicker}</p><h2 id="links-title">{links_title}</h2></div><p>원하는 지역과 학년의 수학과외 안내를 확인해 보세요.</p></div><div class="locality-grid nearby-grid">{link_html}</div></section>
<section class="contact" id="contact"><div class="contact-copy reveal"><p class="kicker">START YOUR WAY</p><h2>{name}<br>상담 신청</h2><p>전화 주시면 학생의 학년과 목표에 맞춰 상담을 도와드립니다.</p><a href="tel:01029283614"><small>전화 상담</small>010-2928-3614</a></div></section></main>
<footer class="site-footer"><a class="brand" href="../"><span class="brand-symbol" aria-hidden="true">∫</span><span>인천 수학과외<small>EDULINE</small></span></a><div><p>{name} · 초·중·고 1:1 수학과외</p><p>상담 문의 <a href="tel:01029283614">010-2928-3614</a></p></div><p>© <span id="year"></span> EDULINE. ALL RIGHTS RESERVED.</p></footer><a class="floating-contact" href="#contact" aria-label="상담 신청"><span>상담</span><span aria-hidden="true">↗</span></a><script src="../script.js?v={ASSET_VERSION}"></script></body></html>'''


def landing_links_section():
    links = "".join(f'<a href="{slug}/">{title}</a>' for title, slug in LANDING_LINKS)
    return (
        '<section class="locality-directory section" id="popular" aria-labelledby="popular-title"><div class="areas-heading reveal"><div><p class="kicker">POPULAR SEARCH</p>'
        '<h2 id="popular-title">많이 찾는<br>수학과외 안내</h2></div><p>송도·청라·검단·영종도 등 지역별 안내와 초등·중등·고등 학년별 수학과외 안내를 확인해 보세요.</p></div>'
        f'<div class="locality-grid nearby-grid">{links}</div></section>'
    )


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
    grade_links = "".join(f'<a href="{href}">{label}</a>' for label, href in district_grade_links(school_district(slug)))
    grade_links_section = (
        '<section class="locality-directory section" aria-labelledby="grade-links-title"><div class="areas-heading reveal"><div><p class="kicker">MATH BY GRADE</p>'
        f'<h2 id="grade-links-title">{district} 학년별<br>수학과외 안내</h2></div><p>초등·중등·고등 학년별 수학과외 안내와 학교 목록을 확인해 보세요.</p></div>'
        f'<div class="locality-grid nearby-grid">{grade_links}</div></section>'
    )
    html = set_seo_block(html, grade_guide(district, 0, "grade-guide") + area_school_section(district, slug_schools(slug)) + grade_links_section + faq_section(district))
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
    html = set_seo_block(html, grade_guide("인천", 0, "grade-guide") + grouped_school_section(
        "인천 학교별<br>수학 내신 대비",
        f"인천 초등학교 {sum(s['type'] == '초등학교' for s in SCHOOLS)}곳, 중학교 {sum(s['type'] == '중학교' for s in SCHOOLS)}곳, 고등학교 {sum(s['type'] == '고등학교' for s in SCHOOLS)}곳. 학생이 다니는 학교의 진도와 시험 범위, 기출 유형에 맞춰 수학내신과 수능대비를 준비합니다.",
        SCHOOL_TYPES,
    ) + faq_section("인천") + landing_links_section())
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
    urls.extend(
        f"  <url><loc>https://eduline.kr/{page['slug']}/</loc><lastmod>{LASTMOD}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>"
        for page in ALL_LANDING_PAGES
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
    items.extend((page["title"], f"https://eduline.kr/{page['slug']}/", page["description"]) for page in ALL_LANDING_PAGES)
    pub_date = "Sat, 24 Oct 2026 09:00:00 +0900"
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

for landing_index, landing_page in enumerate(ALL_LANDING_PAGES):
    directory = ROOT / landing_page["slug"]
    directory.mkdir(exist_ok=True)
    (directory / "index.html").write_text(render_landing(landing_page, landing_index), encoding="utf-8")

update_home()
(ROOT / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8")
(ROOT / "rss.xml").write_text(build_rss(), encoding="utf-8")
print(f"Generated {page_count} locality pages across {len(DISTRICTS)} districts and {len(ALL_LANDING_PAGES)} landing pages.")
