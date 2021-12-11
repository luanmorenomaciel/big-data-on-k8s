key = """
{
    "namespace": "owshq.agent",
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
    "namespace": "owshq.agent",
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
        "name" : "platform",
        "type" : "string"
    },
    {
        "name" : "email",
        "type" : "string"
    },
    {
        "name" : "domain",
        "type" : "string"
    },
    {
        "name" : "hostname",
        "type" : "string"
    },
    {
        "name" : "method",
        "type" : "string"
    },
    {
        "name" : "url",
        "type" : "string"
    },
    {
        "name" : "ipv4",
        "type" : "string"
    },
    {
        "name" : "port_number",
        "type" : "string"
    },
    {
        "name" : "mac_address",
        "type" : "string"
    },
    {
        "name" : "dt_current_timestamp",
        "type" : "string"
    }
        ]
}
"""