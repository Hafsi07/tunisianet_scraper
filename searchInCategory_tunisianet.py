from bs4 import BeautifulSoup as bs 
from urllib.request import urlopen
import json 
import os
import re


# url="https://www.tunisianet.com.tn/438-reseau"
# min=0
# max=99999

def updater(link,minimum,maximum ): 
    '''
    This function updates the values from a calling program 
    '''
    url=link
    min=minimum
    max=maximum

def get_price(item): 
    '''
    This function converts the price from the pade to a usable int in millimes
    '''
    ch=""
    i=0
    while item[i].isnumeric() or item[i]=="," or item[i]==" " or item[i]==" ":
        if not item[i]==",":    
            ch=ch+item[i]
        i+=1
    return int(ch)

def page_reader(url): 
    '''
    This module reads the page and grabs the necessary details of products in that page
    '''
    print(url,"  heh")
    u=urlopen(url)
    
    page=u.read()
    u.close()
    thepage=bs(page,"html.parser")  

    productnames=[]
    productdescs=[]
    productlinks=[]
    productprices=[]


    #product names 
    pcs=thepage.find_all("div",{"class":"wb-product-desc product-description col-lg-5 col-xl-5 col-md-6 col-sm-6 col-xs-6"})
    print(len(pcs),"  heh")
    for pc in pcs: 
        productnames.append(pc.h2.text)

    #product description 
    one=thepage.find_all("div",id=re.compile("product-description-short"))
    # one=one[1:25]
    print(len(one))
    for desc in one:
        productdescs.append(desc.text)

    #product links 
    links=thepage.find_all(["h2"],class_="h3 product-title")
    for link in  links:
        productlinks.append(link.a["href"])

    #prices
    prics=thepage.findAll( "span",{"itemprop":"price"})
    prices=[]
    for i in  range(0,len(prics),2): 
        prices.append(prics[i] )
    for price in prices: 
        productprices.append(price.text)

    items={"products":[]}
    print(len(links),"lenth")
    for i in range(len(links)): 
        fucks={}
        fucks["product_name"]=productnames[i]
        fucks["product_description"]=productdescs[i]
        fucks["product_link"]=productlinks[i]
        fucks["product_price"]=productprices[i]
        items["products"].append(fucks)
    print(len(items["products"]),"  fel page reader")
    return items

def searchByPrice(items,minne,maxxe):
    '''
    Search in products considering a price range
    '''
    products={"products":[]}
    for item in items["products"]: 
        produits={}
        if get_price(item["product_price"]) in range(minne,maxxe): 
            produits["product_name"]=item["product_name"]
            produits["product_description"]=item["product_description"]
            produits["product_link"]=item["product_link"]
            produits["product_price"]=item["product_price"]
            products["products"].append(produits)
    return(products)

def dumper(hh,filename): 
    '''
    dumps the results of search in a json file 
    '''
    newdata=hh
    print(len(hh["products"])," right b4 dumping")
    try: 
        f=open(filename+'.json') 
    except: 
        print("Data file just created ! ")
        f=open(filename+'.json',"w")      
        f.close()
        f=open(filename+'.json') 

    # else: 
    finally:
        if (not(os.path.getsize(filename+'.json') == 0)):
            data=json.load(f)
            f.close()
            l=data["products"]
            for i in hh["products"]: 
                l.append(i)
            # print(len(l))
            newdata={"products":l}
        else: l=hh
        f=open(filename+'.json','w') 
        json.dump(newdata,f,indent=2) 
        f.close()
    

# dumper(page_reader(url),"jisonn")