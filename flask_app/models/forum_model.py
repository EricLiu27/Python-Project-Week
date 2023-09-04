from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
import re
from flask import flash
from flask_app.models import user_model


class Forum:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.subject = data['subject']
        self.posting = data ['posting']
        self.date_posted = data['date_posted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def create(cls,data):
        query = 'INSERT INTO forums (name, subject, posting, date_posted, user_id) VALUES (%(name)s,%(subject)s,%(posting)s,%(date_posted)s,%(user_id)s);'
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def get_all (cls):
        query = 'SELECT * FROM forums JOIN users ON forums.user_id = users.id;'
        results = connectToMySQL(DATABASE).query_db(query)
        all_forums = []
        if results:
            for row in results:
                this_forum= cls (row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_forum.member = this_user
                all_forums.append(this_forum)
        return all_forums
    

    @classmethod
    def api_get_all (cls):
        query = 'SELECT * FROM forums JOIN users ON forums.user_id = users.id;'
        results = connectToMySQL(DATABASE).query_db(query)
        
        return results

    @classmethod
    def get_one (cls,data):
        query = 'SELECT * FROM forums JOIN users ON forums.user_id = users.id WHERE forums.id = %(id)s;'

        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if results:
            row = results [0]
            this_forum= cls (row)
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_user = user_model.User(user_data)
            this_forum.member = this_user
            return this_forum
        return False
    
    @classmethod
    def delete(cls,data):
        query = " DELETE FROM forums WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query ="""
            UPDATE forums
            SET
            name = %(name)s,
            subject = %(subject)s,
            posting = %(posting)s,
            date_posted = %(date_posted)s
            WHERE forums.id = %(id)s;
            """ 
        return connectToMySQL(DATABASE).query_db(query,data)
        



    @staticmethod
    def is_valid(data):
        is_valid = True
        if len(data['name']) < 1:
            flash ('Name is required')
            is_valid = False
        elif len(data['name']) < 3:
            flash ('Name must have at least 3 characters')
            is_valid = False
        if len(data['subject']) < 1:
            flash ('Subject is required')
            is_valid = False
        elif len(data['subject']) < 3:
            flash ('Subject must have at least 3 characters')
            is_valid = False
        if len(data['posting']) < 1:
            flash ('Post is required')
            is_valid = False
        elif len(data['posting']) < 3:
            flash ('Post must have at least 3 characters')
            is_valid = False
        if len(data['date_posted']) < 1:
            flash ('Date is required')
            is_valid = False
        return is_valid
        

        
    @staticmethod
    def api_is_valid(data):
        errors = []
        if len(data['name']) < 1:
            errors.append('Name is required')

        if len(data['subject']) < 1:
            errors.append('Subject is required')

        if len(data['date_posted']) < 1:
            errors.append('Date is required')

        if len(data['posting']) < 1:
            errors.append('Post is required')

        return errors
        