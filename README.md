# Inventory Item Tracker
This is a simple HTTP Flask web application that stores an inventory table in a SQLite database. The database can be accessed and and modified with standard CRUD operations and allows searching for items with various filters.

## Setup
Open up a unix terminal and clone the git repo and move into it:
```
git clone https://github.com/sergmister/Inventory-Intern-Challenge
cd Inventory-Intern-Challenge
```
Ensure you have Python 3 and curl installed on your system and are available in your PATH environment variable. Install the Flask library with the following command:
```
python3 -m pip install -U flask
```
Finally, initialize the database before running the application with the following command:
```
python3 init_db.py
```

## Using the server
To start the server run:
```
python3 -m flask run
```
This should start the server on `http://127.0.0.1:5000/`

We can then test the server with an API testing utility of your choice. For this tutorial we will use the ubiquitous `curl` command. Run the following in a separate terminal:
```
curl -s --header "Content-Type: application/json" -X POST \
    -d '{"ID": "nail", "Description": "A fastener to hold together pieces of wood."}' \
    http://127.0.0.1:5000/create_item
```
You should see response like this `{"success":true}`. If we run the command again we will get `{"success":false}`. This is because for the most part, our operations are idempotent, meaning subsequent applications of the same command will have no effect. In this case, the `ID` field of an item must be unique, so trying to add another item with the same ID will result in a failure.

Let's add a hammer item:
```
curl -s --header "Content-Type: application/json" -X POST \
    -d '{"ID": "hammer", "Description": "A tool used to put in nails."}' \
    http://127.0.0.1:5000/create_item
```

We can get a list of items in json format with the following command:
```
curl -s --header "Content-Type: application/json" -X GET \
    -d '{}' \
    http://127.0.0.1:5000/get_items
```
(You can add ` | json_pp -json_opt pretty,canonical` to the end of the command to print the json in a more readable format if your system has the `json_pp` utility, as most unix based (linux, macos), systems do.)

The search request can have various filters applied to it. For example the following command will find all items that have `fastener` in the description and where added on or after January 2, 2022.
```
curl -s --header "Content-Type: application/json" -X GET \
    -d '{"Description_match": "fastener", "Date_after": "2022-01-02"}' \
    http://127.0.0.1:5000/get_items
```

Search filters include:
- `ID` - Find an item with the exact ID.
- `Description_match` - Find items which contain this word(s) in their description.
- `Date_after` - Find items added on or after this date.
- `Date_before` - Find items added on or before this date.
- `Quantity_min` - Find items with a quantity greater than or equal to this value.
- `Quantity_max` - Find items with a quantity less than or equal to this value.

We update the hammer item by adding 1 to its quantity as follows:
```
curl -s --header "Content-Type: application/json" -X PATCH \
    -d '{"ID": "hammer", "Quantity_change": 1}' \
    http://127.0.0.1:5000/update_item
```

Update modifiers include:
- `Quantity` - Set the item's quantity to this value.
- `Quantity_change` - Change the item's quantity by this value.
- `Description` - Set the item's description to this value.

Finally, to delete an item use the following command:
```
curl -s --header "Content-Type: application/json" -X DELETE \
    -d '{"ID": "hammer"}' \
    http://127.0.0.1:5000/delete_item
```