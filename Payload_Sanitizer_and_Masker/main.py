"""
## Problem 2: Tool Call Payload Sanitizer and Masker

When agents interact with enterprise systems via MCP servers, certain payloads contain sensitive corporate or personal data that must be sanitized before being passed to external or logging utilities.

You are given a configuration of sensitive fields and a nested JSON payload. You must write a recursive sanitizer that masks sensitive values.

### Requirements

1. Traverse a nested JSON object (dictionaries and lists).
2. If a dictionary key matches any string in a provided `sensitive_keys` set, replace its value with `"***MASKED***"`.
3. The matching must be case-insensitive.
4. The structure of the original payload (lists and nested dicts) must be perfectly preserved.
"""

def sanitize_payload(payload: dict | list, sensitive_keys: set[str]) -> dict | list:
    """
    Recursively sanitizes a nested payload by masking values of sensitive keys.
    
    :param payload: A nested JSON-like structure (dicts, lists, primitives).
    :param sensitive_keys: A set of strings representing keys to redact.
    :return: A new sanitized structure with identical shape.
    """
    replacement = "***MASKED***"

    updated_sensitive = {txt.lower() for txt in sensitive_keys}

    if isinstance(payload, dict):
        new_dict = dict()
        for key, val in payload.items():
            if key.lower() in updated_sensitive:
                new_dict[key] = replacement
            else:
                if isinstance(val, (dict, list)):
                    new_dict[key] = sanitize_payload(val, updated_sensitive)
                else:
                    new_dict[key] = val

        return new_dict
    
    elif isinstance(payload, (list)):
        new_list = list()
        for item in payload:
            if isinstance(item, (dict, list)):
                new_list.append(sanitize_payload(item, updated_sensitive))
            else:
                new_list.append(item)
        return new_list
    
    return payload