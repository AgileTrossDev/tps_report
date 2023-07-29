#!/usr/bin/env python3

# Description: Tool used to convert ISO8601 Times to Unit Time Stamps in nanoseconds.
# Used for checking database

import sys
from datetime import datetime


def iso8601_to_unixtime(iso8601_timestamp):
    try:
        dt = datetime.fromisoformat(iso8601_timestamp.rstrip("Z"))
        unix_timestamp_seconds = (dt.timestamp())
        nanoseconds = unix_timestamp_seconds * 1_000_000_000
        return nanoseconds

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python iso8601_to_timestamp.py <ISO8601_TIMESTAMP>")
        sys.exit(1)

    iso8601_timestamp = sys.argv[1]
    unix_timestamp = iso8601_to_unixtime(iso8601_timestamp)
    print(f"{unix_timestamp:.15f}")
