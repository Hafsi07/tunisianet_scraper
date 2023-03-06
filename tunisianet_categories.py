from bs4 import BeautifulSoup as bs 
from urllib.request import urlopen
from searchInCategory_tunisianet import page_reader,dumper
def souper(url):
    '''
    Gets the page soup to extract data from 
    '''
    w=urlopen(url)
    page=w.read()
    w.close() 
    return bs(page,"html.parser") 

#all  the categories 
def pager(soup):
    '''
    returns the categories of the page 
    '''
    pp=soup.find_all("li",{"class":"menu-item item-line"})
    # print(pp)
    cats=[]
    for categ in pp: 
        cats.append(categ.a["href"])
    print(len(cats),"  ", cats[0],"--",cats[1],"--")
    return cats 

def lister(cat):
    '''
    for every category it enlists all the product pages to take the data from 
    '''
    filee="tunisianetwholedata"
    subcats=[]
    for i in cat: 
        page=souper(i)
        elements=page.find("ul",{"class":"page-list clearfix"})
        if elements==None: 
            dumper(page_reader(link),filee)
        else:
            link=elements.li.a["href"]
            pagesnumber=int(elements.find_all("a")[-2].text) #number of pages in the category
            for i in range(1,pagesnumber+1):
                dumper(page_reader(link+"?page="+str(i)),filee)
            
        
        
        
4
# print(souper("https://www.tunisianet.com.tn/"))
lister(pager(souper("https://www.tunisianet.com.tn/")))