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
        elif curr_tok.isalnum():
            next_char()
            if curr_pos >= 0:
                next_tok = decl[curr_pos]
                while next_tok.isalnum():
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
        flag = flag and c.isalnum()
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
    global id_of_fulldecl
    d = parse_declarator()
    ds = parse_declspecs()
    d.extend([id])
    d = d[::-1]
    d.extend(ds)
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
    l.extend(parse_direct_declarator())
    l.extend(parse_pointer())
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
    elif tokens[tok_pos] == ')':
        save_pos = tok_pos
        try:
            consume()
            if tokens[tok_pos] == '(':
                consume()
                l.extend(parse_direct_declarator())
            else:
                m = parse_declarator()
                if is_tok_declspecs():
                    tok_pos = save_pos
                    consume()
                    l.extend(parse_parameter_type_list())
                    if tokens[tok_pos] == '(':
                        consume()
                    else:
                        raise ParserError("expected '('")
                    l.extend(parse_direct_declarator())
                elif tokens[tok_pos] == '(':
                    consume()
                    l.extend(m)
                else:
                    raise ParserError("expected '('")
        except:
            raise ParserError("parsing direct declarator failed")
    elif tokens[tok_pos] == ']':
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
    l = ["of","]"]
    if tokens[tok_pos] == '[':
        pass
    elif is_alnum(tokens[tok_pos]):
        l.extend([tokens[tok_pos]])
        consume()
    else:
        raise ParserError("parsing constant expression failed")
    l.extend(["["])
    l.extend(["array"])
    return l

depth = 0

def parse_parameter_type_list():
    global depth
    params = ["returning", ")"]
    depth += 1
    while True:
        if tokens[tok_pos] == '(':
            params.extend(["("])
            break
        else:
            params.extend(parse_declaration()[::-1])
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
    params.extend(["function"])
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