# CLI to manage events

## Context
Events are managed by the ["Python server" (python WebAPI) ](https://github.com/sylvain-richard-pro/python-server/tree/master/flaskServer)

CLI are command to be used in a Linux distribution.

## Prerequisites

- Linux Curl package installed.
- Python Server are online and available.
- URL of the API python Server

## Installation

### Download project

```bash
git clone <url>...
```

<!--
### Prepare your virtual env

It's advice to use a python virualenv.
```bash
cd $youDirectory
python3 -m venv env1
env1/bin/python -m pip install -r requirements.txt
```
-->

## Configure URL

adapted to your Url. Sample are provide with "http://127.0.0.1:5000"

Set the URL
```bash
vi setenv 
#set with your appropriate value
URL_PYTHON_SERVER="<changeThisValue>"
```

## Usage

3 Command lines are available.

> These commands are just curl wrapper.



1. Add event (POST)

```bash
#use defaut tags
./event_add.sh
#use a specific tags
./event_add.sh '{"tags": ["CLI Wrapper","TWO","THREE"]}'
```
output
```bash
--------------------------------------------------
{
  "_id": "625ae0ebe8f5d327aa51e501", 
  "body": {
    "tags": [
      "CLI Wrapper", 
      "TWO", 
      "THREE"
    ]
  }, 
  "message": "This endpoint should create an event in db", 
  "method": "POST"
}
--------------------------------------------------
HTTP_CODE=200
-I- add event done.
```

2. List all events (GET)

```bash
./event_list.sh
```
output
```bash
--------------------------------------------------
{
  "array_events": "[{'_id': ObjectId('625ae0ebe8f5d327aa51e501'), 'start_epoch': 1650122987.679289, 'stop_epoch': -1, 'tags': ['CLI Wrapper', 'TWO', 'THREE']}]", 
  "message": "This endpoint list all events in db", 
  "method": "GET"
}
--------------------------------------------------
HTTP_CODE=200
-I- list events display done.
```

3. Remove all events or just some

 - just some

> "start_epoch_array" array must contain each start_epoch value that you want to remove.
```bash
./event_remove.sh '{"start_epoch_array": ["1650059272.843029", "1650101244.100029"]}'
```

output
```bash
--------------------------------------------------
{
  "body": {
    "start_epoch_array": [
      "1650059272.843029", 
      "1650101244.100029"
    ]
  }, 
  "message": "This endpoint should remove events in db", 
  "method": "POST", 
  "start_epoch_array_deleted": "[]",         <-- Note: Here, no event are deleted.
  "start_epoch_array_not_deleted": "['1650059272.843029', '1650101244.100029']"
}
--------------------------------------------------
HTTP_CODE=200
-I- remove events done.
```

 - all events
 
> use "purge" property. (may be cumulative, "purge" takes priority.)
```bash
./event_remove.sh '{"purge": true}'
```

output
```bash
--------------------------------------------------
{
  "body": {
    "purge": true
  }, 
  "message": "This endpoint should remove events in db (purge all events)", 
  "method": "POST", 
  "result": "all events are removed"
}
--------------------------------------------------
HTTP_CODE=200
-I- remove events done.
```


<br />



## CLI sample
```bash
# add events
./event_add.sh '{"tags": ["CLI Wrapper","Bob"]}'
./event_add.sh '{"tags": ["CLI Wrapper","Bill"]}'
./event_add.sh '{"tags": ["CLI Wrapper","foo"]}'

# list events
./event_list.sh

# purge all events
./event_remove.sh '{"purge": true}'
# or only some
./event_remove.sh '{"start_epoch_array": ["1650059272.843029", "1650101244.100029"]}'
```

<br />
<br />
<br />



