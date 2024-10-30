from marshmallow import Schema, fields, validate

class UrlSchema(Schema):
    url = fields.Url(required=True)

class AnswersSchema(Schema):
    url = fields.Url(required=True)
    answers = fields.Dict(keys=fields.Str(), values=fields.Str(), required=True) 