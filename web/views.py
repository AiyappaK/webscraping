import requests
from django.shortcuts import render,redirect
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from  . import models

base_url = 'https://bangalore.craigslist.org/search/?query={}'
base_img_url='https://images.craigslist.org/{}_300x300.jpg'

def index(request):

    return render (request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    
    models.Search.objects.create(search=search)
    
    final_url = base_url.format(quote_plus(search))
    
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features = 'html.parser')
    post_listing = soup.find_all('li',{'class':'result-row'})

    final_post = []
    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'n/a'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = base_img_url.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_post.append((post_title , post_url, post_price , post_image_url))
    

    frontend = {'search': search, 'final_post' : final_post}
    return render(request , 'my_app/new_search.html', frontend)