from flask import Blueprint, request, jsonify
from app import db
from app.models import Task, Comment

comments_bp = Blueprint("comments", __name__, url_prefix="/api")

@comments_bp.route("/tasks/<int:task_id>/comments", methods=["GET"])
def list_comments(task_id):
    task = Task.query.get_or_404(task_id)
    comments = [c.to_dict() for c in task.comments]
    return jsonify(comments), 200

@comments_bp.route("/tasks/<int:task_id>/comments", methods=["POST"])
def create_comment(task_id):
    Task.query.get_or_404(task_id)
    data = request.get_json()

    if not data.get("content"):
        return jsonify({"error": "Content required"}), 400

    comment = Comment(
        task_id=task_id,
        content=data["content"],
        author_name=data.get("author_name")
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@comments_bp.route("/tasks/<int:task_id>/comments/<int:comment_id>", methods=["PUT"])
def update_comment(task_id, comment_id):
    Task.query.get_or_404(task_id)
    comment = Comment.query.filter_by(id=comment_id, task_id=task_id).first_or_404()

    data = request.get_json()

    if "content" in data:
        if not data["content"]:
            return jsonify({"error": "Content cannot be empty"}), 400
        comment.content = data["content"]

    if "author_name" in data:
        comment.author_name = data["author_name"]

    db.session.commit()
    return jsonify(comment.to_dict()), 200

@comments_bp.route("/tasks/<int:task_id>/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(task_id, comment_id):
    Task.query.get_or_404(task_id)
    comment = Comment.query.filter_by(id=comment_id, task_id=task_id).first_or_404()

    db.session.delete(comment)
    db.session.commit()

    return "", 204
