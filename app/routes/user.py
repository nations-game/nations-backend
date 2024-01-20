from flask import Blueprint

user_endpoints: Blueprint = Blueprint(
    name="user_endpoints", 
    import_name=__name__, 
    url_prefix="/user"
)

@user_endpoints.route("/signup")
async def signup():
    ...

@user_endpoints.route("/login")
async def login():
    ...