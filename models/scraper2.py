

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from fpdf import FPDF

# # URLs to scrape
# urls = {
#     "about": "https://www.nikles.com/about/",
#     "technologies": "https://www.nikles.com/technologies/",
#     "luxury_finishes": "https://www.nikles.com/nikles-luxury-finishes/",
#     "news": "https://www.nikles.com/news/"
# }

# # Initialize WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# def scrape_about():
#     driver.get(urls['about'])
#     time.sleep(3)  # Wait for the page to load

#     data = {}
#     data["Nikles in short"] = driver.find_element(By.XPATH, "//h2[text()='Nikles in short']/following-sibling::p").text
#     data["History"] = driver.find_element(By.XPATH, "//h2[text()='History']/following-sibling::p").text
#     data["Philosophy"] = driver.find_element(By.XPATH, "//h2[text()='Philosophy']/following-sibling::p").text
#     return data

# def scrape_technologies():
#     driver.get(urls['technologies'])
#     time.sleep(3)  # Wait for the page to load

#     technologies = []
#     technology_elements = driver.find_elements(By.XPATH, "//div[@class='technologies-list']/div")
#     for element in technology_elements:
#         tech_name = element.find_element(By.TAG_NAME, "h3").text
#         tech_details = element.find_element(By.TAG_NAME, "p").text
#         technologies.append({"name": tech_name, "details": tech_details})
#     return technologies

# def scrape_luxury_finishes():
#     driver.get(urls['luxury_finishes'])
#     time.sleep(3)  # Wait for the page to load

#     luxury_finishes = driver.find_element(By.CLASS_NAME, "content").text
#     return luxury_finishes

# def scrape_news():
#     driver.get(urls['news'])
#     time.sleep(3)  # Wait for the page to load

#     news = []
#     news_elements = driver.find_elements(By.XPATH, "//div[@class='news-list']/div")
#     for element in news_elements:
#         title = element.find_element(By.TAG_NAME, "h2").text
#         details = element.find_element(By.TAG_NAME, "p").text
#         news.append({"title": title, "details": details})
#     return news

# def create_pdf(data):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     pdf.set_font("Arial", size=12)

#     # About section
#     pdf.set_font("Arial", style='B', size=14)
#     pdf.cell(200, 10, txt="About Nikles", ln=True, align='C')
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt="Nikles in short", ln=True, align='L')
#     pdf.multi_cell(0, 10, txt=data['about']['Nikles in short'])
#     pdf.cell(200, 10, txt="History", ln=True, align='L')
#     pdf.multi_cell(0, 10, txt=data['about']['History'])
#     pdf.cell(200, 10, txt="Philosophy", ln=True, align='L')
#     pdf.multi_cell(0, 10, txt=data['about']['Philosophy'])

#     # Technologies section
#     pdf.add_page()
#     pdf.set_font("Arial", style='B', size=14)
#     pdf.cell(200, 10, txt="Technologies", ln=True, align='C')
#     pdf.set_font("Arial", size=12)
#     for tech in data['technologies']:
#         pdf.cell(200, 10, txt=tech['name'], ln=True, align='L')
#         pdf.multi_cell(0, 10, txt=tech['details'])

#     # Luxury finishes section
#     pdf.add_page()
#     pdf.set_font("Arial", style='B', size=14)
#     pdf.cell(200, 10, txt="Nikles Luxury Finishes", ln=True, align='C')
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, txt=data['luxury_finishes'])

#     # News section
#     pdf.add_page()
#     pdf.set_font("Arial", style='B', size=14)
#     pdf.cell(200, 10, txt="News", ln=True, align='C')
#     pdf.set_font("Arial", size=12)
#     for news_item in data['news']:
#         pdf.cell(200, 10, txt=news_item['title'], ln=True, align='L')
#         pdf.multi_cell(0, 10, txt=news_item['details'])

#     pdf.output("Nikles_Info.pdf")

# def main():
#     data = {}
#     data['about'] = scrape_about()
#     data['technologies'] = scrape_technologies()
#     data['luxury_finishes'] = scrape_luxury_finishes()
#     data['news'] = scrape_news()

#     # Save data to a CSV file for simplicity, but you can use other formats like JSON, database, etc.
#     pd.DataFrame([data['about']]).to_csv('about.csv', index=False)
#     pd.DataFrame(data['technologies']).to_csv('technologies.csv', index=False)
#     pd.DataFrame([{"luxury_finishes": data['luxury_finishes']}]).to_csv('luxury_finishes.csv', index=False)
#     pd.DataFrame(data['news']).to_csv('news.csv', index=False)

#     create_pdf(data)

#     driver.quit()

# if __name__ == "__main__":
#     main()

# src/backend/scrape_data.py

# URLs to scrape
urls = {
    "about": "https://www.nikles.com/about/",
    "technologies": "https://www.nikles.com/technologies/",
    "luxury_finishes": "https://www.nikles.com/nikles-luxury-finishes/",
    "news": "https://www.nikles.com/news/"
}

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_about():
    driver.get(urls['about'])
    time.sleep(3)  # Wait for the page to load

    data = {}
    data["Nikles in short"] = driver.find_element(By.XPATH, "//h2[text()='Nikles in short']/following-sibling::p").text
    data["History"] = driver.find_element(By.XPATH, "//h2[text()='History']/following-sibling::p").text
    data["Philosophy"] = driver.find_element(By.XPATH, "//h2[text()='Philosophy']/following-sibling::p").text
    return data

def scrape_technologies():
    driver.get(urls['technologies'])
    time.sleep(3)  # Wait for the page to load

    technologies = []
    technology_elements = driver.find_elements(By.XPATH, "//div[@class='technologies-list']/div")
    for element in technology_elements:
        tech_name = element.find_element(By.TAG_NAME, "h3").text
        tech_details = element.find_element(By.TAG_NAME, "p").text
        technologies.append({"name": tech_name, "details": tech_details})
    return technologies

def scrape_luxury_finishes():
    driver.get(urls['luxury_finishes'])
    time.sleep(3)  # Wait for the page to load

    luxury_finishes = driver.find_element(By.CLASS_NAME, "content").text
    return luxury_finishes

def scrape_news():
    driver.get(urls['news'])
    time.sleep(3)  # Wait for the page to load

    news = []
    news_elements = driver.find_elements(By.XPATH, "//div[@class='news-list']/div")
    for element in news_elements:
        title = element.find_element(By.TAG_NAME, "h2").text
        details = element.find_element(By.TAG_NAME, "p").text
        news.append({"title": title, "details": details})
    return news

def main():
    data = {}
    data['about'] = scrape_about()
    data['technologies'] = scrape_technologies()
    data['luxury_finishes'] = scrape_luxury_finishes()
    data['news'] = scrape_news()

    # Save data to a CSV file for simplicity, but you can use other formats like JSON, database, etc.
    pd.DataFrame([data['about']]).to_csv('about.csv', index=False)
    pd.DataFrame(data['technologies']).to_csv('technologies.csv', index=False)
    pd.DataFrame([{"luxury_finishes": data['luxury_finishes']}]).to_csv('luxury_finishes.csv', index=False)
    pd.DataFrame(data['news']).to_csv('news.csv', index=False)

    driver.quit()

if __name__ == "__main__":
    main()
