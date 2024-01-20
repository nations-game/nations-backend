from flask import Blueprint, Request, request

user_endpoints: Blueprint = Blueprint(
    name="user_endpoints", 
    import_name=__name__, 
    url_prefix="/user"
)

# TODO: Create a user account.
@user_endpoints.route("/signup", methods=["POST"])
async def signup():
    data: Request = request.data
    ...

# TODO: Log in.
@user_endpoints.route("/login", methods=["POST"])
async def login():
    ...

# TODO: Returns data about a specified user, or if none is specified, the current logged-in user. Requires authorization.
@user_endpoints.route("/info", methods=["GET"])
async def user_data():
    ...
