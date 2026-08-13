"""
API Rate Limiter for Agent Tool Calls
When building AI agents that automate workflows, one of the biggest risks is an agent entering a loop and overwhelming internal systems (like Finance or HR APIs) with thousands of requests per second.

You are tasked with implementing a lightweight Rate Limiter to protect internal APIs from runaway agents.

Requirements:
1. The rate limiter must track requests per agent_id.
2. It must enforce a limit of max_requests over a rolling time window of window_size_seconds.
3. If an agent exceeds the limit, the system should block the request.
4. Old requests that fall outside the current time window should no longer count against the agent's limit.
"""

from collections import defaultdict, deque

class AgentRateLimiter:
    def __init__(self, max_requests: int, window_size_seconds: int):
        """
        Initializes the rate limiter.
        """
        self.max_requests = max_requests
        self.window_size = window_size_seconds
        self.request_history = defaultdict(deque)

    def is_allowed(self, agent_id: str, timestamp_seconds: int) -> bool:
        """
        Determines if a tool call from an agent is allowed.
        
        :param agent_id: String identifier for the agent
        :param timestamp_seconds: The current time in seconds (monotonically increasing)
        :return: True if the request is allowed, False if it is rate-limited
        """
        agent_request_history = self.request_history[agent_id]

        while agent_request_history and (timestamp_seconds - agent_request_history[0]) >= self.window_size:
            agent_request_history.popleft()

        if len(agent_request_history) < self.max_requests:
            agent_request_history.append(timestamp_seconds)
            return True

        return False