from collections import namedtuple

StepRequirement = namedtuple('StepRequirement', 'req, step')


def main():
    with open('input') as f:
        lines = f.readlines()

    step_requirements = [StepRequirement(line[5], line[36]) for line in lines]
    step_order = determine_step_order(step_requirements)

    print('Answer part 1: {}'.format(step_order))


def determine_step_order(individual_step_requirements):
    step_order = []
    taken_steps = set()

    step_requirements = {}
    for step_req in individual_step_requirements:
        step_requirements.setdefault(step_req.step, set()).add(step_req.req)

    all_steps = set(step_req.req for step_req in individual_step_requirements).union(step_req.step for step_req in individual_step_requirements)
    available_steps = [step for step in all_steps if step not in step_requirements]

    while len(step_order) < len(all_steps):
        available_steps.sort()

        current_step = available_steps.pop(0)
        step_order.append(current_step)
        taken_steps.add(current_step)

        for step, reqs in step_requirements.items():
            if step in taken_steps:
                continue
            if step in available_steps:
                continue
            if taken_steps.issuperset(reqs):
                available_steps.append(step)

    return ''.join(step_order)


assert determine_step_order([
    StepRequirement('C', 'A'),
    StepRequirement('C', 'F'),
    StepRequirement('A', 'B'),
    StepRequirement('A', 'D'),
    StepRequirement('B', 'E'),
    StepRequirement('D', 'E'),
    StepRequirement('F', 'E')
]) == 'CABDFE'

if __name__ == '__main__':
    main()
