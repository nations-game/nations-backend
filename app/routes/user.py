from flask import Blueprint, Request, request

user_endpoints: Blueprint = Blueprint(
    name="user_endpoints", 
    import_name=__name__, 
    url_prefix="/user"
)

@user_endpoints.route("/signup")
async def signup():
    data: Request = request.data
    ...

@user_endpoints.route("/login")
async def login():
    ...
