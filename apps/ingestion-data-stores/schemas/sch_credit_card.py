key = """
{
    "namespace": "owshq.credit_card",
    "name": "key",
    "type": "record",
    "fields" : [
    {
        "name" : "user_id",
        "type" : "int"
    }
            ]
}
"""

value = """
{
    "namespace": "owshq.credit_card",
    "name": "value",
    "type": "record",
    "fields" : [
    {
        "name" : "uuid",
        "type" : "string"
    },
    {
        "name" : "user_id",
        "type" : "int"
    },
    {
        "name" : "provider",
        "type" : "string"
    },
    {
        "name" : "number",
        "type" : "string"
    },
    {
        "name" : "expire_data",
        "type" : "string"
    },
    {
        "name" : "security_code",
        "type" : "string"
    },
    {
        "name" : "dt_current_timestamp",
        "type" : "string"
    }
        ]
}
"""