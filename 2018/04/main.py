import re
from datetime import datetime, timedelta

from collections import namedtuple
from operator import attrgetter, itemgetter

log_entry_pattern = re.compile(r'\[(?P<timestamp>\d+-\d+-\d+ \d+:\d+)] (?P<message>.+)')
LogEntry = namedtuple('LogEntry', 'timestamp, message')


def main():
    with open('input') as f:
        lines = f.readlines()

    log_entries = [parse_log_entry(line) for line in lines]
    log_entries.sort(key=attrgetter('timestamp'))

    answer_part_one = solve_part_one(log_entries)

    print('Answer part 1: {}'.format(answer_part_one))


def parse_log_entry(line):
    match = log_entry_pattern.match(line)
    assert match
    return LogEntry(
        datetime.strptime(match.group('timestamp'), '%Y-%m-%d %H:%M'),
        match.group('message')
    )


def solve_part_one(log_entries):
    sleep_log = compile_guard_sleep_log(log_entries)

    guard_sleep_times = {}

    for guard_id, durations in sleep_log.items():
        for (sleep_from, sleep_to) in durations:
            sleep_minutes = (sleep_to - sleep_from).total_seconds() / 60
            guard_sleep_times[guard_id] = sleep_minutes + guard_sleep_times.get(guard_id, 0)

    sleepiest_guard_id = max(guard_sleep_times.items(), key=itemgetter(1))[0]
    print('Sleepiest guard id: {}'.format(sleepiest_guard_id))

    sleep_minutes = {}
    for (sleep_from, sleep_to) in sleep_log[sleepiest_guard_id]:
        timestamp = sleep_from
        while timestamp < sleep_to:
            sleep_minutes[timestamp.minute] = 1 + sleep_minutes.get(timestamp.minute, 0)
            timestamp += timedelta(minutes=1)

    sleepiest_minute = max(sleep_minutes.items(), key=itemgetter(1))[0]
    print('Sleepiest minute: {}'.format(sleepiest_minute))

    return sleepiest_guard_id * sleepiest_minute


def compile_guard_sleep_log(log_entries):
    guard_log_pattern = re.compile(r'Guard #(?P<id>\d+) begins shift')

    guard_sleep_times = {}

    current_guard_id = None
    sleep_start = None

    for entry in log_entries:
        if entry.message.startswith('Guard'):
            match = guard_log_pattern.match(entry.message)
            assert match
            current_guard_id = int(match.group('id'))
            pass
        elif entry.message == 'falls asleep':
            sleep_start = entry.timestamp
        else:
            assert entry.message == 'wakes up'
            guard_sleep_times.setdefault(current_guard_id, []).append((sleep_start, entry.timestamp))

    return guard_sleep_times


if __name__ == '__main__':
    main()
