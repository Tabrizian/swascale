from pymodm import MongoModel, fields


class Server(MongoModel):
    uid = fields.CharField(required=True)
    name = fields.CharField(required=True)
    image = fields.CharField(required=True)
    flavor = fields.CharField(required=True)
    networks = fields.ListField(field=fields.CharField())
    region = fields.CharField(required=True)
    driver = fields.CharField(required=True)
