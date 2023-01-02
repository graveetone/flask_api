from flask import abort, make_response
from models import Person, people_schema, person_schema
from config import database as db

def read_all():
    people = Person.query.all()
    return people_schema.dump(people)

def find_person(lname):
    return Person.query.filter_by(lname=lname).one_or_none()


def create(person):
    lname = person.get('lname')
    existing_person = find_person(lname)

    if not existing_person:
        new_person = person_schema.load(person, session=db.session)

        db.session.add(new_person)
        db.session.commit()

        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with {lname} already exists")

def read_one(lname):
    person = find_person(lname)

    if person:
        return people_schema.dump(person)
    else:
        abort(404, f"Person with last name {lname} not found")

def update(lname, person):
    existing_person = find_person(lname)

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with last name {lname} not found")

def delete(lname):
    existing_person = find_person(lname)
    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()

        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {lname} not found")
