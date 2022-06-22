import sys

# Read file, strip whitespace as well as leading and trailing parentheses and shorten keywords for easier parsing later
def parse_file(file_name):
    with open(file_name) as f:
        text = f.read()
        text = text.replace(' ', '').replace('\n', '')
        text = text.replace('sum', 's').replace('if', 'i').replace('true', 't').replace('false', 'f')
        return text

# add([2,2]) -> 4
def add(my_list):
    if len(my_list) == 2:
        return sum(my_list)
    else:
        raise ValueError("Cannot add more or less than 2 numbers")
        
# minus([2,2]) -> 4
def minus(my_list):
    if len(my_list) == 2:
        return my_list[0] - my_list[1]
    else:
        raise ValueError("Cannot subtract more or less than 2 numbers")
        
# equals([2,2]) -> True
def equals(my_list):
    if len(my_list) == 2:
        return my_list[0] == my_list[1]
    else:
        raise ValueError("Cannot check for equality between more or less than 2 expressions")
        
# if_list([True, 22, 14]) -> 22
def if_list(my_list):
    if len(my_list) == 3:
        return my_list[1] if my_list[0] else my_list[2]
    else:
        raise ValueError("Cannot carry out boolean logic on more or less than 3 expressions")

# sum_list([1,2,3) -> 6
def sum_list(my_list):
    return sum(my_list)

# Push given object to list at specified depth
def push(obj, l, depth):
    if isinstance(obj, list) or (isinstance(obj, str) and not obj.isdigit()):
        while depth:
            l = l[-1]
            depth -= 1
        
        #Replace previously shortened keys with keywords or python objs
        if isinstance(obj, list):
            l.append(obj)
        elif obj == 'i':
            l.append('if')
        elif obj == 's':
            l.append('sum')
        elif obj == 't':
            l.append(True)
        elif obj == 'f':
            l.append(False)
        else:
            l.append(obj)
    # If we pass a number, replace list instead of appending to keep in line with operator e.g
    # ['+', 5, 5] instead of ['+', [5], [5]] to remove need to unpack later
    else:
        while depth-1:
            l = l[-1]
            depth -= 1
            
        l.pop()
        l.append(int(obj))

# Recursively append expressions to nested lists
def parse_parentheses(s):
    groups = []
    depth = 0

    try:
        num = None
        for char in s:
            if char == '(':
                push([], groups, depth)
                depth += 1
            # If we find a number we append to it until we hit a ')' then push all chars
            elif char == ')':
                if num != None:
                    push(num, groups, depth)
                    num = None
                depth -= 1
            elif char.isdigit():
                if num == None:
                    num = char
                else:
                    num = num + char
            else:
                push(char, groups, depth)
    except IndexError:
        raise ValueError('Parentheses mismatch')

    if depth > 0:
        raise ValueError('Parentheses mismatch')
    else:
        return groups

# Resolve any sub expression (flattened list) to a result
def resolve_list(expression):
    operator = expression[0]
    if operator == '+':
        return add(expression[1:])
    elif operator == '-':
        return minus(expression[1:])
    elif operator == '=':
        return equals(expression[1:])
    elif operator == 'sum':
        return sum_list(expression[1:])
    elif operator == 'if':
        return if_list(expression[1:])
    else:
        return operator
    
# Recursively resolve any sub expressions until we're left with one expression (a flat list)
def flatten_list(list_to_flatten):
    flattened_list = []
    for ix, elem in enumerate(list_to_flatten):
        if not isinstance(elem, list):
            flattened_list.append(elem)
        elif isinstance(elem, list) and not any([isinstance(child, list) for child in elem]):
            flattened_list.append(resolve_list(elem))
        else:
            while(isinstance(elem, list) and any([isinstance(child, list) for child in elem])):
                elem = flatten_list(elem)
            flattened_list.append(resolve_list(elem))
    return flattened_list
    
def main():
    file = sys.argv[1]
    text = parse_file(file)
    parsed = parse_parentheses(text)
    flattened = flatten_list(parsed)
    print(resolve_list(flattened))
    
if __name__ == '__main__':
    main()
    