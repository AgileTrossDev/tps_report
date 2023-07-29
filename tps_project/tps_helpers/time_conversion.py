
def convert_to_nano_seconds(iso8601_timestamp):
    """
    Converts a ISO8601 Time to a Unix Time Stamp in nano_seconds
    """
    print(f"Converting: {iso8601_timestamp}")
    # dt = datetime.fromisoformat(iso8601_timestamp.rstrip("Z"))
    unix_timestamp_seconds = (iso8601_timestamp.timestamp())
    nanoseconds = unix_timestamp_seconds * 1_000_000_000
    return nanoseconds
