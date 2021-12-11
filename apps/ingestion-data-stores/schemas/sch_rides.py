key = """
{
    "namespace": "owshq.rides",
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
    "namespace": "owshq.rides",
    "name": "value",
    "type": "record",
    "fields" : [
    {
        "name" : "user_id",
        "type" : "int"
    },
    {
        "name" : "time_stamp",
        "type" : "int"
    },
    {
        "name" : "source",
        "type" : "string"
    },
    {
        "name" : "destination",
        "type" : "string"
    },
    {
        "name" : "distance",
        "type" : "float"
    },
    {
        "name" : "price",
        "type" : "float"
    },
    {
        "name" : "surge_multiplier",
        "type" : "float"
    },
    {
        "name" : "id",
        "type" : "string"
    },
    {
        "name" : "product_id",
        "type" : "string"
    },
    {
        "name" : "name",
        "type" : "string"
    },
    {
        "name" : "cab_type",
        "type" : "string"
    },
    {
        "name" : "dt_current_timestamp",
        "type" : "string"
    }
        ]
}
"""