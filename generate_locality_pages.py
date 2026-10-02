from pathlib import Path
from urllib.parse import quote
import json
import re


ROOT = Path(__file__).parent
LASTMOD = "2026-10-02"
FORM_ACTION = "https://script.google.com/macros/s/AKfycby5gWmodksOJ1oI7YBIBO9cZtlHjPZXqIQ4vbHYIvL52DLf4ZLBJaXr9jiYzdLpRRH4Ig/exec"

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


def encoded(value):
    return quote(value, safe="")


def render_page(slug, district, locality, index):
    canonical = f"https://eduline.kr/{slug}/{encoded(locality)}/"
    rural = locality.endswith(("읍", "면"))
    area_copy = (
        f"{locality}의 이동 여건과 학교 일정, 학생의 학습 목표를 함께 확인해 가능한 수업 일정과 방식을 안내합니다."
        if rural else
        f"{locality} 학생의 학교 진도와 최근 시험, 풀이 습관을 확인해 복습·현행·선행의 균형을 정합니다."
    )
    action_copy = "수업 가능 지역 상담" if rural else "무료 학습 상담"
    area_label = f"{locality} 지역별 상담" if rural else f"{locality} 맞춤 수업"
    number = str(index + 1).zfill(2)
    schema = json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": f"인천 {locality} 수학과외", "url": canonical,
        "telephone": "+82-10-2928-3614", "areaServed": f"인천광역시 {district} {locality}",
        "provider": {"@type": "EducationalOrganization", "name": "인천 수학과외 EDULINE", "url": "https://eduline.kr/"},
    }, ensure_ascii=False, separators=(",", ":"))
    return f'''<!doctype html><html lang="ko"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description" content="인천 {district} {locality} 수학과외 - 초등·중등·고등 1:1 맞춤 수업. 개념 복습부터 학교 내신과 수능 준비까지 학생별로 지도합니다."><meta name="theme-color" content="#14362f"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="인천 {locality} 수학과외 | 초중고 1:1 맞춤 수업"><meta property="og:description" content="{district} {locality} 학생을 위한 개인별 수학 학습 설계"><meta property="og:url" content="{canonical}"><link rel="canonical" href="{canonical}"><link rel="icon" href="../../favicon.svg" type="image/svg+xml"><title>인천 {locality} 수학과외 | {district} 초중고 맞춤 지도</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="../../styles.css"><script type="application/ld+json">{schema}</script></head><body>
<header class="site-header" id="top"><a class="brand" href="../../" aria-label="인천 수학과외 홈"><span class="brand-symbol" aria-hidden="true">∫</span><span>{locality} 수학과외<small>EDULINE</small></span></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="메뉴 열기"><span></span><span></span><span></span></button><nav class="primary-nav" id="primary-nav" aria-label="주요 메뉴"><a href="#approach">수업 안내</a><a href="#curriculum">학년별 준비</a><a href="../">{district} 지역</a><a class="nav-contact" href="#contact">상담 신청</a></nav></header>
<main><section class="hero" aria-labelledby="hero-title"><div class="hero-image" role="img" aria-label="선생님과 함께 수학 문제를 공부하는 학생"></div><div class="hero-overlay"></div><div class="hero-content"><p class="kicker light">{slug.upper()} {number} MATH TUTORING</p><h1 id="hero-title">인천 {locality} 수학과외,<br><em>학생에게 맞는 1:1 수업</em></h1><p class="hero-text">{area_copy}<br class="desktop-only"> 이해한 내용을 스스로 풀어낼 때까지 꼼꼼하게 이어갑니다.</p><div class="hero-actions"><a class="button button-coral" href="#contact">{action_copy} <span aria-hidden="true">↗</span></a><a class="phone" href="tel:01029283614"><small>전화 상담</small><strong>010-2928-3614</strong></a></div></div><div class="hero-note" aria-hidden="true"><span>{number}</span><i></i><span>{area_label}</span></div></section>
<section class="intro section" id="approach"><div class="section-heading reveal"><p class="kicker">PERSONAL MATH LESSON</p><h2>현재 실력에서<br>필요한 공부부터</h2></div><div class="intro-copy reveal"><p class="lead">정해진 진도보다<br><strong>학생의 이해를 먼저 봅니다.</strong></p><p>{area_copy} 개념 이해도와 계산 정확도, 문제 해석 과정을 살핀 뒤 학생이 소화할 수 있는 순서로 수업합니다.</p></div><div class="values"><article class="value reveal"><span>01</span><strong>진단</strong><h3>개념 빈틈 확인</h3><p>최근 시험과 오답에서 막히는 지점을 찾습니다.</p></article><article class="value reveal"><span>02</span><strong>설계</strong><h3>개인별 진도 구성</h3><p>학교 일정과 목표에 맞춰 학습 순서를 정합니다.</p></article><article class="value reveal"><span>03</span><strong>관리</strong><h3>복습과 오답 점검</h3><p>배운 내용을 혼자서도 풀 수 있게 관리합니다.</p></article></div></section>
<section class="areas section" id="curriculum"><div class="areas-heading reveal"><div><p class="kicker">GRADE-BY-GRADE GUIDE</p><h2>학년과 목표에 맞춘<br>{locality} 수학 수업</h2></div><p>이전 과정의 기초부터 학교 내신과 수능 준비까지 단계별로 연결합니다.</p></div><div class="values"><article class="value reveal"><span>01</span><strong>초등</strong><h3>개념과 연산 습관</h3><p>교과 개념을 정확히 이해하고 풀이 과정을 설명하는 힘을 기릅니다.</p></article><article class="value reveal"><span>02</span><strong>중등</strong><h3>내신과 고등 기초</h3><p>학교 진도와 시험 유형을 반영하고 취약 단원을 집중 보완합니다.</p></article><article class="value reveal"><span>03</span><strong>고등</strong><h3>내신·수능 목표 설계</h3><p>개념, 기출, 실전 문제를 학생의 목표에 맞춰 단계적으로 학습합니다.</p></article></div></section>
<section class="steps section"><div class="steps-heading reveal"><p class="kicker light">HOW WE BEGIN</p><h2>충분히 살펴보고<br>맞는 수업을 시작합니다</h2></div><ol class="step-list"><li class="reveal"><span>01</span><strong>학습 상담</strong><p>지역과 목표 확인</p></li><li class="reveal"><span>02</span><strong>실력 진단</strong><p>개념과 습관 점검</p></li><li class="reveal"><span>03</span><strong>학습 설계</strong><p>개인별 계획 제안</p></li><li class="reveal"><span>04</span><strong>수업 관리</strong><p>복습과 오답 확인</p></li></ol></section>
<section class="contact" id="contact"><div class="contact-copy reveal"><p class="kicker">START YOUR WAY</p><h2>{locality} 수학과외<br>상담 신청</h2><p>학생의 학년과 목표, 정확한 거주 지역을 남겨주시면 맞춤 상담을 도와드립니다.</p><a href="tel:01029283614"><small>전화 상담</small>010-2928-3614</a></div><form class="contact-form reveal" id="contact-form" action="{FORM_ACTION}" method="POST"><input type="hidden" name="_token" value="tutorway-2026-mail"><input type="hidden" name="사이트" value="eduline.kr - 인천 {district} {locality}"><input class="honeypot" type="text" name="_honey" tabindex="-1" autocomplete="off"><div class="form-row"><label>학생 이름<input type="text" name="학생 이름" autocomplete="name" placeholder="이름" required></label><label>학년<select name="학년" required><option value="">선택해 주세요</option><option>초등학생</option><option>중학교 1학년</option><option>중학교 2학년</option><option>중학교 3학년</option><option>고등학교 1학년</option><option>고등학교 2학년</option><option>고등학교 3학년</option></select></label></div><label>보호자 연락처<input type="tel" name="보호자 연락처" autocomplete="tel" inputmode="tel" placeholder="010-0000-0000" required></label><label>거주 도로명주소<input type="text" name="거주 도로명주소" autocomplete="street-address" placeholder="인천광역시 {district} {locality} 도로명주소" required></label><label>상담 내용<textarea name="상담 내용" rows="3" placeholder="학습 고민이나 원하는 수업 방향을 적어주세요."></textarea></label><label class="agreement"><input type="checkbox" name="개인정보 수집 동의" value="동의" required><span>상담 및 회신을 위한 개인정보 수집·이용과 이메일 전송에 동의합니다.</span></label><button class="button submit-button" type="submit">상담 신청하기 <span aria-hidden="true">↗</span></button><p class="form-status" role="status" aria-live="polite"></p></form></section></main>
<footer class="site-footer"><a class="brand" href="../../"><span class="brand-symbol" aria-hidden="true">∫</span><span>인천 수학과외<small>EDULINE</small></span></a><div><p>{district} {locality} 초·중·고 1:1 수학과외</p><p>상담 문의 <a href="tel:01029283614">010-2928-3614</a></p></div><p>© <span id="year"></span> EDULINE. ALL RIGHTS RESERVED.</p></footer><a class="floating-contact" href="#contact" aria-label="상담 신청"><span>상담</span><span aria-hidden="true">↗</span></a><script src="../../script.js"></script></body></html>'''


