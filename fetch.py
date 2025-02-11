import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://jhapiyush2013:5PnvrMPf1iPrRjsz@mongo-pagination-test.ghb1b.mongodb.net/")
db = client["master"]
collection = db["application_data"]

def skiplimit(page_size, page_number):
    """Fetch data using skip-limit pagination."""
    skip = (page_number - 1) * page_size
    cursor = collection.find().skip(skip).limit(page_size)
    return list(cursor)

def idlimit(page_size, last_id):
    """Fetch data using cursor-based pagination."""
    query = {} if last_id is None else {'_id': {'$gt': last_id}}
    cursor = collection.find(query).limit(page_size)
    data = list(cursor)
    new_last_id = data[-1]['_id'] if data else None
    return data, new_last_id


def idlimit_1(page_size, last_id):
    """Function returns `page_size` number of documents after last_id
    and the new last_id.
    """
    if last_id is None:
        # When it is first page
        cursor = db['application_data'].find().limit(page_size)
    else:
        cursor = db['application_data'].find({'_id': {'$gt': last_id}}).limit(page_size)

    # Get the data
    data = [x for x in cursor]

    if not data:
        # No documents left
        return None, None

    # Since documents are naturally ordered with _id, last document will
    # have max id.
    last_id = data[-1]['_id']

    # Return data and last_id
    return data, last_id