# Pizzas API Python

This API manager storage, orders and types of pizzas.

### Tech Stack
* Python 3.10
* MongoDB

### First Step
* Install all packages in requirements.txt.
* Create an .env file and use the .env_example file as model.

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


Send request header, page size and values. To receive your Paginated data.
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

Send in your request header, a size value, and a value to page. To receive your Paginated data.

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

* Create an item in Store

Send in the body of your request, the item you want to create. Use the Store model for this.

```
http://localhost:8000/api/store/
```
* Get all item in Store

Send in your request header, a size value, and a value to page. To receive your Paginated data.

```
http://localhost:8000/api/store/
```
* Update a specific item in Store

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