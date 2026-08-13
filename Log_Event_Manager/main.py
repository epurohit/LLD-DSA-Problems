"""
When building internal automation pipelines and ingesting logs from various business units (Finance, RevOps, People), data streams often contain duplicate events due to network retries or webhooks firing multiple times.

You need to write a utility that processes a stream of log records, filters out duplicate events within a specific sliding time window, and aggregates the counts of unique events.

Requirements
1. Each log record is represented as a dictionary containing timestamp, source, and event_id.
2. A log is considered a duplicate if an identical event_id from the same source has already been processed within the last window_seconds.
3. Discard duplicate logs and return a dictionary tracking the total count of unique processed events per source.
"""

from collections import defaultdict, deque

def process_and_deduplicate_logs(logs: list[dict], window_seconds: int) -> dict[str, int]:
    """
    Deduplicates logs within a time window and returns unique event counts per source.
    
    :param logs: A list of log dicts, e.g., [{"timestamp": 10, "source": "finance", "event_id": "e1"}]
    :param window_seconds: The time window threshold for duplicate detection.
    :return: A dictionary mapping each source to its count of unique events.
    """

    log_records = deque()
    current_events = defaultdict(set)
    unique_events = defaultdict(int)

    for log in logs:
        source = log["source"]
        event = log["event_id"]
        ts = log["timestamp"]


        while log_records and (ts - log_records[0]["timestamp"]) > window_seconds:
            removed_log = log_records.popleft()

            if removed_log["event_id"] in current_events[removed_log["source"]]:
                current_events[removed_log["source"]].remove(removed_log["event_id"])

        if event not in current_events[source]:
            log_records.append(log)
            current_events[source].add(event)

            unique_events[source] += 1

    return dict(unique_events)
