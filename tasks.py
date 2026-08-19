from flask import Blueprint, request, jsonify
from models import db, Task
from auth_middleware import token_required

tasks_bp = Blueprint('tasks', __name__)


#GET requests data from a specific resource, should never be used with sensitive data
@tasks_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    #list comprehension conversting Task objects into dictionaries because json can't serialize
    #SQLAlchemy objects directly so they need to be converted to python dictionaries first
    result = [{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'status': t.status,
        'createdAt': t.createdAt.isoformat(),#formatting datetime object to ISO 8601 string representation for JSON serialization
        'updatedAt': t.updatedAt.isoformat()
    } for t in tasks]

    return jsonify(result), 200

@tasks_bp.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({'error':'Title is required'}), 400

    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        user_id=current_user.id
    )

    db.session.add(new_task)
    db.session.commit

    return jsonify({'message':'Task created','id': new_task.id}), 201


#<int:task_id> extracts task id from the url into the function as an integer
#PUT is correct for updating an exsiting resource
@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)

    db.session.commit()
    return jsonify({'message':'Task updated'}), 200
    
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
            return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message':'Task deleted'}), 200