
from app import marsh
from flask_marshmallow import fields


class ThreadsSchema(marsh.Schema):
    class Meta:
        fields = ('title', 'body', 'created_at')



class ReplySchema(marsh.Schema):
    class Meta:
        fields = ('user', 'body', 'created_at')

class ThreadSchema(marsh.Schema):
    replies = marsh.Nested(ReplySchema, many=True)
    class Meta:
        fields = ('title', 'body', 'created_at')
    
