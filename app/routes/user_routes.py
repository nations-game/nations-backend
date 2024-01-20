from flask import Blueprint, request, jsonify
from ..database import database_instance as database
from sqlalchemy.exc import IntegrityError

from ..utils.security import create_jwt_token, decode_jwt_token, verify_password
from ..database.models import User

user_endpoints: Blueprint = Blueprint(
    name="user_endpoints", 
    import_name=__name__, 
    url_prefix="/user"
)


# TODO: Create a user account.
@user_endpoints.route("/signup", methods=["POST"])
async def signup():
    # Get the data of the request
    register_data: dict = request.get_json()

    username = register_data.get("username")
    email = register_data.get("email")
    password = register_data.get("password")
    confirm_password = register_data.get("confirmPassword")
    accepted_terms = register_data.get("acceptedTerms")

    if accepted_terms != True:
        return jsonify({
            "status": "error", 
            "details": "Please accept the terms and conditions!"
        }), 401

    if password != confirm_password:
        return jsonify({
            "status": "error", 
            "details": "Passwords do not match!"
        }), 401

    
    user = await database.create_user_account(
        username=username,
        email=email,
        password=password
    )

    if  isinstance(user, User):
        token = create_jwt_token(user.id)

        return jsonify({
            "status": "success",
            "details": user.to_dict(),
            "token": token
        }), 200
    else:
        return jsonify({
            "status": "error",
            "details": user
        }), 400

# TODO: Log in.
@user_endpoints.route("/login", methods=["POST"])
async def login():
    login_data: dict = request.get_json()
    email = login_data.get("email")
    password = login_data.get("password")

    user = await database.get_user_by_email(email)

    if user and verify_password(password, user.salted_password, user.hashed_password):
        token = create_jwt_token(user.id)
        return jsonify({
            "status": "success",
            "details": user.to_dict(),
            "token": token
        })
    else:
        return jsonify({
            "status": "error",
            "details": "Invalid email or password!"
        }), 401

# TODO: Returns data about a specified user, or if none is specified, the current logged-in user. Requires authorization.
@user_endpoints.route("/info", methods=["GET"])
async def user_data():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"status": "error", "details": "Authorization token missing"}), 401

    user_id = decode_jwt_token(token)

    if request.get_json().get("user_id") != None:
        user_id = request.get_json().get("user_id")

    if user_id is not None:
        user = await database.get_user_by_id(user_id)
        if user:
            user_details = user.to_dict()
            del user_details["email"]
            return jsonify({
                "status": "success",
                "details": user.to_dict()
            })
    return jsonify({"status": "error", "details": "Invalid or expired token"}), 401