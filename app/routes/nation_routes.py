from flask import Blueprint

nation_endpoints: Blueprint = Blueprint(
    name="nation_endpoints", 
    import_name=__name__, 
    url_prefix="/nation"
)

# TODO: Creates a nation. Sets a name, flag, etc.
@nation_endpoints.route("/create", methods=["POST"])
async def create():
    ...

# TODO: Returns data of specified nation, or of nation belonging to logged in user.
@nation_endpoints.route("/info", methods=["GET"])
async def nation_data():
    ...