#   tokens = {CONST,ID,INT}
#   literals = {'=','==','<=','>=','!=','&&','||','!','+','-','*','/',';'}

#   
#   Input -> empty | Input Line ';' 
#   Line  -> Assign Operation
#   Operation -> '(' Operation ')' | addOp | equalOp
#
#   Assign -> empty | Assign ID '='
#
#   equalOp -> compOp | compOp equalSymbol Operation
#   compOp -> unary | unary compSymbol Operation
#
#   compSymbol -> '>=' | '<='
#   equalSymbol -> '==' | '!='
#
#   
#   addOp -> prodOp '+' Operation
#   addOp -> prodOp '-' Operation
#   addOp -> prodOp
#
#   prodOp -> unary '*' Operation
#   prodOp -> unary '/' Operation
#   prodOp -> unary
#   
#   unary -> fact | '!' Operation | '-' Operation
#
#   fact -> ID | NUM


from sly import Lexer,Parser
import os, sys


class calcLexer(Lexer):

    tokens = {ID,NUM,EQUAL,LE_EQ, GR_EQ, NOT_EQ, AND, OR}

    literals = {'=','!','+','-','*','/',';'}
    ignore = r' \t'
    ignore_newline = r'\n+'

    NUM = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    EQUAL = r'=='
    LE_EQ = r'<='
    GR_EQ = r'>='
    NOT_EQ = r'!='
    AND = r'&&'
    OR = r'\|\|'
    

    @_(r'\d+')
    def NUM(self, t):
        #t.value = t.value
        return t
    
    #line number traking?
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno
    
    def error(self,t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index +=1




if __name__ == '__main__':
   
    lexer = calcLexer()

    inputs = ""
    with open(os.path.join(sys.path[0], "prueba.c"), "r") as file:
        inputs = file.read()
    tokens = lexer.tokenize(inputs)
    print(inputs)

    for t in tokens:
        print(t.type + " " + t.value + "\n")


    while True:
        try:
            text = input('buenas > ')
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)
            for t in tokens:
                print(t.type+ " "+ t.value+ "  \n")


