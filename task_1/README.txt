# Backend assignment for ~REDACTED~
~REDACTED~

Instructions:
- Install requirements,
- Start the server like any other django server,
- Run migrations.

pip install -r requirements.txt
./manage.py migrate
./manage.py runserver

The server supports the following API:

POST "/auth/"
    {"username":"admin","password":"12345678"}
    Returns a token

GET "/orders/"
    Returns list of orders for current user (requires auth token)

GET "/products/[?page=PAGE]"
    Returns a paged list of products (public)

POST "/orders/"
    {"product":1,"quantity":2}
    Creates an order as the logged user (requires auth token)
