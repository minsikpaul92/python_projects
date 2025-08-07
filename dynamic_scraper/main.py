from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

keywords = [
    "flutter",
    "nextjs",
    "kotlin",
]

for keyword in keywords:
    p = sync_playwright().start()

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")

    time.sleep(5)

    # page.click("button.Aside_searchButton__Ib5Dn.Aside_isNotMobileDevice__ko_mZ")

    # time.sleep(5)

    # page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

    # time.sleep(2)

    # page.keyboard.down("Enter")

    # time.sleep(6)

    # page.click("a#search_tab_position")

    # time.sleep(5)

    for _ in range(4):
        page.keyboard.down("End")
        time.sleep(3)

    content = page.content()
    p.stop()

    soup = BeautifulSoup(content, "html.parser")

    jobs = soup.find_all("div", class_="JobCard_container__zQcZs")

    jobs_db = []

    for job in jobs:
        link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
        title = job.find("strong", class_="JobCard_title___kfvj").text
        company_name = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu wds-nkj4w6").text
        period = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l wds-nkj4w6").text
        reward_elem = job.find("span", class_="JobCard_reward__oCSIQ")
        reward = reward_elem.text if reward_elem else "N/A"
        job = {
            "title":title,
            "company_name":company_name,
            "period":period,
            "reward":reward,
            "link":link,
        }
        jobs_db.append(job)

    file = open(f"{keyword}_jobs.csv", "w")
    writer = csv.writer(file)
    writer.writerow(job.keys())

    for job in jobs_db:
        writer.writerow(job.values())

    file.close()
