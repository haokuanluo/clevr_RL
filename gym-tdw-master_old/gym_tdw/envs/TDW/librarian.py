from TDW.db_server import MODELS_COLLECTION, MATERIALS_COLLECTION
from bson.json_util import dumps, loads
from bson import ObjectId
import io


"""
librarian.py is a collection of helper functions for querying the model and material record database.
For example implementation, see example_librarian_controller.py
"""


def get_collection_from_json(collection):
    """
    Convert a MongoDB collection into a JSON dictionary.
    :param collection: The MongoDB collection.
    :return: A JSON dictionary converted from the MongoDB collection.
    """

    return loads(dumps(collection))


def fetch_all_model_records():
    """
    Fetches all model records.
    :return: A list of model records.
    """

    return get_collection_from_json(MODELS_COLLECTION.find())


def fetch_model_record_by_id(record_id):
    """
    Fetch a model record by ID.
    :param record_id: The MongoDB ID of the record.
    :return: A model record.
    """

    return get_collection_from_json(MODELS_COLLECTION.find_one(filter={"_id": ObjectId(record_id)}))


def fetch_model_records_by_ids(record_ids):
    """
    Fetch a list of model records by a list of IDs.
    :param record_ids: A list of MongoDB IDs corresponding to records.
    :return: A list of model records.
    """

    records = []
    for r in record_ids:
        records.append(get_collection_from_json(MODELS_COLLECTION.find(filter={"_id": ObjectId(r)})))

    return records


def fetch_model_record_by_name(model_name):
    """
    Fetch a model record by name.
    :param model_name: The name of the model.
    :return: A model record.
    """

    return get_collection_from_json(MODELS_COLLECTION.find_one(filter={"model_name": model_name}))


def fetch_model_records_by_names(model_names):
    """
    Fetch a list model records by a list of names.
    :param model_names: The names of the models.
    :return: A list of model records.
    """

    records = []
    for m in model_names:
        records.append(get_collection_from_json(MODELS_COLLECTION.find_one(filter={"model_name": m})))

    return records


def fetch_all_model_categories():
    """
    Fetch a dictionary of all WordNet IDs and categories in the records database.
    :return A dictionary, where the key is the WordNet ID and the value is the WordNet category.
    """

    wnids = get_collection_from_json(MODELS_COLLECTION.find(projection={"wcategory": True, "wnid": True, "_id": False}))
    wnids_dict = dict()
    for w in wnids:
        if w["wnid"] not in wnids_dict:
            wnids_dict.update({w["wnid"]: w["wcategory"]})
    return wnids_dict


def fetch_model_records_by_wnid(wnid):
    """
    Fetch a list of all model records with the WordNet ID.
    :param wnid: The WordNet ID.
    :return: A list of model
    """

    return get_collection_from_json(MODELS_COLLECTION.find(filter={"wnid": str(wnid)}))


def load_model_substructure(record):
    """
    Returns the model's substructure record as a list of JSON data.
    :param record: The model record.
    :return: The model's substructure.
    """

    return loads(record["substructure"])


def load_model_bounds(record):
    """
    Returns the model's bounds data.
    :param record: The model record.
    :return: The model's bounds data.
    """

    return loads(record["bounds"])


def fetch_all_material_records():
    """
    Fetch all material records.
    :return: A list of all material records.
    """

    return get_collection_from_json(MATERIALS_COLLECTION.find())


def fetch_material_record_by_id(record_id):
    """
    Fetch a material record by ID.
    :param record_id: The MongoDB ID of the record.
    :return: A material record.
    """

    return get_collection_from_json(MATERIALS_COLLECTION.find_one(filter={"_id": ObjectId(record_id)}))


def fetch_materials_records_by_ids(record_ids):
    """
    Fetch a list of material records by a list of IDs.
    :param record_ids: A list of MongoDB IDs corresponding to records.
    :return: A list of material records.
    """

    records = []
    for r in record_ids:
        records.append(get_collection_from_json(MATERIALS_COLLECTION.find(filter={"_id": ObjectId(r)})))


def fetch_material_record_by_name(material_name):
    """
    Fetch a material record by name.
    :param material_name: The name of the material.
    :return: A material record.
    """

    return get_collection_from_json(MATERIALS_COLLECTION.find_one(filter={"material_name": material_name}))


def fetch_material_records_by_names(material_names):
    """
    Fetch a list material records by a list of names.
    :param material_names: The names of the materials.
    :return: A list of material records.
    """

    records = []
    for m in material_names:
        records.append(get_collection_from_json(MATERIALS_COLLECTION.find_one(filter={"material_name": m})))
    return records


def fetch_material_records_by_type(semantic_type):
    """
    Fetch a list of all material records of a given semantic type.
    :param semantic_type: The semantic type.
    :return: A list of all material records with the given semantic type.
    """

    return get_collection_from_json(MATERIALS_COLLECTION.find(filter={"material_type": semantic_type}))


def write_to_csv(records, filename, delimiter="\t"):
    """
    Write a list of records to a .csv file.
    :param records: The list of records.
    :param filename: The name of the file.
    :param delimiter: The CSV delimiter. Default=tab.
    """
    output = ""
    num_keys = len(records[0].keys())
    # Create the header.
    for key, i in zip(records[0], range(num_keys)):
        output += key
        if i < num_keys - 1:
            output += delimiter
    output += "\n"
    for record in records:
        for key, i in zip(record, range(num_keys)):
            output += str(record[key])
            if i < num_keys - 1:
                output += delimiter
        output += "\n"
    # Append the correct extension.
    if not filename.endswith(".csv"):
        filename += ".csv"
    with io.open(filename, "wt", encoding="utf-8") as f:
        f.write(output)