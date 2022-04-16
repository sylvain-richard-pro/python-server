# Python server to manage events

## Introduction to Python server

Constraint: use a Mongo database.

Endpoints:
* `/add_event`
* `/list_events`
* `/remove_events`
 
An event has:
* A start (epoch).
* An optional stop.
* tags (strings).

This Python Server is based on flask framework.


## Prerequisites

- Python 3
> Note: Tested on python3.10

- A mongodb server is necessary to store events.


## Installation

### Download project

```bash
git clone <url>...
```


### Prepare your virtual env

It's advice to use a python virualenv.
```bash
cd $youDirectory
python3 -m venv env1
env1/bin/python -m pip install -r requirements.txt
```

### Config your Mongodb connection string

Update the YAML config file config.yml 
```bash
cat config.yml 
#set your Mongodb connection string
mongodb_url: "localhost:27017"
```

### Start the python server

> This code is just given as an example.
> Mode development: Do not use this for PRODUCTION.

```bash
cd $youDirectory
. env1/bin/activate
./runServerFlask.sh
```

## Usage

3 Endpoints are available.

adapted to your Url. Sample are provide with "http://127.0.0.1:5000"

1. Add event (POST)
> "tags" array must be adapted to your needs.
```
cat postrequest_tags.json
{
    "tags": [
        "pyclient A",
        "Rest API"
    ]
}
```
```bash
curl -d @postrequest_tags.json -H "Content-Type: application/json" http://127.0.0.1:5000/add_event
```
response sample
```bash
{
    "_id": "625ac1d2e8f5d327aa51e4e0", 
    "body": {
        "tags": [
            "pyclient A", 
            "Rest API"
        ]
    }, 
    "message": "This endpoint should create an event in db", 
    "method": "POST"
}
```

2. List all events (GET)
```bash
curl -v -H "Content-Type: application/json" http://127.0.0.1:5000/list_events
```
response sample
```bash
{
    "array_events": "[{'_id': ObjectId('625aaa453fc83c15582e6eba'), 'start_epoch': 1650108997.5920792, 'stop_epoch': -1, 'tags': ['pyclient A', 'Rest API']}, {'_id': ObjectId('625ac1d2e8f5d327aa51e4e0'), 'start_epoch': 1650115026.325763, 'stop_epoch': -1, 'tags': ['pyclient A', 'Rest API']}]", 
    "message": "This endpoint list all events in db", 
    "method": "GET"
}```

3. Remove all events or just some
 - just some
> "start_epoch_array" array must contain each start_epoch value that you want to remove.
```
cat postrequest_start_epoch_array.json
{
    "start_epoch_array": [1650059272.843029, 1650101244.100029]
}
```
```bash
curl -d @postrequest_start_epoch_array.json -H "Content-Type: application/json" http://127.0.0.1:5000/remove_events
```
response sample
```bash
{
    "body": {
        "start_epoch_array": [
            "1650059272.843029",
            "1650101244.100029"
        ]
    }, 
    "message": "This endpoint should remove events in db", 
    "method": "POST", 
    "start_epoch_array_deleted": "['1650101244.100029']",
    "start_epoch_array_not_deleted": "['1650059272.843029']"  <-- this event does not exist
}
```

 - all events
 > use "purge" property. (may be cumulative, "purge" takes priority.)
```
cat postrequest_purge_all_events.json
{
  "purge": true,
  "start_epoch_array": ["1650059272.843029", "1650101244.100029"]
}
```
```bash
curl -d @postrequest_purge_all_events.json -H "Content-Type: application/json" http://127.0.0.1:5000/remove_events
```
response sample
```bash
{
    "body": {
        "purge": true, 
        "start_epoch_array": [
            "1650059272.843029", 
            "1650101244.100029"
        ]
    }, 
    "message": "This endpoint should remove events in db (purge all events)", 
    "method": "POST", 
    "result": "all events are removed"
}```

<br />

> For more information, use docstring.
```bash
cd $youDirectory
. env1/bin/activate
python
>>> import server
>>> help(server)
[CTRL+C]
```


## CLI

You should use CLI to test events feature [CLI Documentation](https://github.com/sylvain-richard-pro/python-server/tree/master/cli).


<br />
<br />
<br />
