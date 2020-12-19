def pretty_print(node, prefix='program', indent=0):
    print(f"{' ' * indent}{prefix}: {type(node).__name__}")
    indent += 2
    for key, value in node.__dict__.items():
        if isinstance(value, list):
            for index, node in enumerate(value):
                pretty_print(node, f'{key}[{index}]', indent)
        elif '__dict__' in dir(value):
            pretty_print(value, key, indent)
        else:
            print(f"{' ' * indent}{key}: {value}")
