import json

import requests
from bs4 import BeautifulSoup

url = 'https://www.unian.ua/recipes'

# req = requests.get(url)
# src = req.text
#
# with open("main.html", "w") as file:
#     file.write(src)
with open("main.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

final_lst = []
list_of_all_dishes = []

tarfile = soup.find(class_="content-column").find_all(class_="cooking-background__item")
for i in tarfile:
    temp_name = ""
    temp_dict = {}
    temp_lst = []
    temp = i.find_all("a")
    list_of_every_dish = []

    for item in temp:
        temp_list_of_deepest_dishes = []
        if item.get("class")[0] == "cooking-background__title":
            temp_name = item.text.strip()
        else:
            list_of_every_dish.append(item.get("href"))
            temp_url = item.get("href")
            temp_request_for_every = requests.get(temp_url).text
            temp_soup_for_dish = BeautifulSoup(temp_request_for_every, "lxml")
            list_of_all_names_dishes = temp_soup_for_dish.find_all("div", class_="cooking-recipe__item cooking-recipe__item--big")
            for name in list_of_all_names_dishes:
                temp_name = name.find("h3").text.strip()
                temp_list_of_deepest_dishes.append(temp_name)

            temp_lst.append({item.text.strip(): temp_list_of_deepest_dishes})


        temp_dict[temp_name] = temp_lst
    final_lst.append(temp_dict)
    list_of_all_dishes.append(list_of_every_dish)

for item in final_lst:
    for dish in item:
        print(f"{dish}: {item[dish]}")
with open("main.json", 'a', encoding="utf-8") as file:
    json.dump(final_lst, file, indent=4, ensure_ascii=False)
