import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting all entries for a list
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_all_entries(list_id):
    # if the given method is invalid, return status code 405
    if request.method != 'GET':
        abort(405)
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    # find all todo entries for the todo list with the given id
    return jsonify([i for i in todos if i['list'] == list_id]), 200

# define endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        todo_lists.remove(list_item)
        return jsonify({'msg': 'success'}), 200
    else:
        abort(405)

# define endpoint for adding a new list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # if the given method is invalid, return status code 405
    if request.method != 'POST':
        abort(405)
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    # create id for new list, save it and return the list with id
    new_list['id'] = uuid.uuid4()
    todo_lists.append(new_list)
    return jsonify(new_list), 200

# define endpoint for adding one entry to a list
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    # if the given method is invalid, return status code 405
    if request.method != 'POST':
        abort(405)
    # make JSON from POST data (even if content type is not set correctly)
    new_entry = request.get_json(force=True)
    # expand the json with an unique id and the list id
    new_entry = new_entry + {'id': uuid.uuid4(), 'list': list_id}
    todos.append(new_entry)

    return jsonify(new_entry), 200
    

# define endpoint for updating or deleting an existing entry
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def update_entry(list_id, entry_id):
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    entry_item = None
    for l in todos:
        if l['id'] == entry_id:
            entry_item = l
            break
    if request.method == 'PUT':
        # find all todo entries for the todo list with the given id
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete entry with given id
        todo_lists.remove(entry_item)
        return jsonify({'msg': 'success'}), 200
    else:
        abort(405)

# define endpoint for getting all lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    if request.method != 'GET':
        abort(405)
    return jsonify(todo_lists), 200


if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='127.0.0.1', port=3000)
