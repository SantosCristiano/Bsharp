# Simple Compiler for B#.

# Complete Compiler

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
        if index < len(tokens):
            if tokens[index] == 'func':
                index += 1
                if index < len(tokens):
                    name = tokens[index]
                    index += 1
                    params = []
                    while index < len(tokens) and tokens[index] != ')':
                        if tokens[index] != ',':
                            params.append(tokens[index])
                        index += 1
                    index += 1  # skip ')'
                    body = parse_block()
                    return ASTNode('function', name, [params, body])
            else:
                name = tokens[index]
                index += 1
                if index < len(tokens) and tokens[index] == '(':
                    index += 1
                    args = []
                    while index < len(tokens) and tokens[index] != ')':
                        if tokens[index] != ',':
                            args.append(tokens[index])
                        index += 1
                    index += 1  # skip ')'
                    return ASTNode('call', name, args)
                else:
                    return ASTNode('variable', name)
        return None

    def parse_block():
        nonlocal index
        statements = []
        while index < len(tokens) and tokens[index] != 'end':
            expr = parse_expression()
            if expr:
                statements.append(expr)
            if index < len(tokens) and tokens[index] == 'end':
                index += 1
                break
        return ASTNode('block', children=statements)

    return parse_block()


def generate_java(ast):
    if ast.node_type == 'block':
        return '\n'.join(generate_java(child) for child in ast.children)
    elif ast.node_type == 'function':
        params = ', '.join(f'var {param}' for param in ast.children[0])
        body = generate_java(ast.children[1])
        return f'public static Object {ast.value}({params}) {{\n    {body.replace("\n", "\n    ")}\n}}'
    elif ast.node_type == 'call':
        args = ', '.join(ast.children)
        return f'{ast.value}({args});'
    elif ast.node_type == 'variable':
        return ast.value
    return ''


# java_code = generate_java(ast)
# print(java_code)

def generate_python(ast):
    if ast.node_type == 'block':
        return '\n'.join(generate_python(child) for child in ast.children)
    elif ast.node_type == 'function':
        params = ', '.join(ast.children[0])
        body = generate_python(ast.children[1])
        return f'def {ast.value}({params}):\n    {body.replace("\n", "\n    ")}'
    elif ast.node_type == 'call':
        args = ', '.join(ast.children)
        return f'{ast.value}({args})'
    elif ast.node_type == 'variable':
        return ast.value
    return ''


# python_code = generate_python(ast)
# print(python_code)

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
// Importing a financial library
import finance_lib as fl

// Function to calculate moving average
func moving_average(prices, window_size)
    return fl.moving_average(prices, window_size)

// Using the function
prices = [100, 102, 101, 105, 110]
window_size = 3
avg = moving_average(prices, window_size)
print(avg)
"""

ast = parse_bsharp(bsharp_code)
if ast:
    csharp_code = generate_csharp(ast)
    print(csharp_code)
else:
    print("Failed to parse B# code.")
