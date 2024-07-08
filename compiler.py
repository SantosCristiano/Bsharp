# Compilador simples para B#.

# Compilador Completo

import re

class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children or []

def parse_bsharp(code):
    tokens = re.findall(r'\w+|\S', code)
    index = 0
    
    def parse_expression():
        nonlocal index
        if tokens[index] == 'func':
            index += 1
            name = tokens[index]
            index += 1
            params = []
            while tokens[index] != ')':
                if tokens[index] != ',':
                    params.append(tokens[index])
                index += 1
            index += 1  # skip ')'
            body = parse_block()
            return ASTNode('function', name, [params, body])
        else:
            name = tokens[index]
            index += 1
            if tokens[index] == '(':
                index += 1
                args = []
                while tokens[index] != ')':
                    if tokens[index] != ',':
                        args.append(tokens[index])
                    index += 1
                index += 1  # skip ')'
                return ASTNode('call', name, args)
            else:
                return ASTNode('variable', name)

    def parse_block():
        nonlocal index
        statements = []
        while index < len(tokens) and tokens[index] != 'end':
            statements.append(parse_expression())
            if tokens[index] == 'end':
                break
        return ASTNode('block', children=statements)

    return parse_block()

def generate_csharp(ast):
    if ast.node_type == 'block':
        return '\n'.join(generate_csharp(child) for child in ast.children)
    elif ast.node_type == 'function':
        params = ', '.join(f'var {param}' for param in ast.children[0])
        body = generate_csharp(ast.children[1])
        return f'public static dynamic {ast.value}({params}) {{\n    {body.replace("\n", "\n    ")}\n}}'
    elif ast.node_type == 'call':
        args = ', '.join(ast.children)
        return f'{ast.value}({args});'
    elif ast.node_type == 'variable':
        return ast.value
    return ''

bsharp_code = """
// Importando uma biblioteca financeira
import finance_lib as fl

// Função para calcular a média móvel
func moving_average(prices, window_size)
    return fl.moving_average(prices, window_size)

// Usando a função
prices = [100, 102, 101, 105, 110]
window_size = 3
avg = moving_average(prices, window_size)
print(avg)
"""

ast = parse_bsharp(bsharp_code)
csharp_code = generate_csharp(ast)
print(csharp_code)
