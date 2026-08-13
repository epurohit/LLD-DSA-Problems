from main import resolve_config

# Test Case 1: Simple Resolution
config_1 = {
    "host": "localhost",
    "port": "5432",
    "url": "$host",
    "connection_string": "$url"
}

try:
    print(resolve_config(config=config_1))
except Exception as e:
    print(str(e))

# Expected Output:
# {
#     "host": "localhost",
#     "port": "5432",
#     "url": "localhost",
#     "connection_string": "localhost"
# }

# Test Case 2: Missing Key
config_2 = {
    "db_user": "admin",
    "password": "$db_password" # $db_password is not a key in the dict
}
try:
    print(str(resolve_config(config=config_2)))
except Exception as e:
    print(str(e))

# Expected Output: Raises KeyError

# Test Case 3: Circular Reference
config_3 = {
    "node_a": "$node_b",
    "node_b": "$node_c",
    "node_c": "$node_a"
}

try:
    print(str(resolve_config(config=config_3)))
except Exception as e:
    print(str(e))
# Expected Output: Raises ValueError