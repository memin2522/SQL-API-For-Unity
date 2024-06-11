from marshmallow import Schema, fields

class PatienSchema(Schema):
    id = fields.Int(dump_only=True)
    registration = fields.Str()
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    dateOfBirth = fields.Date(required=True)
    militaryStatus = fields.Str(required=True)
    militaryRank = fields.Str()

class PatienUpdateSchema(Schema):
    registration = fields.Str()
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    dateOfBirth = fields.Date(required=True)
    militaryStatus = fields.Str(required=True)
    militaryRank = fields.Str()