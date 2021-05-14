import requests
from bs4 import BeautifulSoup
import ecommerce_db
import pandas

prod_url="https://www.decathlon.in/men/men-s-footwear-17119?icm=minibanner&icn=MENFOOTWEAR&range%5Bprice%5D%5Bmin%5D=1221&page="

scraped_shoe_info_list=[]

ecommerce_db.db_connect("products.db")

for pg_num in range(1,7):
    url=prod_url+str(pg_num)

    print("GET request for: "+url)
    req=requests.get(url)
    content=req.content

    soup=BeautifulSoup(content,"html.parser")

    all_shoes=soup.find_all("div",{"class":"deca_card"})

    for shoe in all_shoes:
        shoe_dict={}
        shoe_dict["name"]=shoe.find("div",{"class":"mb-3 card-title"}).text
        #shoe_dict["picture"]=shoe.find("div",{"class":"swiper-slide-active"}).text - decathlon
        #shoe_dict["picture"]=shoe.find("div",{"class":"s-image-overlay"}).text - amazon
        shoe_dict["price"]=shoe.find("button",{"span":None}).text      #class":"price_tag mb-3
        try:
            shoe_dict["rating"]=shoe.find("span",{"class":"rate_number"}).text
        except AttributeError:
            shoe_dict["rating"]=None
        #try:
        #    shoe_dict["no_of_rating"]=shoe.find("a",{"class":"a-link-normal"}).text
        #except AttributeError:
        #    shoe_dict["no_of_rating"]=None

        scraped_shoe_info_list.append(shoe_dict)

        ecommerce_db.set_shoe_info("products.db",tuple(shoe_dict.values()))

data=pandas.DataFrame(scraped_shoe_info_list)
print("Creating csv file...")
data.to_csv("Shoes.csv")

ecommerce_db.get_shoe_info("products.db")
