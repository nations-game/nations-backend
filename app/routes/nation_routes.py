from flask import Blueprint, request, jsonify
from ..database import database_instance as database

from ..utils.security import decode_jwt_token
from ..database.models import User, Nation

nation_endpoints: Blueprint = Blueprint(
    name="nation_endpoints", 
    import_name=__name__, 
    url_prefix="/nation"
)

@nation_endpoints.route("/create", methods=["POST"])
def create():
    """
    Creates a new nation linked to the authorized account

    Headers:
        Authorization `str`: The jwt for the user.

    JSON:
        name `str`: The name of the nation.
        system `int`: The system used in the nation. View `NationTypes`
    
    Response JSON:
        status `str`: "error" or "success"
        details `str | dict`:
            If `status` is "error", it's the reason for the error as a `str`.
            Otherwise, it's' the nations information as a `dict`.
    """
    
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"status": "error", "details": "Unauthorized"}), 401

    user_id = decode_jwt_token(token)
    user: User
    
    if user_id is None:
        return jsonify({"status": "error", "details": "Bad authorization token."}), 401
    
    user = database.get_user_by_id(user_id)
    
    if user.nation_id != None:
        return jsonify({"status": "error", "details": "User already has a nation."}), 400
    
    request_data: dict = request.get_json()

    name: str = request_data.get("name")
    system: int = request_data.get("system")
    
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
            "details": "Error creating nation"
        }), 400

# Returns data of nation belonging to logged in user.
@nation_endpoints.route("/info", methods=["GET"])
def nation_data():
    """
    Gets the data of a nation given an ID.
    If a nation ID is not specified, it will default to the logged-in user's nation.

    Headers:
        Authorization `str`: The jwt for the user.
    
    JSON:
        nation_id `int`: The ID of the nation, is optional.
    
    Response JSON:
        status `str`: "error" or "success"
        details `str | dict`:
            If `status` is "error", it's the reason for the error as a `str`.
            Otherwise, it's' the nations information as a `dict`.
    """

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
    """
    Gets the factories of the logged-in user's nation.

    Headers:
        Authorization `str`: The jwt for the user.
    
    Response JSON:
        status `str`: "error" or "success"
        details `str | list`:
            If `status` is "error", it's the reason for the error as a `str`.
            Otherwise, it's' the list of the nations factories as a `list`.
    """

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
        return jsonify(factories)

@nation_endpoints.route('/factories/create', methods=["POST"])
def create_factory():
    """
    Creates a factory if a user provides a valid jwt token and deducts money from the user nation
    
    TODO: After land management is added, we must add a value in the JSON for the land used (most probably x1, x2, y1, y2)

    Headers:
        Authorization `str`: The jwt for the user.
    
    JSON:
        nation_id `int`: The ID of the nation
        factory_type `str`: The type of factory
    
    Response JSON:
        status `str`: "error" or "success"
    """

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"status": "error", "details": "Authorization token missing"}), 401
    
    nation_id: int
    factory_type_id: int

    user_id = decode_jwt_token(token)
    user = database.get_user_by_id(user_id)

    if user is not None:
        if user.nation_id is None:
            return jsonify({"status": "error", "details": "User does not have a nation."}), 401
        nation_id = user.nation_id
    else:
        return jsonify({"status": "error", "details": "Bad authorization token."}), 401
    
    factory_type = database.get_factory_type_by_id(factory_type_id)
    if factory_type is None:
        return jsonify({"status": "error", "details": "Invalid factory type"}), 400
    
    database.add_factory_to_nation(nation_id, factory_type_id)
    return jsonify({"status": "success"})
    
    