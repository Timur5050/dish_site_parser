import json
import os
import shutil

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

    for index, item in enumerate(temp):
        temp_list_of_deepest_dishes = []
        if item.get("class")[0] == "cooking-background__title":
            temp_name = item.text.strip()
        else:
            list_of_every_dish.append(item.get("href"))
            temp_lst.append({item.text.strip(): temp_list_of_deepest_dishes})



        temp_dict[temp_name] = temp_lst
    final_lst.append(temp_dict)
    list_of_all_dishes.append(list_of_every_dish)


# print(final_lst)
# for item in final_lst:
#     for dishes in item:
#         for deepest_dish in item[dishes]:
#             for final in deepest_dish:
#                 print(f"{deepest_dish} ~~~ {deepest_dish[final]}")
#         print(f"{dishes}: {item[dishes]}")

# it was creating all html pages form all subtypes of dishes
amount_of_dirs = 7
# for index, links in enumerate(list_of_all_dishes):
#     path_dir = f'F:\important\python\pythonProjects\- web-scraping\my_prot\data\data{index + 1}'
#     for indexy, link in enumerate(links):
#         temp_request_for_every = requests.get(link).text
#         if not os.path.exists(path_dir):
#             os.mkdir(path_dir)
#             with open(f"F:\important\python\pythonProjects\- web-scraping\my_prot\data\data{index + 1}\dish{indexy + 1}.html", "w", encoding='utf-8') as file:
#                 file.write(temp_request_for_every)
#         else:
#             with open(f"F:\important\python\pythonProjects\- web-scraping\my_prot\data\data{index + 1}\dish{indexy + 1}.html", "w", encoding='utf-8') as file:
#                 file.write(temp_request_for_every)


# now, getting all data from saved before html pages
temp_dict_for_all_fast_dishes = {}
counter = 1
for dir_index in range(1, amount_of_dirs + 2):
    html_index = 1
    while True:
        temp_html = f"data\data{dir_index}\dish{html_index}.html"
        if os.path.isfile(temp_html):
            temp_list_for_dishes = []
            with open(temp_html, encoding="utf-8") as file:
                temp_src = file.read()

            temp_soup_for_dish = BeautifulSoup(temp_src, "lxml")
            list_of_all_names_dishes = temp_soup_for_dish.find_all("div", class_="cooking-recipe__item cooking-recipe__item--big")
            for name in list_of_all_names_dishes:
                temp_name = name.find("h3").text.strip()
                temp_list_for_dishes.append(temp_name)

            temp_dict_for_all_fast_dishes[counter] = temp_list_for_dishes

            html_index += 1
            counter += 1
        else:
            break

with open("temp.json", 'a', encoding="utf-8") as file:
    json.dump(temp_dict_for_all_fast_dishes, file, indent=4, ensure_ascii=False)

final_counter = 1

for item in final_lst:
    for dishes in item:
        for deepest_dish in item[dishes]:
            for final in deepest_dish:
                deepest_dish[final].extend(temp_dict_for_all_fast_dishes[final_counter])
                final_counter += 1

with open("main.json", 'a', encoding="utf-8") as file:
    json.dump(final_lst, file, indent=4, ensure_ascii=False)