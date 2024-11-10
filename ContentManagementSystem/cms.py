from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from ContentManagementSystem.auth import login_required
from ContentManagementSystem.db import get_db
from ContentManagementSystem.mongodb import mongoConnection
import pymongo
import pandas as pd

cms = Blueprint('cms', __name__)

@cms.route('/')
def index():
    # posts = ['a', 'abshbdia', 'adigaid ']
    return render_template('cms/index.html')

# uploading the csv function
@cms.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        file_upload_msg = {}
        try:
            mongo = mongoConnection()
            client= mongo.create_connection () 

            db = client['marrowDB']
            collection = db['movie'] 

            # upload file flask
            f = request.files.get('file')
            df = pd.read_csv(f)
            data = df.to_dict(orient='records')

            collection.insert_many(data)
            # collection.delete_many({})
            file_upload_msg['status'] = 0

            return render_template("cms/index.html", file_upload_msg=file_upload_msg)
        except Exception as e:
            file_upload_msg['status'] = 1
            print(e)
            return render_template("cms/index.html", file_upload_msg=file_upload_msg)


# Fetching the data to list with pagination and sort 
@cms.route('/list', methods=['GET'])
def listData():
    try:
        page = int(request.args.get('page',1))
        sortby = request.args.get('sortby','date_added')
        per_page = 10
        mongo = mongoConnection()
        client= mongo.create_connection () 
        db = client['marrowDB']
        collection = db['movie'] 
        filter = {}
        skip_count = (page - 1)* per_page
        print(skip_count)

        # movie_list = collection.find(filter).sort(('release_year'),1).skip(skip_count).limit(per_page)
        # movie_list = collection.find(filter).sort(('date_added'),1).skip(skip_count).limit(per_page)
        # movie_list = collection.find(filter).sort(('duration'),1).skip(skip_count).limit(per_page)

        movie_list = collection.find(filter).sort((sortby),1).skip(skip_count).limit(per_page)
        print(type(movie_list), movie_list)
        total_count = collection.count_documents({})
        return render_template("cms/listingPage.html", movie_list=movie_list, page = page, total_count = total_count, sort=sortby)    
    except Exception as e:
        print('except')
        print(e)
    
