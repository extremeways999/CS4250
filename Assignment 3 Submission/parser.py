import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["crawler_db"]
pages_collection = db["pages"]
professors_collection = db["professors"]

def get_target_page_html(target_url):
    page = pages_collection.find_one({"url": target_url})
    if page:
        return page["html"]
    else:
        print("Target page not found.")
        return None
def parse_and_store_faculty_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    faculty_members = soup.find_all("div", class_="faculty-member")

    for member in faculty_members:
        name = member.find("span", class_="name").get_text(strip=True) if member.find("span", class_="name") else "N/A"
        title = member.find("span", class_="title").get_text(strip=True) if member.find("span", class_="title") else "N/A"
        office = member.find("span", class_="office").get_text(strip=True) if member.find("span", class_="office") else "N/A"
        phone = member.find("span", class_="phone").get_text(strip=True) if member.find("span", class_="phone") else "N/A"
        email = member.find("span", class_="email").get_text(strip=True) if member.find("span", class_="email") else "N/A"
        website = member.find("a", class_="website")["href"] if member.find("a", class_="website") else "N/A"
#creating dictionary to store parsed data for each faculty member
        professor_data = {"name": name,"title": title,"office": office,"phone": phone,"email": email,"website": website}
        professors_collection.insert_one(professor_data) #insert faculty data into professors collection
    
    print("Faculty data stored.")

if __name__ == "__main__":
    target_url = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"
    html_content = get_target_page_html(target_url)

    if html_content:
        parse_and_store_faculty_data(html_content)
