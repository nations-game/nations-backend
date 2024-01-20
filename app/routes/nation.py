from flask import Blueprint

nation_endpoints: Blueprint = Blueprint(
    name="nation_endpoints", 
    import_name=__name__, 
    url_prefix="/nation"
)

@nation_endpoints.route("/create")
async def create():
    ...