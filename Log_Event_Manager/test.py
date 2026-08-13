from main import process_and_deduplicate_logs

logs_stream = [
    {"timestamp": 1, "source": "finance", "event_id": "tx_100"},
    {"timestamp": 3, "source": "finance", "event_id": "tx_100"}, # Duplicate within window (3 - 1 < 5)
    {"timestamp": 4, "source": "people", "event_id": "hr_01"},
    {"timestamp": 8, "source": "finance", "event_id": "tx_100"}, # Outside window relative to first (8 - 1 >= 5), but let's check rolling logic
    {"timestamp": 10, "source": "finance", "event_id": "tx_200"}
]
# If window_seconds = 5:
# - log at t=1 (finance, tx_100) -> Kept
# - log at t=3 (finance, tx_100) -> Dropped (within 5s of t=1)
# - log at t=4 (people, hr_01) -> Kept
# - log at t=8 (finance, tx_100) -> Kept (since 8 - 3 >= 5, or measured from last seen)
# - log at t=10 (finance, tx_200) -> Kept

print(process_and_deduplicate_logs(logs_stream, 5))

logs_stream_2 = [
    {"timestamp": 1, "source": "finance", "event_id": "tx_100"},
    {"timestamp": 3, "source": "engineering", "event_id": "tx_100"},
    {"timestamp": 4, "source": "people", "event_id": "hr_01"},
    {"timestamp": 6, "source": "engineering", "event_id": "tx_100"},
    {"timestamp": 10, "source": "finance", "event_id": "tx_100"}
]
# If window_seconds = 5:
# - log at t=1 (finance, tx_100) -> Kept
# - log at t=3 (engineering, tx_100) -> Kept
# - log at t=4 (people, hr_01) -> Kept
# - log at t=6 (engineering, tx_100) -> Dropped (since 6 - 3 <= 3)
# - log at t=10 (finance, tx_200) -> Kept

print(process_and_deduplicate_logs(logs_stream_2, 3))