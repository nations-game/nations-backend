from flask import Blueprint, request, jsonify
from ..database import database_instance as database

from ..utils.security import decode_jwt_token
from ..database.models import User, Nation

nation_endpoints: Blueprint = Blueprint(
    name="nation_endpoints", 
    import_name=__name__, 
    url_prefix="/nation"
)

# TODO: Creates a nation. Sets a name, flag, etc.
@nation_endpoints.route("/create", methods=["POST"])
def create():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"status": "error", "details": "Unauthorized"}), 401

    user_id = decode_jwt_token(token)
    user: User
    if user_id is not None:
        user = database.get_user_by_id(user_id)
    else:
        return jsonify({"status": "error", "details": "Bad authorization token."}), 401
    
    if user.nation_id != None:
        return jsonify({"status": "error", "details": "User already has a nation."}), 400
    
    request_data: dict = request.get_json()

    name = request_data.get("name")
    system = request_data.get("system")
    
    nation = database.create_nation(
        user=user,
        name=name,
        system=system
    )

    if  isinstance(nation, Nation):
        return jsonify({
            "status": "success",
            #"details": nation.to_dict()
        }), 200
    else:
        return jsonify({
            "status": "error",
            "details": nation
        }), 400

# Returns data of nation belonging to logged in user.
@nation_endpoints.route("/info", methods=["GET"])
def nation_data():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"status": "error", "details": "Authorization token missing"}), 401

    nation_id: int

    if request.get_json().get("nation_id") != None:
        nation_id = request.get_json().get("nation_id")
    else:
        user_id = decode_jwt_token(token)
        user = database.get_user_by_id(user_id)

        if user is not None:
            if user.nation_id is None:
                return jsonify({"status": "error", "details": "User does not have a nation."}), 401
            nation_id = user.nation_id
        else:
            return jsonify({"status": "error", "details": "Bad authorization token."}), 401

    if nation_id is not None:
        nation = database.get_nation_by_id(nation_id)
        if nation:
            return jsonify({
                "status": "success",
                "details": nation
            })
    return jsonify({"status": "error", "details": "Invalid or expired token"}), 401

# Get the factories of the logged-in user's nation.
@nation_endpoints.route("/factories", methods=["GET"])
def get_factories():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"status": "error", "details": "Authorization token missing"}), 401

    nation_id: int

    user_id = decode_jwt_token(token)
    user = database.get_user_by_id(user_id)

    if user is not None:
        if user.nation_id is None:
            return jsonify({"status": "error", "details": "User does not have a nation."}), 401
        nation_id = user.nation_id
    else:
        return jsonify({"status": "error", "details": "Bad authorization token."}), 401

    if nation_id is not None:
        factories = database.get_nation_factories(nation_id)
        print(factories)
        return jsonify(factories)