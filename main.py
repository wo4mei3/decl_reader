decl = ""
curr_pos = 0
tokens = []
explanation = []

def read():
    global decl
    global curr_pos
    decl = input("> ")
    curr_pos = len(decl) - 1

def next_char():
    global curr_pos
    curr_pos = curr_pos - 1

def lex():
    curr_tok = ""
    global tokens
    global curr_pos
    while curr_pos >= 0:
        curr_tok = decl[curr_pos]
        if curr_tok.isspace():
            curr_tok = ""
            next_char()
        elif curr_tok.isalnum() or curr_tok == '_':
            next_char()
            if curr_pos >= 0:
                next_tok = decl[curr_pos]
                while next_tok.isalnum() or next_tok == '_':
                    curr_tok += next_tok
                    next_char()
                    if curr_pos >= 0:
                        next_tok = decl[curr_pos]
                    else:
                        break
            tokens.append(curr_tok[::-1])
            curr_tok = ""
        elif curr_tok == '*':
            tokens.append(curr_tok)
            curr_tok = ""
            next_char()  
        elif curr_tok == ',':
            tokens.append(curr_tok)
            curr_tok = ""
            next_char()
        elif curr_tok == ';':
            tokens.append(curr_tok)
            curr_tok = ""
            next_char()
        elif curr_tok == '(':
            tokens.append(curr_tok)
            curr_tok = ""
            next_char()
        elif curr_tok == ')':
            tokens.append(curr_tok)
            curr_tok = ""
            next_char()
        elif curr_tok == '[':
            tokens.append(curr_tok)
            curr_tok = ""
            next_char()
        elif curr_tok == ']':
            tokens.append(curr_tok)
            curr_tok = ""
            next_char()
        elif curr_tok == ';':
            tokens.append(curr_tok)
            next_char()
        else:
            print("error")
            break

def is_alnum(s):
    flag = True
    for c in s:
        flag = flag and (c.isalnum() or c == '_')
    return flag

class ParserError(Exception):
    pass

tok_pos = 0

def consume():
    global tok_pos
    tok_pos = tok_pos + 1

def parse_full_declaration():
    l = []
    if tokens[tok_pos] == ';':
        consume()
        l = parse_declaration()
    else:
        raise ParserError("expected ';'")
    return l


def parse_declaration():
    global id
    d = parse_declarator()
    ds = parse_declspecs()
    d.extend([id])  # First of all, We read identifier of declarator by which names the variable declares.
    d = d[::-1]  # Second, We read the rules applied while parsing declarator in the inverse order.
    d.extend(ds)  # Finally, We read declaration specifiers
    return d


def is_tok_declspecs():
    if tok_pos < len(tokens):
        if is_alnum(tokens[tok_pos]):
            return True
        else:
            return False
    else:
        return False

def parse_declspecs():
    l = []
    if is_tok_declspecs():
        l.extend([tokens[tok_pos]])
        consume()
        l.extend(parse_declspecs())
    else:
        pass
    return l

def parse_declarator():
    l = []
    d = parse_direct_declarator()
    p = parse_pointer()
    l.extend(p)
    l.extend(d)
    return l
    
def parse_pointer():
    l = []
    m = parse_type_qualifer()
    if tokens[tok_pos] == '*':
        consume()
        try:
            l.extend(parse_pointer())
            l.extend(["pointer of"])
            l.extend(m)
        except:
            return l
    else:
        l
    return l 

  
def parse_type_qualifer():
    l = []
    if tokens[tok_pos] == "const" or tokens[tok_pos] == "volatile":
        l.extend([tokens[tok_pos]])
        consume()
        l.extend(parse_type_qualifer())
        return l
    else:
        pass
    return l

id = ""

def parse_direct_declarator():
    global tok_pos
    global id
    l = []
    if is_alnum(tokens[tok_pos]):
        id = tokens[tok_pos]
        consume()
    elif tokens[tok_pos] == ')':  # if current rightmost token is RPAREN, Two rules can be the applying candidates.
        save_pos = tok_pos
        try:
            consume()
            if tokens[tok_pos] == '(':  # if LPAREN folows, it is empty parameter type list.
                l.extend(parse_parameter_type_list())
                if tokens[tok_pos] == '(':
                    consume()
                else:
                    raise ParserError("expected '('")
                l.extend(parse_direct_declarator())
            else:
                m = parse_declarator()  # We try parsing declarator, then check it out that if declaration specifiers follows.
                if is_tok_declspecs():  # if declspecs follows after parsing declarator, it is parameter type list.
                    tok_pos = save_pos  # We restore tok_pos in order to parse whole parameter type list.
                    consume()
                    l.extend(parse_parameter_type_list())
                    if tokens[tok_pos] == '(':
                        consume()
                    else:
                        raise ParserError("expected '('")
                    l.extend(parse_direct_declarator())
                elif tokens[tok_pos] == '(':  # if LPAREN follows after parsing declarator, it is just a nested declarator.
                    consume()
                    l.extend(m)
                else:
                    raise ParserError("expected '('")
        except:
            raise ParserError("parsing direct declarator failed")
    elif tokens[tok_pos] == ']':  #if rightmost token is RBRACKET, We are reading the suffix of an array.
        consume()
        l.extend(parse_constant())
        if tokens[tok_pos] == '[':
            consume()
        else:
            raise ParserError("expected '[")
        l.extend(parse_direct_declarator())
    else:
        raise ParserError("parsing direct declarator failed")
    return l
        
def parse_constant():
    l = ["of","]"]  # notice this list is going to eventually be revered. "of" follows after the closing bracket.
    if tokens[tok_pos] == '[':
        pass
    elif is_alnum(tokens[tok_pos]):
        l.extend([tokens[tok_pos]])
        consume()
    else:
        raise ParserError("parsing constant expression failed")
    l.extend(["["])
    l.extend(["array"])  # consider l is going to be reversed, you will find the string "array" appears in the beginning.
    return l

depth = 0

def parse_parameter_type_list():
    global depth
    params = ["returning", ")"]  # notice this list is going to be revesed again. same as in parse_constant()
    depth += 1
    while True:
        if tokens[tok_pos] == '(':
            params.extend(["("])
            break
        else:
            params.extend(parse_declaration()[::-1])  # consider the result of parse_declaration() is already reversed once, We should reverse then again.
            if tokens[tok_pos] == ',':
                params.extend([","])
                consume()
                continue
            elif tokens[tok_pos] == '(':
                params.extend(["("])
                break
            else:
                raise ParserError("parsing parameter type list failed")
    depth -= 1
    params.extend(["function"])  # This string will be appear in the beginning in function part of the output.
    return params


def parse():
    return parse_full_declaration()

if __name__ == '__main__':
    while True:
        read()
        lex()
        result = parse()
        print("")
        print(" ".join(result))
        print("")