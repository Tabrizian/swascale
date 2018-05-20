from pymodm import MongoModel, fields


class Server(MongoModel):
    _id = fields.CharField(required=true)
    name = fields.CharField(required=true)
    image = fields.CharField(required=true)
    flavor = fields.CharField(required=true)
    networks = fields.FieldList(field=CharField)