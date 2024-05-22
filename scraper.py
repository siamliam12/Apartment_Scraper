import requests 
from bs4 import BeautifulSoup as bs
import json


def customize_input(user_input):
    # Remove leading/trailing whitespace and split the input into words
    words = user_input.strip().split()
    
    # Capitalize the first letter of each word
    capitalized_words = [word.capitalize() for word in words]
    
    # Join the words with hyphens
    customized_input = '-'.join(capitalized_words)
    
    return customized_input
city = input("Enter city: ").strip()
country = input("Enter country: ").strip()
city = customize_input(city)
country = customize_input(country)
baseurl = "https://housinganywhere.com"
search_url = f"https://housinganywhere.com/s/{city}--{country}"
print(search_url)
page = requests.get(search_url)
soup = bs(page.content,"html.parser")
all_apartments = soup.find_all("div",class_="css-13xb9t5-card")
all_apartments_link = soup.find_all("div",class_="css-jdbo8x-HousingAnywhereColorProvider-root")

# empty lists 
apartment_data = []
links_list = []

for links in all_apartments_link:
    link = links.find_all("a",class_="css-1a3e697-cardLink")
    for tag in link:
        href = tag.get('href')
        href = baseurl + href
        title = tag.get('title')
        links_list.append({"title": title,"link": href})
for i,apartment in enumerate(all_apartments):
    price= apartment.find("span",class_="MuiTypography-root")
    details = apartment.find("div",class_="css-1nl1v0i-propertyInfo")
    if i < len(links_list):
        link_info = links_list[i]
        title = link_info["title"]
        href = link_info["link"]
    else: 
        title = "N/A"
        href = "N/A"
    apartment_data.append({
        "title": title,
        "link":href,
        "price":price.text,
        "details":details.text
    })
json_data = []
for data in apartment_data:
    json_data.append(data)
with open("output.json", "a",encoding="utf-8") as file:
    json.dump(json_data, file,ensure_ascii=False, indent=4)
    file.write(",")
    file.close()