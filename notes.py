from flask import abort, make_response

from config import database as db
from models import Note, note_schema, Person
from constants import Messages 


def find_note(note_id):
    return Note.query.get(note_id)

def read_one(note_id):
    note = find_note(note_id)

    if note:
        return note_schema.dump(note)
    else:
        abort(
            404, Messages.NOTE_NOT_FOUND_MESSAGE.format(note_id=note_id)
        )

def update(note_id, note):
    existing_note = find_note(note_id)

    if existing_note:
        update_note = note_schema.load(note, session=db.session)
        
        existing_note.content = update_note.content
        db.session.merge(existing_note)
        db.session.commit()

        return note_schema.dump(existing_note), 201
    else:
        abort(
            404, Messages.NOTE_NOT_FOUND_MESSAGE.format(note_id=note_id)
        )

def delete(note_id):
    note = find_note(note_id)
    
    if note:
        db.session.delete(note)
        db.session.commit()

        return make_response(Messages.NOTE_SUCCESSFULLY_DELETED.format(note_id=note_id), 204)
    else:
        abort(404, Messages.NOTE_NOT_FOUND_MESSAGE.format(note_id=note_id))
        
def create(note):
    person_id = note.get('person_id')
    person = Person.query.get(person_id)

    if person:
        note = note_schema.load(note)
        person.notes.append(note)

        db.session.commit()
        
        return note_schema.dump(note), 201
    else:
        abort(404, Messages.PERSON_WITH_ID_NOT_FOUND.format(person_id=person_id))
        