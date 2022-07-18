from recipe_app.config.mysqlconnection import connectToMySQL
from recipe_app.models import user
from recipe_app.models import comment
from flask import flash
import pprint
class Recipe:
    db_name="recipes"
    def __init__(self,data):
        self.id=data["id"]
        self.name=data["name"]
        self.description = data["description"]
        self.instruction= data["instruction"]
        self.date_made_on = data["date_made_on"]
        self.under_30_minutes = data["under_30_minutes"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.users=[]

        self.comments=[]

    @classmethod
    def create(cls,data):
        query="INSERT INTO recipes (name,description,instruction,date_made_on,under_30_minutes,user_id) VALUES (%(NAME)s,%(DESCRIPTION)s, %(INSTRUCTION)s, %(DATE_MADE_ON)s, %(UNDER_30_MINUTES)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all_recipe(cls):
        query="SELECT * FROM recipes;"
        result = connectToMySQL(cls.db_name).query_db(query)
        recipes=[]
        for one_recipe in result:
            recipes.append(cls(one_recipe))
        return recipes

    @classmethod
    def get_recipe_with_user(cls,data):
        query="SELECT * FROM recipes LEFT JOIN users on users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results= connectToMySQL(cls.db_name).query_db(query,data)
        recipe = cls(results[0])
        for all in results:
            user_data={
                "id": all["users.id"],
                "first_name": all["first_name"],
                "last_name":all["last_name"],
                "email":all["email"],
                "password":all["password"],
                "created_at":all["created_at"],
                "updated_at":all["updated_at"]
            }
            users = user.User(user_data)
            recipe.users
        return recipe

    @classmethod
    def get_one_recipe(cls,data):
        query="SELECT * FROM recipes WHERE id=%(id)s;"
        results=  connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update_recipe(cls,data):
        query="UPDATE recipes SET name=%(NAME)s, description=%(DESCRIPTION)s, instruction=%(INSTRUCTION)s, date_made_on=%(DATE_MADE_ON)s, under_30_minutes=%(UNDER_30_MINUTES)s WHERE recipes.id=%(id)s;"
        results=  connectToMySQL(cls.db_name).query_db(query,data)
        print (results)
        return results

    @classmethod
    def delete_recipe(cls,data):
        query="DELETE FROM recipes WHERE recipes.id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
      
    @classmethod
    def get_recipe_with_comment(cls,data):
        query="SELECT * ,likes.user_id AS liked_by FROM recipes LEFT JOIN comments ON comments.recipe_id = recipes.id LEFT JOIN users ON comments.user_id = users.id LEFT JOIN likes ON likes.user_id=%(user_id)s AND likes.comment_id = comments.id  WHERE recipes.id = %(id)s;"
        results=  connectToMySQL(cls.db_name).query_db(query,data)
        recipe = cls(results[0])
        # pprint.pprint(results)
        for one_recipe in results:
            comment_data={
                "id" : one_recipe["comments.id"],
                "comment" : one_recipe["comment"],
                "user_id" :one_recipe["user_id"],
                "recipe_id" :one_recipe["recipe_id"],
                "created_at" : one_recipe["created_at"],
                "updated_at": one_recipe["updated_at"]
            }
            get_comments = comment.Comment(comment_data)
            # liked_by same as likes.user_id
            if one_recipe ["likes.user_id"] == data["user_id"]:
                get_comments.LIKE = True
                print(one_recipe["comments.id"])
                print(one_recipe["liked_by"])
            get_comments.userName = one_recipe["first_name"]
            recipe.comments.append(get_comments)
        # pprint.pprint(recipe)
        return recipe
        


    @staticmethod
    def validate_recipe(data):
        is_valid=True
        if len(data["NAME"]) <3:
            flash("Name must be at least 3 characters.","recipe")
            is_valid=False
        if len(data["DESCRIPTION"]) <3:
            flash("Description must be at least 3 characters.",'recipe')
            is_valid=False
        
        if len(data["INSTRUCTION"]) <3:
            flash("Instructions must be at least 3 characters.",'recipe')
            is_valid=False
        if len(data["DATE_MADE_ON"]) =="":
            flash("Please enter a date","recipe")
            is_valid=False
            
        if "UNDER_30_MINUTES" not in data  :
            flash("Please choose one.","recipe")
            is_valid=False
       
        return is_valid


