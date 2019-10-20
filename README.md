# ZSSN (Zombie Survival Social Network)


> Version: 1.0


## Description
A zombie apocalypse is just happening and the humans are running out of resources. They need a way to share resources among them in order to survive. 
This is a REST API developed to help them store information about the survivors, as well as the resources they own.


## Requirements
### Core

* Python (3.6.6 used) - https://www.python.org/
* Django (2.2.6) - https://www.djangoproject.com/
* Django Rest Framework (3.10.3) - https://www.django-rest-framework.org/


## Features

- **Add survivors**
- **Update survivor location**
- **Flag survivor as infected**
- **Trade items**
- **Reports**
    1. Infected survivors.
    2. Non-infected survivors.
    3. Resource by survivor
    4. Points lost by infected survivor.


## Set up the application

Install Python dependencies:

    pip install -r requirements.txt
    
Create migrations of the models:
    
    python manage.py makemigrations zssn

Apply migrations to the database:

    python manage.py migrate
    
Run the server:

    python manage.py runserver
   
   
## Routes

### Survivors

**GET** `/survivors/` to retrieve all registered survivors.

**GET** `/survivors/{id}` to retrieve a specific survivor.

**POST** `/survivors/` to register a new survivor.
```
{
    "name": "Survivor Name",
    "age": 20,
    "gender": "M",
    "last_location": {
          "latitude":24325.09,
          "longitude":-56456
          }
    "inventory": {
          "water:2,
          "food":3,
          "med":5,
          "ammo":8,
          }
}
```

* name - Name of the survivor.
* age - Age of the survivor.
* gender - Gender of the survivor (can be male'M' or female'F').
* [location] - Latitude and longitude of the last location of the survivor.
* inventory - Items that this survivor holds.

**POST** `/survivors/{id}/last_location` to update a survivor location.
```
{
    "latitude": -14235.9080,
    "longitude: 346454.234
}
```

* latitude - New latitude of the survivor.
* longitude - New longitude of the survivor.

**POST** `/survivors/{id}/trade` to trade items.
```
{
    "buyer_id": 3,
    "pick_water": 4,
    "pick_food": 3,
    "pick_med": 2,
    "pick_ammo": 4,
    "offer_water": 5,
    "offer_food": 7,
    "offer_med": 8,
    "offer_ammo": 2
}
```

* id - Survivor that's receiving the deal.
* buyer_id - Survivor that's issuing the deal.
* offer - Items that the buyer is offering in exchange.
* pick - Items that the buyer wishes to obtain.

**POST** `/survivors/{id}/flag` to flag a survivor as infected.
```
{
    "flagged_id": 0
}
```

* id - Survivor that's flagging.
* flagged_id - Survivor that's going to be flagged as infected.

### Inventory

**GET** `/survivors/{id}/inventory` to retrieve a survivor's inventory.

### Reports

**GET** `/reports/infected` the percentage of survivors infected by the virus.

**GET** `/reports/non_infected` the percentage of healthy survivors.

**GET** `/reports/average_resource` the average amount of each kind of resource by survivor.

**GET** `/reports/points_lost` the amount of points lost because of the infected.



## Running Tests

You can run some automated tests to check the functionalities by running the command below:

    python manage.py zssn.tests
    
