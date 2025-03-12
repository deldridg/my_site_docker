
from django.shortcuts import render
from django.http import HttpResponse

from datetime import date
import pandas as pd

#---------- Grabbing/displaying blog posts from Excel ----------

# Read the Excel file
file_path = "blog/data/data.xlsx"
sheet_name = "Data"

def load_excel_data(file_path, sheet_name):
    # Load Excel file into a pandas DataFrame
    data_frame = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Convert the 'date' column to date objects if it exists
    if 'date' in data_frame.columns:
        data_frame['date'] = pd.to_datetime(data_frame['date']).dt.date

   # Convert DataFrame to list of dictionaries
    data = data_frame.to_dict(orient='records')
    
    # Manually handle line breaks in text fields
    for record in data:
        for key, value in record.items():
            if isinstance(value, str):
                record[key] = value.replace('\n', '\r\r')

    return data

def sort_posts_by_date(posts):
    # Sort the list of dictionaries by the 'date' key
    sorted_posts = sorted(posts, key=lambda x: x.get('date', date.min))
    
    return sorted_posts

all_posts = load_excel_data(file_path, sheet_name)
# all_posts = sort_posts_by_date(posts)

myStr = ""

for i in all_posts:
    for key, value in i.items():
        myStr += f"<p><b>{key}</b>: {value}</p>"

myStr += "<p>" + str(type(all_posts)) + "</p>"

# Output contents of the dataList to /data
def show_data(request):
    return HttpResponse(myStr)

def get_date(post):
    return post['date']

#---------------------------------------------------------------

# Create your views here.
#posts = data_frame.to_dict(orient="records")

def starting_page(request):
    sorted_posts = sorted(all_posts, key=get_date)
    latest_posts = sorted_posts[-3:]
    return render(request, "blog/index.html", {
        "posts": latest_posts
    })

def posts(request):
    return render(request, "blog/all-posts.html", {
        "all_posts": all_posts
    })

def post_detail(request, slug):
    post = next(post for post in all_posts if post['slug'] == slug)
    return render(request, "blog/post-detail.html", {
        "post": post
    })

