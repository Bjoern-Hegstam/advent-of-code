import re
from datetime import datetime, timedelta

from collections import namedtuple
from operator import attrgetter, itemgetter

log_entry_pattern = re.compile(r'\[(?P<timestamp>\d+-\d+-\d+ \d+:\d+)] (?P<message>.+)')
LogEntry = namedtuple('LogEntry', 'timestamp, message')


def main():
    with open('input') as f:
        lines = f.readlines()

    # lines = [
    #     '[1518-11-01 00:00] Guard #10 begins shift',
    #     '[1518-11-01 00:05] falls asleep',
    #     '[1518-11-01 00:25] wakes up',
    #     '[1518-11-01 00:30] falls asleep',
    #     '[1518-11-01 00:55] wakes up',
    #     '[1518-11-01 23:58] Guard #99 begins shift',
    #     '[1518-11-02 00:40] falls asleep',
    #     '[1518-11-02 00:50] wakes up',
    #     '[1518-11-03 00:05] Guard #10 begins shift',
    #     '[1518-11-03 00:24] falls asleep',
    #     '[1518-11-03 00:29] wakes up',
    #     '[1518-11-04 00:02] Guard #99 begins shift',
    #     '[1518-11-04 00:36] falls asleep',
    #     '[1518-11-04 00:46] wakes up',
    #     '[1518-11-05 00:03] Guard #99 begins shift',
    #     '[1518-11-05 00:45] falls asleep',
    #     '[1518-11-05 00:55] wakes up',
    # ]

    log_entries = [parse_log_entry(line) for line in lines]
    log_entries.sort(key=attrgetter('timestamp'))

    solve_part_one(log_entries)


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
    sleepiest_minutes_per_guard = {}
    most_frequent_guard_per_minute = {}

    for guard_id, sleep_durations in sleep_log.items():
        sleep_minutes_histogram = {}
        for (sleep_from, sleep_to) in sleep_durations:
            sleep_minutes = (sleep_to - sleep_from).total_seconds() / 60
            guard_sleep_times[guard_id] = sleep_minutes + guard_sleep_times.get(guard_id, 0)

            timestamp = sleep_from
            while timestamp < sleep_to:
                sleep_minutes_histogram[timestamp.minute] = 1 + sleep_minutes_histogram.get(timestamp.minute, 0)
                timestamp += timedelta(minutes=1)

        sleepiest_minutes_per_guard[guard_id] = max(sleep_minutes_histogram.items(), key=itemgetter(1))[0]
        for minute, sleep_times in sleep_minutes_histogram.items():
            if minute not in most_frequent_guard_per_minute:
                most_frequent_guard_per_minute[minute] = (guard_id, sleep_times)
            elif sleep_times > most_frequent_guard_per_minute.get(minute)[1]:
                most_frequent_guard_per_minute[minute] = (guard_id, sleep_times)

    sleepiest_guard_id = max(guard_sleep_times.items(), key=itemgetter(1))[0]
    print('Sleepiest guard id: {}'.format(sleepiest_guard_id))

    sleepiest_minute = sleepiest_minutes_per_guard[sleepiest_guard_id]
    print('Sleepiest minute: {}'.format(sleepiest_minute))

    print('Answer part 1: {}'.format(sleepiest_guard_id * sleepiest_minute))

    most_frequent_minute = max(most_frequent_guard_per_minute.items(), key=lambda item: item[1][1])[0]
    print('Most frequent minute: {}'.format(most_frequent_minute))

    (most_frequent_guard_id, sleep_times) = most_frequent_guard_per_minute[most_frequent_minute]
    print('Most frequent minute guard id: {} [sleep_times={}]'.format(most_frequent_guard_id, sleep_times))

    print('Answer part 2: {}'.format(most_frequent_minute * most_frequent_guard_id))


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
