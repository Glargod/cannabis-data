from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import sqlite3
import time

# URL
url = "https://www.leafly.com/strains/blue-dream"

# Set up headless Firefox
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Fetch page
try:
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript
    soup = BeautifulSoup(driver.page_source, "html.parser")
except Exception as e:
    print(f"Error fetching page: {e}")
    driver.quit()
    exit()
finally:
    driver.quit()

# Strain name
strain_name_elem = soup.find("h1")
strain_name = strain_name_elem.text.strip() if strain_name_elem else "Unknown Strain"

# Terpenes
terpene_span = soup.find("span", string="Terpenes:")
terpenes = []
if terpene_span:
    # Get the parent <ul> or sibling <a> tags
    parent = terpene_span.find_parent()
    terpene_links = parent.find_all("a", class_="text-green")
    terpenes = [link.text.strip().capitalize() for link in terpene_links
                if link.text.strip().lower() in ["myrcene", "pinene", "caryophyllene", "limonene", "terpinolene"]]
    print("Debug: Terpene links found:", [link.text.strip() for link in terpene_links])
terpenes = terpenes if terpenes else ["Not found"]

# Helps with
helps_with_section = soup.find("div", id="helps-with-section")
helps_with = []
if helps_with_section:
    conditions = helps_with_section.find_all("li", class_="mb-xl")
    for condition in conditions:
        name_elem = condition.find("a", class_="font-bold")
        percent_elem = condition.find("span", class_="font-bold")
        if name_elem and percent_elem:
            name = name_elem.text.strip()
            percent = percent_elem.text.strip()
            helps_with.append(f"{name} ({percent})")
helps_with = helps_with if helps_with else ["Not found"]

# Save to SQLite
conn = sqlite3.connect("cannabis_data.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS strains (
        name TEXT UNIQUE,
        terpenes TEXT,
        helps_with TEXT
    )
""")

# Insert data
cursor.execute(
    "INSERT OR REPLACE INTO strains (name, terpenes, helps_with) VALUES (?, ?, ?)",
    (strain_name, ", ".join(terpenes), ", ".join(helps_with))
)

conn.commit()
conn.close()

print(f"Saved: {strain_name}")
print(f"Terpenes: {', '.join(terpenes)}")
print(f"Helps with: {', '.join(helps_with)}")
