class Context:
    def __init__(self):
        # In real life, contexts are much larger than just a table!
        self.locals = {}

    def add_variable(self, name, variable):
        if name in self.locals:
            raise ValueError(f'Identifier {name} already declared')
        self.locals[name] = variable

    def lookup_variable(self, name):
        if variable := self.locals.get(name):
            return variable
        raise ValueError('Identifier {name} not declared')


def analyze(program):
    program.analyze(Context())
    return program


def optimize(program):
    return program


def show_graph(program):
    entities = {}
    add_reachable_entities(program, entities)
    for node, index in entities.items():
        print(detail_line(node, index, entities))


def add_reachable_entities(node, entities):
    if not node or '__dict__' not in dir(node) or node in entities:
        return
    entities[node] = len(entities)
    for key, value in node.__dict__.items():
        if isinstance(value, list):
            for n in value:
                add_reachable_entities(n, entities)
        else:
            add_reachable_entities(value, entities)


def ref(value, entities):
    if isinstance(value, list):
        return f"[{','.join(ref(v, entities) for v in value)}]"
    elif '__dict__' in dir(value):
        return f'#{entities.get(value)}'
    return repr(value)


def detail_line(node, index, entities):
    line = f'{index} ({type(node).__name__})'
    for key, value in node.__dict__.items():
        value = ref(value, entities)
        line += '' if not value else f' {key}={value}'
    return line
