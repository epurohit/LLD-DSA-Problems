"""
To make internal tools reusable, the AI Transformation team stores agent configurations as nested JSON-like dictionaries.

Some values in these configurations are variables that reference other keys within the same dictionary. Your task is to write a parser that resolves all these variables dynamically.

Requirements:
1. A variable is formatted as a string with a $ prefix (e.g., "$db_host").
2. The parser must recursively resolve variables to their literal values.
3. A variable might resolve to another variable, which then needs to be resolved.
4. If a variable references a key that does not exist, raise a KeyError.
5. If the configuration contains a circular reference (e.g., A resolves to B, and B resolves to A), raise a ValueError.
"""

from collections import defaultdict

def resolve_config(config: dict[str, str]) -> dict[str, str]:
    ans = {}
    
    def dfs(key: str, current_path: set) -> str:
        # 1. Memoization: If we already resolved this key, just return it
        if key in ans:
            return ans[key]
            
        # 2. Base Cases (Errors)
        if key not in config:
            raise KeyError(f"Missing referenced key: {key}")
            
        if key in current_path:
            raise ValueError(f"Circular dependency detected at key: {key}")
            
        # 3. Add to current traversal path
        current_path.add(key)
        
        # 4. Resolve the value
        val = config[key]
        if val.startswith('$'):
            # The variable name is everything after the '$'
            val = dfs(val[1:], current_path)
            
        # 5. Backtrack: Remove from path so other branches can visit it safely
        current_path.remove(key)
        
        # 6. Store the final literal value in our answer dictionary (memoizing it)
        ans[key] = val
        return val

    # Iterate through all keys in the original config
    for key in config:
        dfs(key, set())
        
    return ans
