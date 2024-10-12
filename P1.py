#   tokens = {CONST,ID,NUM}
#   literals = {'=','==','<=','>=','!=','&&','||','!','+','-','*','/',';'}
#   
#   Input -> empty | Input Line ';' 
#   Line  -> Assign Operation
#   Operation -> orOp | '(' Operation ')'
#
#   Assign -> empty | Assign ID '='
#
#   orOp -> andOp | andOp '&&' orOp
#   andOp -> equalOp | equalOp '||' andOp
#   equalOp -> compOp | compOp equalSymbol equalOp
#   compOp -> addOp | addOp compSymbol compOp
#
#   equalSymbol -> '==' | '!='
#   compSymbol -> '>=' | '<='
#
#   addOp -> prodOp '+' addOp
#   addOp -> prodOp '-' addOp
#   addOp -> prodOp
#
#   prodOp -> unary '*' prodOp
#   prodOp -> unary '/' prodOp
#   prodOp -> unary
#   
#   unary -> fact | '!' Operation | '-' Operation
#
#   fact -> ID | NUM


from sly import Lexer,Parser
import os, sys


class P1Lexer(Lexer):

    tokens = {ID,NUM,EQUAL,LE_EQ, GR_EQ, NOT_EQ, AND, OR, ERROR}

    literals = {'=','!','+','-','*','/',';','(',')'}
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

class P1Parser(Parser):
    tokens = P1Lexer.tokens
    
    def __init__(self):
        pass

    @_('')
    def Input(self,p):
        print("\nCadena Aceptada\n")

    @_('Input Line ";"')
    def Input(self,p):
        pass
    
    @_('Assign Operation')
    def Line(self,p):
        pass

    @_('"(" Operation ")"')
    def Operation(self,p):
        pass

    @_('orOp')
    def Operation(self,p):
        pass

    @_('')
    def Assign(self,p):
        pass

    @_('Assign ID "="')
    def Assign(self,p):
        pass

    @_('andOp')
    def orOp(self,p):
        pass

    @_('andOp AND orOp')
    def orOp(self,p):
        pass

    @_('equalOp')
    def andOp(self,p):
        pass

    @_('equalOp OR andOp')
    def andOp(self,p):
        pass
    
    @_('compOp')
    def equalOp(self,p):
        pass

    @_('compOp equalSymbol equalOp')
    def equalOp(self,p):
        pass

    @_('addOp')
    def compOp(self,p):
        pass

    @_('addOp compSymbol compOp')
    def compOp(self,p):
        pass

    @_('EQUAL')
    def equalSymbol(self,p):
        pass

    @_('NOT_EQ')
    def equalSymbol(self,p):
        pass

    @_('LE_EQ')
    def compSymbol(self,p):
        pass

    @_('GR_EQ')
    def compSymbol(self,p):
        pass

    @_('prodOp "+" Operation')
    def addOp(self,p):
        pass

    @_('prodOp "-" Operation')
    def addOp(self,p):
        pass

    @_('prodOp')
    def addOp(self,p):
        pass

    @_('unary "*" Operation')
    def prodOp(self,p):
        pass

    @_('unary "/" Operation')
    def prodOp(self,p):
        pass

    @_('unary')
    def prodOp(self,p):
        pass

    @_('fact')
    def unary(self,p):
        pass

    @_('"-" Operation')
    def unary(self,p):
        pass

    @_('"!" Operation')
    def unary(self,p):
        pass

    @_('ID')
    def fact(self,p):
        pass

    @_('NUM')
    def fact(self,p):
        pass

if __name__ == '__main__':
   
    lexer = P1Lexer()
    parser = P1Parser()
    
    with open(os.path.join(sys.path[0], "prueba.c"), "r") as file:
        inputs = file.read()
    tokens = lexer.tokenize(inputs)
    parser.parse(tokens)

#    while True:
#        try:
#            text = input('buenas > ')
#        except EOFError:
#            break
#        if text:
#            tokens = lexer.tokenize(text)
#            parser.parse(tokens)
#            for t in tokens:
#                print(t.type+ " "+ t.value+ "  \n")
