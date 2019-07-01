from marshmallow import Schema, fields


class ReportInputSchema(Schema):
    report_type = fields.Str(required=True)
    headers = fields.List(fields.Str(), required=True)
    data = fields.List(fields.Dict(keys=fields.Str()), required=True)
