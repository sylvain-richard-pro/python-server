#!/Users/sylvain/Documents/dev/bioSerenity/flaskServer/venv/bin/python3

import sys, time, json
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint


#open config file  (REM: need pyYaml in Python3)
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
#client = MongoClient(port=27017)
try:
    #get cfg
    conn_str_mongodb = cfg["mongodb_connection_string"]
    #init conn
    client = MongoClient(host = conn_str_mongodb, serverSelectionTimeoutMS = 3000)
    print(client)
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    raise

db = client.dbEvent


# main.py
from flask import Flask, request, abort, Response

# Create the flask app
app = Flask(__name__)

@app.route('/add_event', methods=['POST'])
def add_event():
    """Add event
attr:
    mandatory: tags (array)
                  
body.request
    {
  "tags": [
    "pyclient A",
    "Rest API"
  ]
}"""
    if request.method == "POST":
        # get tags from request.json
        #print(type(request.json))  #dict
        #print(repr(request.json))
        if request.content_type != 'application/json':
            abort(403, description='Invalid content-type. Must be application/json.')
        if (request.content_type.startswith('application/json')):
            try:
                tags=request.json['tags']
            except KeyError:
                abort(400, description="tags Array is mandatory.")

            if type(tags) is not list:
                abort(400, description="tags invalid format, must be an Array.")
        
        #add event to db         
        curEvent={ "start_epoch": time.time(), "stop_epoch": -1, "tags": tags }
        result=db.myCollectionEvent.insert_one(curEvent)

        #Print to the console the ObjectID of the new document
        print('-I- Event Created "_id" : ObjectId("{0}")'.format(result.inserted_id))

        # body_response = {
        #     'message': 'This endpoint should create an event in db',
        #     'method': request.method,
        #     'body': request.json,
        #     '_id': str(result.inserted_id)
        # }

 #       return Response(json.dumps(body_response)+"\n", status=201, mimetype='application/json')

        return {
            'message': 'This endpoint should create an event in db',
            'method': request.method,
            'body': request.json,
            '_id': str(result.inserted_id)
        }, 201, {'ContentType':'application/json'}



@app.route('/list_events', methods=['GET'])
def list_events():
    """List events from db

body.response
{
  "array_events":[
    {"_id": "6259e8e0cdb7edce8762c0c3", "start_epoch": 1650059488.691395, "stop_epoch": -1, "tags": ["pyclient A", "onebyone"]},
    {"_id": "625a86b66b193bca91c37317", "start_epoch": 1650099894.0093179, "stop_epoch": -1, "tags": ["pyclient A", "Rest API"]}
]
}"""
    if request.method == "GET":

        #get events from db
        result=db.myCollectionEvent.find()
        #show in console
        res=[]
        for i in result:
            print(i)
            res.append(i)

        #response    
        return {
            'message': 'This endpoint list all events in db',
            'method': request.method,
            'array_events': repr(res)
        }, 200, {'ContentType':'application/json'}




@app.route('/remove_events', methods=['POST'])
def remove_events():
    """Remove events from array from start_epoch

attr:
    mandatory: start_epoch_array (array)

body.request
{
  "start_epoch_array": [1650059272.843029, 1]
}

and/or

for purge all events
attr:
    optional: purge (boolean) 

body.request
{
  "purge": true
}

""" 

    if request.method == "POST":
        #control
        if request.content_type != 'application/json':
            abort(403, description='Invalid content-type. Must be application/json.')

        if (request.content_type.startswith('application/json')):
            try:
                purge_events = request.json['purge']
                if purge_events is True:
                    try:
                        db.myCollectionEvent.drop()
                    except Exception as err:
                        print(f"Unexpected {err=}, {type(err)=}")
                        abort(500, description="Error during purge process.")

                    print("-I- all events removed")
                    return {
                        'message': 'This endpoint should remove events in db (purge all events)',
                        'method': request.method,
                        'body': request.json,
                        'result': 'all events are removed'
                    }, 200, {'ContentType':'application/json'}

            except KeyError:
                # continue with 'start_epoch_array'
                pass

            
            try:           
                start_epoch_list = request.json['start_epoch_array']
            except KeyError:
                abort(400, description="start_epoch_array must by defined.")

            if type(start_epoch_list) is not list:
                abort(400, description="start_epoch_array invalid format, must be an Array.")
        
 
        #start_epoch_list=[ 1650059272.843029, 1]

        start_epoch_array_deleted=[]
        start_epoch_array_not_deleted=[]

        for start_epoch_value in start_epoch_list:
            result = db.myCollectionEvent.delete_many( {'start_epoch': float(start_epoch_value) } )
            if result.deleted_count == 1:
                print('-I- Event Removed {0} , raw_result: {1} , "start_epoch": {2} '.format(result.deleted_count, result.raw_result['n'], str(start_epoch_value)))
                start_epoch_array_deleted.append(start_epoch_value)
            else:
                print('-W- No Event Removed {0} , raw_result: {1} , "start_epoch": {2} '.format(result.deleted_count, result.raw_result['n'], str(start_epoch_value)))
                start_epoch_array_not_deleted.append(start_epoch_value)


        return {
            'message': 'This endpoint should remove events in db',
            'method': request.method,
            'body': request.json,
            'start_epoch_array_not_deleted': repr(start_epoch_array_not_deleted),
            'start_epoch_array_deleted': repr(start_epoch_array_deleted)            
        }, 200, {'ContentType':'application/json'}

