from main import AgentRateLimiter

limiter = AgentRateLimiter(max_requests=3, window_size_seconds=10)

# Agent A makes 3 requests at second 1 (All Allowed)
assert limiter.is_allowed("Agent_A", 1) == True
assert limiter.is_allowed("Agent_A", 1) == True
assert limiter.is_allowed("Agent_A", 1) == True

# Agent A is blocked on the 4th request at second 2
assert limiter.is_allowed("Agent_A", 2) == False

# Agent B is completely unaffected by Agent A's limit
assert limiter.is_allowed("Agent_B", 2) == True

# Time jumps to second 11. 
# The window is now (1 to 11]. The requests at second 1 fall out of the window.
# Agent A should be allowed to make requests again.
assert limiter.is_allowed("Agent_A", 11) == True