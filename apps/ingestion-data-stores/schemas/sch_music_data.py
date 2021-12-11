key = """
{
    "namespace": "owshq.music_data",
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
    "namespace": "owshq.music_data",
    "name": "value",
    "type": "record",
    "fields" : [
    {
        "name" : "user_id",
        "type" : "int"
    },
    {
        "name" : "genre",
        "type" : "string"
    },
    {
        "name" : "artist_name",
        "type" : "string"
    },
    {
        "name" : "track_name",
        "type" : "string"
    },
    {
        "name" : "track_id",
        "type" : "string"
    },
    {
        "name" : "popularity",
        "type" : "int"
    },
    {
        "name" : "duration_ms",
        "type" : "int"
    }
        ]
}
"""