from collections import namedtuple
from operator import attrgetter

from util.constants import ALPHABET_UPPER

StepRequirement = namedtuple('StepRequirement', 'req, step')
WorkItem = namedtuple('WorkItem', 'step, finished_at')


def main():
    with open('input') as f:
        lines = f.readlines()

    step_requirements = [StepRequirement(line[5], line[36]) for line in lines]

    part_one_answer = determine_step_order(step_requirements)
    assert part_one_answer == ('CGKMUWXFAIHSYDNLJQTREOPZBV', 0)
    print('Answer part 1: {}'.format(part_one_answer))

    answer_part_two = determine_step_order(step_requirements, worker_count=5, processing_takes_time=True, base_processing_time=60)
    assert answer_part_two == ('CGUXKMFSWAIHYDNQLJTREOPZBV', 1046)
    print('Answer part 2: {}'.format(answer_part_two))


def determine_step_order(step_requirements, worker_count=1, processing_takes_time=False, base_processing_time=0):
    requirements_per_step = {}
    for step_req in step_requirements:
        requirements_per_step.setdefault(step_req.step, set()).add(step_req.req)

    all_steps = set(step_req.req for step_req in step_requirements).union(step_req.step for step_req in step_requirements)
    steps_that_can_be_started = [step for step in all_steps if step not in requirements_per_step]

    current_time = 0
    current_work_items = []
    step_order = []

    while len(step_order) < len(all_steps):
        steps_that_can_be_started.sort(reverse=True)

        # Assign available workers
        while worker_count - len(current_work_items) > 0 and steps_that_can_be_started:
            next_step = steps_that_can_be_started.pop()
            current_work_items.append(
                WorkItem(
                    next_step,
                    current_time + base_processing_time + 1 + ALPHABET_UPPER.find(next_step) if processing_takes_time else 0
                )
            )

        # Move forward to next time step when a work item is finished
        current_work_items.sort(key=attrgetter('finished_at'), reverse=True)
        current_time = current_work_items[-1].finished_at
        while current_work_items and current_work_items[-1].finished_at == current_time:
            work_item = current_work_items.pop()
            step_order.append(work_item.step)

        # Update list of steps that can be started
        reserved_steps = set(step_order).union(steps_that_can_be_started).union(wi.step for wi in current_work_items)
        for step, reqs in requirements_per_step.items():
            if step not in reserved_steps and set(step_order).issuperset(reqs):
                steps_that_can_be_started.append(step)

    result = ''.join(step_order), current_time
    print('DEBUG: Step order: {}'.format(result))
    return result


assert determine_step_order([
    StepRequirement('C', 'A'),
    StepRequirement('C', 'F'),
    StepRequirement('A', 'B'),
    StepRequirement('A', 'D'),
    StepRequirement('B', 'E'),
    StepRequirement('D', 'E'),
    StepRequirement('F', 'E')
]) == ('CABDFE', 0)

assert determine_step_order([
    StepRequirement('C', 'A'),
    StepRequirement('C', 'F'),
    StepRequirement('A', 'B'),
    StepRequirement('A', 'D'),
    StepRequirement('B', 'E'),
    StepRequirement('D', 'E'),
    StepRequirement('F', 'E')
], worker_count=2, processing_takes_time=True, base_processing_time=0) == ('CABFDE', 15)

if __name__ == '__main__':
    main()
