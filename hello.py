#!/usr/bin/env python3

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("task")

TODOs = {
    1: {"task": "build an API"},
    2: {"task": "?????"},
    3: {"task": "profit"},
}


def abort_if_todo_not_found(todo_id):
    if todo_id not in TODOs:
        abort(404, message="TODO {} does not exist".format(todo_id))


def add_todo(todo_id):
    args = parser.parse_args()
    todo = {"task": args["task"]}
    TODOs[todo_id] = todo
    return todo


class Todo(Resource):
    """
    Shows a single TODO item and lets you delete a TODO item.
    """

    def get(self, todo_id):
        abort_if_todo_not_found(todo_id)
        return TODOs[todo_id]

    def delete(self, todo_id):
        abort_if_todo_not_found(todo_id)
        del TODOs[todo_id]
        return "", 204

    def put(self, todo_id):
        return add_todo(todo_id), 201


class TodoList(Resource):
    """
    Shows a list of all TODOs and lets you POST to add new tasks.
    """

    def get(self):
        return TODOs

    def post(self):
        todo_id = max(TODOs.keys()) + 1
        return add_todo(todo_id), 201


api.add_resource(Todo, "/todos/<int:todo_id>")
api.add_resource(TodoList, "/todos")


'''
CORS:
Let's imagine you have two websites:
1. Zoe's Happy fun online discussion emporium
2. Hazel's Evil discussion runing hacker troll site

on website 1, we have a FORM that does a POST to make a post on the discussion
on website 2, all we have to do is tell the browser to make a POST to the same URL on webiste as the FORM would POST to... except, we can fill it in with our own NEFAIROUS AND EVIL CONTENT!!!

if the user for example, is logged into website 1, but they also browse to website2, then website 2 can make their browser post FOR THEM to website1, and it can make them say WHATEVER THEY WANT!!!
'''

if __name__ == "__main__":
    app.run(debug=True)
