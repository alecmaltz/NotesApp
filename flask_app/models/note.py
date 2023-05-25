from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class note:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.note_date = db_data['note_date']
        self.description = db_data['description']
        self.updated_at = db_data['updated_at']
        self.created_at = db_data['created_at']
        self.creator = None


    @classmethod
    def save_note( cls,data ):
        query = "INSERT INTO notes (title, note_date, description, user_id) VALUES (%(title)s, %(note_date)s, %(description)s, %(user_id)s);"
        return connectToMySQL('notes_app').query_db(query,data)


    @classmethod
    def get_user_with_notes(cls, name):
        query ="SELECT * FROM notes WHERE user.id = %(user_id)s;"
        results = connectToMySQL('notes_app').query_db(query , name)
        results = []
        for note in results:
            results.append(cls(note))
        return results


    @classmethod
    def get_one_with_name(cls, id):
        query = "SELECT * FROM notes LEFT JOIN users ON notes.user_id = users.id WHERE notes.id = %(id)s;"
        results = connectToMySQL('notes_app').query_db(query, {"id" : id})

        this_note = []
        if not results:
            return []
        
        for row in results:
            one_note = cls(row)
            
            creator_data = {
                "id" : row['id'],
                "user.id" : row['user_id'], 
                "first_name" : row['first_name'],
                "last_name": row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" :row['users.updated_at']
            }
            this_creator = user.User(creator_data)
            one_note.creator = this_creator
            this_note.append(one_note)
        return this_note


    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM notes LEFT JOIN users ON notes.user_id = users.id;"
        results = connectToMySQL('notes_app').query_db(query)
        
        all_notes = []
        if not results:
            return []
        
        for row in results:
            one_note = cls(row)
            
            creator_data = {
                "id" : row['id'],
                "user.id" : row['user_id'], 
                "first_name" : row['first_name'],
                "last_name": row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" :row['users.updated_at']
            }
            
            this_creator = user.User(creator_data)
            one_note.creator = this_creator
            all_notes.append(one_note)
        return all_notes


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM notes WHERE id = %(id)s;"
        return connectToMySQL('notes_app').query_db(query,data)



    @classmethod
    def update(cls,data):
        query = "UPDATE reportings SET title=%(title)s, date=%(date)s, desc=%(desc)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('notes_app').query_db(query,data)

