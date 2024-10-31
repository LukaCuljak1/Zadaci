from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zadaci.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.filter_by(is_deleted=False).all()
    return jsonify([{'id': task.id, 'content': task.content, 'completed': task.completed} for task in tasks])

@app.route('/api/tasks/bulk', methods=['POST'])
def add_tasks_bulk():
    data = request.json
    tasks = [Task(content=task['content'], completed=task.get('completed', False)) for task in data if 'content' in task]
    db.session.bulk_save_objects(tasks)
    db.session.commit()
    return jsonify({'message': 'Tasks added'}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = Task.query.get_or_404(task_id)
    if 'completed' in data:
        task.completed = data['completed']
    db.session.commit()
    return jsonify({'message': 'Task updated'}), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
