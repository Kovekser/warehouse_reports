from marshmallow import Schema, fields


class ReportInputSchema(Schema):
    rtype = fields.Str(required=True)
    headers = fields.List(fields.Str(), required=True)
    data = fields.List(fields.Dict(keys=fields.Str()), required=True)
