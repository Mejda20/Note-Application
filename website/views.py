from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/edit-note/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    data = json.loads(request.data)
    edited_content = data['content']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            note.data = edited_content
            db.session.commit()
            return jsonify({'message': 'Note updated successfully'}), 200
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    else:
        return jsonify({'error': 'Note not found'}), 404

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({'message': 'Note deleted successfully'}), 200
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    else:
        return jsonify({'error': 'Note not found'}), 404


