# basic_backend.py
items = list()  # global variable where we keep the data

def create_items(app_items):
    global items
    items = app_items

def create_item(name, price, quantity):
    global items
    items.append({'name': name, 'price': price, 'quantity': quantity})
    
def read_item(name):
    global items
    myitems = list(filter(lambda x: x['name'] == name, items))
    return myitems[0]

def read_items():
    global items
    return [item for item in items]

