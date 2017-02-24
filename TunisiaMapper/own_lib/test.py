import maps_api

api = maps_api.initiate_google_maps_api('AIzaSyBksI1g3hmNZXLyoctDmQoH8hdnpJWGLRo')
maps_api.get_places_within_state_by_type("park","NY",api)