def update_parent(slug, district, localities):
    file_path = ROOT / slug / "index.html"
    html = file_path.read_text(encoding="utf-8")
    links = "".join(f'<a href="{encoded(locality)}/">{locality}</a>' for locality in localities)
    section = (
        '<!-- LOCALITY_LINKS_START --><section class="locality-directory section" aria-labelledby="locality-title">'
        f'<div class="areas-heading"><div><p class="kicker">LOCAL AREA GUIDE</p><h2 id="locality-title">{district} 동·읍·면별<br>수학과외 안내</h2></div>'
        '<p>거주 지역을 선택하면 해당 지역의 1:1 수학과외 안내와 상담 신청을 확인할 수 있습니다.</p></div>'
        f'<div class="locality-grid">{links}</div></section><!-- LOCALITY_LINKS_END -->'
    )
    if "<!-- LOCALITY_LINKS_START -->" in html:
        html = re.sub(r"<!-- LOCALITY_LINKS_START -->.*?<!-- LOCALITY_LINKS_END -->", section, html, flags=re.S)
    else:
        html = html.replace('<section class="contact" id="contact">', section + '\n<section class="contact" id="contact">')
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


page_count = 0
for district_slug, district_name, locality_names in DISTRICTS:
    update_parent(district_slug, district_name, locality_names)
    for locality_index, locality_name in enumerate(locality_names):
        directory = ROOT / district_slug / locality_name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(
            render_page(district_slug, district_name, locality_name, locality_index), encoding="utf-8"
        )
        page_count += 1

(ROOT / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8")
print(f"Generated {page_count} locality pages across {len(DISTRICTS)} districts.")