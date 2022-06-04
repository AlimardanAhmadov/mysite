from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, Orders
from datetime import datetime
import time
from requests.auth import HTTPBasicAuth
import requests
from woocommerce import API
import math
import pandas as pd
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .forms import QuillFieldForm
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_orders(api_key):
    wcapi = API(
    url="https://cantaistiyorum.com",
    consumer_key=api_key,
    consumer_secret="cs_daa346482eca9d5ca755744cefcb999d27216de2",
    version="wc/v3",
    query_string_auth=True,
    timeout=30)
    orders = []
    r = wcapi.get("orders", params={"per_page": 100, "page":1, "status":"shipped,packed,completed,processing"})
    # changing status from processing to completed gives the shipped and completed orders
    # available status =  "processing", "packed", "shipped" , "completed", "cancelled"
    order_list = r.json()
    length = len(order_list)
    orders.extend(order_list)
    return pd.DataFrame(orders)


# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)
    item = ls.item_set.get(id=1)
    return render(response, "main/list.html", {"ls":ls})
   



def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method=="POST":
        if response.POST.get("newProduct"):
            n = response.POST.get("name")
            sku = response.POST.get("sku")
            p = response.POST.get("price")
            s = response.POST.get("sale_price")
            images = response.POST.get("images")
            c = response.POST.get("color_options")
            response.user.products.create(name=n, sku=sku, price=p, sale_price=s, images=images, color_options=c)

    return render(response, "main/create.html", {})

def product_list(response):
    wcapi = API(
        url="https://cantaistiyorum.com",
        consumer_key="ck_b62a5628ba155eda28d40c0857de5de7c96e9bde",
        consumer_secret="cs_daa346482eca9d5ca755744cefcb999d27216de2",
        version="wc/v3",
        query_string_auth=True,
        timeout=10
    )

    def get_simple_products():
        simple_df = pd.DataFrame()
        length = 1
        i=0
        while length!=0:
            r = wcapi.get("products", params={"per_page": 100, "page":i+1,"timeout":30})
            products = r.json()
            df = pd.DataFrame(products)
            length = len(df)
            if length!=0:
                df1 = df[(df["type"]=="simple") & (df["catalog_visibility"]=="visible")]
                simple_df = simple_df.append(df1)
            i=i+1
        return simple_df
    
    simple_products = get_simple_products().iloc[:100]
    def extract_color_options(product):
        attributes = product["attributes"]
        for attribute in attributes:
            try:
                if attribute["name"]=="Renk":
                    color_option = attribute["options"][0]
                product["color_option"] = color_option
            except:
                color_option = ""
                product["color_option"] = color_option
        return product
    
    def extract_dimensions(product):
        length = product["dimensions"]["length"]
        width = product["dimensions"]["width"]
        height = product["dimensions"]["height"]
        if width =="":
            product["width"] = 0
        else:
            product["width"] = float(width)
        if length =="":
            product["length"] = 0
        else:
            product["length"] = float(length)
        if height =="":
            product["height"] = 0
        else:
            product["height"] = float(height)
        
        return product

    def extract_simple_product_images(product):
        images = []
        for image in product["raw_images"]:
            image_src = image["src"]
            images.append(image_src)
        product["images"] = images
        return product

    def parse_text_from_html(product_description):
        html = product_description
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    
    def weight_check(product):
        if product["weight"]=="":
            product["weight"]= 0
        else:
            product["weight"]= float(product["weight"])
        return product

    simple_products["description"] = simple_products.apply(lambda x: parse_text_from_html(x["description"]),axis=1)
    simple_products = simple_products.apply(lambda x: extract_color_options(x),axis=1)
    simple_products = simple_products.apply(lambda x: extract_dimensions(x),axis=1)
    simple_products = simple_products.rename(columns={"images":"raw_images"})
    simple_products = simple_products.apply(lambda x: extract_simple_product_images(x),axis=1)
    simple_products = simple_products.apply(lambda x: weight_check(x) , axis=1)        
    simple_products = simple_products[["id","name","description","sku","price", "regular_price", "sale_price", "tax_status", "tax_class", "stock_quantity", "weight", "length","width","height", "images", "categories","color_option" ]]
    for i in range(30):
        first_product = simple_products.iloc[i]
        
        if response.user.products.filter(variation_id="0", main_id=first_product["id"]).exists():
            response.user.products.filter(variation_id="0", main_id=first_product["id"]).update(name=first_product["name"], description=first_product["description"],
                                    sku=first_product["sku"], price=float(first_product["regular_price"]),
                                    sale_price=float(first_product["sale_price"]),color_options=first_product["color_option"],
                                    quantity = first_product["stock_quantity"], weight= first_product["weight"],
                                    length = first_product["length"], height= first_product["height"],
                                    width = first_product["width"], images=first_product["images"]
                                    )
        else:                        
            response.user.products.create(name=first_product["name"], main_id=first_product["id"],
                                    variation_id="0", description=first_product["description"],
                                    sku=first_product["sku"], price=float(first_product["regular_price"]),
                                    sale_price=float(first_product["sale_price"]),color_options=first_product["color_option"],
                                    quantity = first_product["stock_quantity"], weight= first_product["weight"],
                                    length = first_product["length"], height= first_product["height"],
                                    width = first_product["width"], images=first_product["images"]
                                    )
        
        
        
    
    

    return render(response, "main/apps/customers/product_list.html", {})

def order_list(response):
    return render(response, "main/apps/customers/order_list.html", {})

def entegrasyon(response):
    return render(response, "main/entegrasyon.html", {})

def trendyol_integration(response):
    return render(response, "main/trendyol_integration.html", {})

def order_view(response,order_id):
    order = response.user.orders.get(order_id=order_id)
    return render(response, "main/order.html", {"order":order})

def product_view(response,id, variation_id):
    product = response.user.products.get(id=id, variation_id=variation_id)
    return render(response, "main/product.html", {"product":product})

def edit_product(response, id, variation_id):
    product = response.user.products.get(id=id, variation_id=variation_id)
    #return render(response, 'main/edit-product.html', {'form': QuillFieldForm(), "product":product})
    return render(response, "main/edit-product.html", {"product":product})

def woocommerce_integration(response):
    if response.method=="POST":
        if response.POST.get("newWoocommerce"):
            current_user = response.user
            api_key = response.POST.get("api_key")
            api_secret = response.POST.get("api_secret")
            website = response.POST.get("website")
            current_user.woocommerce_api_key = api_key
            current_user.woocommerce_api_secret = api_secret
            current_user.woocommerce_sitename = website
            current_user.save()

    return render(response, "main/woocommerce_integration.html", {})

def parasut_integration(response):
    if response.method=="POST":
        if response.POST.get("newParasut"):
            current_user = response.user
            parasut_firma_no = response.POST.get("parasut_firma_no")
            parasut_client_id = response.POST.get("parasut_client_id")
            parasut_client_secret = response.POST.get("parasut_client_secret")
            parasut_username = response.POST.get("parasut_username")
            parasut_password = response.POST.get("parasut_password")
            current_user.parasut_firma_no = parasut_firma_no
            current_user.parasut_client_id = parasut_client_id
            current_user.parasut_client_secret = parasut_client_secret
            current_user.parasut_username = parasut_username
            current_user.parasut_password = parasut_password
            current_user.save()
    return render(response, "main/parasut_integration.html", {})