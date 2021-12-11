key = """
{
    "namespace": "owshq.users",
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
    "namespace": "owshq.users",
    "name": "value",
    "type": "record",
    "fields" : [
    {
        "name" : "user_id",
        "type" : "int"
    },
    {
        "name" : "uuid",
        "type" : "string"
    },
    {
        "name" : "first_name",
        "type" : "string"
    },
    {
        "name" : "last_name",
        "type" : "string"
    },
    {
        "name" : "date_birth",
        "type" : "string"
    },
    {
        "name" : "city",
        "type" : "string"
    },
    {
        "name" : "country",
        "type" : "string"
    },
    {
        "name" : "company_name",
        "type" : "string"
    },
    {
        "name" : "job",
        "type" : "string"
    },
    {
        "name" : "phone_number",
        "type" : "string"
    },
    {
        "name" : "last_access_time",
        "type" : "string"
    },
    {
        "name" : "time_zone",
        "type" : "string"
    },
    {
        "name" : "dt_current_timestamp",
        "type" : "string"
    }
        ]
}
"""