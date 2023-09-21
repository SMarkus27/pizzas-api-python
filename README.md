# Pizzas API Python

This API manages storage, orders, and types of pizzas.

### Tech Stack
* Python 3.10
* MongoDB

### First Step
* Creates a virtual environment for the project.
```
python -m venv venv
```
* Install all packages in requirements.txt.
```
pip install -r requirements.txt
```
* Creates a .env file and uses the .env_example file as a model.

### Running the API
```
python main.py
```

### How to use the API

### Pizza Routes
#### Pizza Model

```
{
    "name": str,
    "price": float,
    "ingredients": [str, str]
}
```

* Creates a pizza

Send in the request body, and the pizza type. Use the Pizza model.

```
http://localhost:8000/api/pizzas/
```
* Get all Pizzas


Send request header, page size, and values. To receive your Paginated data.
```
http://localhost:8000/api/pizzas/
```
* Get a specific pizza

```
http://localhost:8000/api/pizzas/pizza_name
```
* Update a pizza

Send the pizza data you want to update in the body of your request. Use the Pizza model for this.
```
http://localhost:8000/api/pizzas/pizza_name
```

* Delete a pizza
```
http://localhost:8000/api/pizzas/pizza_name
```
### Orders Routes

#### Orders Model
```
{
    "name": str,
    "quantity": int
}
```

* Create an order
Send the order you want to create in the body of your request. Use the Order model for this.
```
http://localhost:8000/api/pizzas/pizza_name
```
* Get all orders

Send in your request header, a size value, and a value to the page. To receive your Paginated data.

```
http://localhost:8000/api/pizzas/pizza_name
```
* Get a specific order
```
http://localhost:8000/api/pizzas/pizza_name
```
### Store Routes

#### Store Model
```
{
    "name": str,
    "quantity": int
}
```

* Create an item in the Store

Send the item you want to create in the body of your request. Use the Store model for this.

```
http://localhost:8000/api/store/
```
* Get all items in the Store

Send in your request header, a size value, and a value to the page. To receive your Paginated data.

```
http://localhost:8000/api/store/
```
* Update a specific item in the Store

Send the data of the store item you want to update in the body of your request. Use the Store model for this.

```
http://localhost:8000/api/store/
```

### API Swagger 
* You can access all API routes and also test all API functionalities.
```
http://localhost:8000/docs
```

### Tests
Building

#### License

This project is under license [MIT](/LICENSE).