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

    def add_reachable_entities(node):
        if node and '__dict__' in dir(node) and node not in entities:
            entities[node] = len(entities)
            for key, value in node.__dict__.items():
                if isinstance(value, list):
                    for n in value:
                        add_reachable_entities(n)
                else:
                    add_reachable_entities(value)

    def ref(value):
        if isinstance(value, list):
            return f"[{','.join(ref(v) for v in value)}]"
        elif '__dict__' in dir(value):
            return f'#{entities.get(value)}'
        return repr(value)

    add_reachable_entities(program)
    for node, index in entities.items():
        attributes = [f'{k}={ref(v)}' for k, v in node.__dict__.items()]
        print(f'{index} ({type(node).__name__}) {" ".join(attributes)}')
