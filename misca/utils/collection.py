def make_groups(items, group_size: int):
    groups = []
    current_group = []

    for item in items:
        if len(current_group) < group_size:
            current_group.append(item)
        else:
            groups.append(tuple(current_group))
            current_group = [item]

    if len(current_group) > 0:
        groups.append(tuple(current_group))

    return groups
