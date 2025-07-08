from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Retrieve all pictures.

    Returns:
        Response: A Flask response object containing the list of pictures in JSON format if available,
                  or an empty list with a 200 status code if no pictures are found.
    """
    if data:
        return jsonify(data), 200
    else:
        return jsonify([]), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Retrieve a picture by its ID.

    Args:
        id (int): The ID of the picture to retrieve.

    Returns:
        Response: A Flask response object containing the picture data in JSON format if found,
                  or an error message if the picture is not found.
    """
    if data:
        for picture in data:
            try:
                if int(picture["id"]) == id:
                    return jsonify(picture), 200
            except (KeyError, ValueError):
                # Handle the case where 'id' key is missing or cannot be converted to an integer
                continue

    return jsonify({"message": f"Picture with id {id} not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture and add it to the data list.

    Expects:
        JSON data representing the new picture.

    Returns:
        Response: A Flask response object containing a success message and the new picture data,
                  or an error message if the request is invalid.
    """
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    # Extract JSON data from the request
    new_picture = request.get_json()

    # Validate the data (you can add additional validations here)
    if not new_picture:
        return jsonify({"message": "Invalid picture data"}), 400

    # Add a new ID if necessary (e.g., using the last ID + 1)
    if not data:
        new_picture["id"] = 1
    else:
        new_picture["id"] = max(int(picture["id"]) for picture in data) + 1

    # Add the new picture to the data list
    data.append(new_picture)

    # Return a success response with the new picture data
    return jsonify({"message": "Picture added successfully", "picture": new_picture}), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
