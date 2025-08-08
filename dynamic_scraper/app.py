# 필요한 라이브러리를 가져옵니다.
# Flask: 웹 프레임워크
# render_template: HTML 템플릿을 렌더링
# request: HTTP 요청 정보에 접근
# requests: HTTP 요청을 보내기 위함
# BeautifulSoup: HTML/XML을 파싱
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
import os

# Flask 애플리케이션을 초기화합니다.
app = Flask("JobScraper")

# 이전에 스크래핑한 결과를 저장하기 위한 가짜 데이터베이스(딕셔너리)
# 매번 검색할 때마다 새로 스크래핑하는 것을 방지하여 속도를 높입니다.
db = {}

# Berlin Startup Jobs에서 채용 정보를 스크래핑하는 함수
def scrape_berlinstartupjobs(term):
    """
    주어진 검색어로 berlinstartupjobs.com에서 채용 정보를 스크랩합니다.
    """
    url = f"https://berlinstartupjobs.com/skill-areas/{term}/"
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        })
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Berlin Startup Jobs: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("li", class_="bjs-jlid")
    
    results = []
    for job in jobs:
        title_element = job.find("h4", class_="bjs-jlid__h")
        company_element = job.find("a", class_="bjs-jlid__b")
        link_element = job.find("a")

        if title_element and company_element and link_element:
            title = title_element.get_text(strip=True)
            company = company_element.get_text(strip=True)
            link = link_element["href"]
            results.append({"title": title, "company": company, "link": link})
    return results

# We Work Remotely에서 채용 정보를 스크래핑하는 함수
def scrape_weworkremotely(term):
    """
    주어진 검색어로 weworkremotely.com에서 채용 정보를 스크랩합니다.
    """
    url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        })
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching We Work Remotely: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find("section", class_="jobs").find_all("li")
    
    results = []
    for job in jobs:
        # 'view-all' 링크와 같은 불필요한 li 태그를 건너뜁니다.
        if job.find("a"):
            title_element = job.find("span", class_="title")
            company_element = job.find("span", class_="company")
            link_element = job.find("a", href=True)

            if title_element and company_element and link_element:
                title = title_element.get_text(strip=True)
                company = company_element.get_text(strip=True)
                link = f"https://weworkremotely.com{link_element['href']}"
                results.append({"title": title, "company": company, "link": link})
    return results

# Web3 Career에서 채용 정보를 스크래핑하는 함수
def scrape_web3career(term):
    """
    주어진 검색어로 web3.career에서 채용 정보를 스크랩합니다.
    """
    url = f"https://web3.career/{term}-jobs"
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        })
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Web3 Career: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    # 'tbody'에서 직접 'tr'을 찾습니다.
    job_rows = soup.find("tbody").find_all("tr", class_="table_row")
    
    results = []
    for row in job_rows:
        link_element = row.find("a")
        title_element = row.find("h2")
        # 회사는 종종 'td' > 'div' > 'div' > 'a' 구조에 있습니다.
        company_element = row.select_one("td:nth-of-type(1) > div > div > a")
        
        if title_element and company_element and link_element:
            title = title_element.get_text(strip=True)
            company = company_element.get_text(strip=True)
            link = f"https://web3.career{link_element['href']}"
            results.append({"title": title, "company": company, "link": link})
    return results


# 메인 페이지 라우트
@app.route("/")
def home():
    """홈페이지를 렌더링합니다."""
    return render_template("home.html")

# 검색 결과 페이지 라우트
@app.route("/search")
def search():
    """
    검색어를 받아 각 사이트에서 스크래핑하고 결과를 표시합니다.
    """
    term = request.args.get('term')
    if not term:
        # 검색어가 없으면 홈으로 리다이렉트합니다.
        return redirect(url_for("home"))
    
    term_lower = term.lower()
    
    # 캐시된 결과가 있는지 확인합니다.
    if term_lower in db:
        jobs = db[term_lower]
    else:
        # 캐시에 없으면 새로 스크래핑합니다.
        jobs = (
            scrape_berlinstartupjobs(term_lower) +
            scrape_weworkremotely(term_lower) +
            scrape_web3career(term_lower)
        )
        # 결과를 캐시에 저장합니다.
        db[term_lower] = jobs
        
    return render_template("search.html", term=term, jobs=jobs, job_count=len(jobs))

# 스크립트가 직접 실행될 때 Flask 서버를 시작합니다.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
