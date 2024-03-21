from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# פונקציה לסקרייפינג של פרטי משרה מסוימת
def scrape_job_info(driver, job_url):
    driver.get(job_url)
    time.sleep(1)

    job_details = driver.find_element(By.ID, "dnn_ctr505_OfferDetails_pnlOfferDetails")
    title = job_details.find_element(By.ID, "dnn_ctr505_OfferDetails_hTitle").text
    job_desc = job_details.find_element(By.ID, "dnn_ctr505_OfferDetails_lblODesc").text
    requirements = job_details.find_element(By.ID, "dnn_ctr505_OfferDetails_lblONeedsValue").text
    category = job_details.find_element(By.ID, "dnn_ctr505_OfferDetails_lblOField").text
    try:
        company_size = job_details.find_element(By.ID, "dnn_ctr505_OfferDetails_lblCoSize").text
    except:
        company_size = "לא צוין"

    return title, job_desc, requirements, company_size, category

# פונקציה לסקרייפינג של כל המשרות בקטגוריה מסוימת
def scrape_jobs_in_category(driver, category_url):
    driver.get(category_url)
    time.sleep(1)

    job_links = driver.find_elements(By.CSS_SELECTOR, "a.value.tooltip-activator")
    job_links = [link.get_attribute("href") for link in job_links]

    for job_link in job_links:
        title, job_desc, requirements, company_size, category = scrape_job_info(driver, job_link)
        with open("./jobs.csv", "a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([title, job_desc, requirements, company_size, category])
        time.sleep(1)

# פונקציה לסקרייפינג של כל הקטגוריות והמשרות באתר
def scrape_categories_and_jobs(main_url):
    driver = webdriver.Chrome()
    driver.get(main_url)
    time.sleep(1)

    categories = driver.find_elements(By.CSS_SELECTOR, "a.Normal")[:10]
    category_links = [category.get_attribute("href") for category in categories]

    for category_link in category_links:
        scrape_jobs_in_category(driver, category_link)
        time.sleep(1)

    driver.quit()

def main():
    scrape_categories_and_jobs("https://www.jobinfo.co.il/%D7%93%D7%A8%D7%95%D7%A9%D7%99%D7%9D-%D7%94%D7%99%D7%99%D7%98%D7%A7/%D7%93%D7%A8%D7%95%D7%A9%D7%99%D7%9D-%D7%AA%D7%95%D7%9B%D7%A0%D7%94")
    print('סיים')

if __name__ == "__main__":
    main()
