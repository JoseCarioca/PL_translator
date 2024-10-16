#   tokens = {ID,NUM,EQUAL,LE_EQ, GR_EQ, NOT_EQ, AND, OR }
#   literals = {'=','!','+','-','*','/',';','(',')'}
#   
#   Input -> empty | Input Line ';' 
#   Line  -> Assign Operation
#
#   Assign -> empty | Assign ID '='
#
#   Operation -> andOp | andOp '||' Operation
#   andOp -> equalOp | equalOp '&&' andOp
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
#   prodOp -> fact '*' prodOp
#   prodOp -> fact '/' prodOp
#
#   fact -> ID | NUM | '!' fact | '-'fact | '(' Operation ')'
#  


from sly import Lexer,Parser
import os, sys


class P1Lexer(Lexer):

    tokens = {ID,NUM,EQUAL,LE_EQ, GR_EQ, NOT_EQ, AND, OR } 

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
    
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'//.*')
    def ignoreComment( self, t ):
        pass
    
    def error(self,t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index +=1

class P1Parser(Parser):

    tokens = P1Lexer.tokens

    def __init__(self):
        self.ErrorFlag = False 
    

    def error(self, t):
        self.ErrorFlag = True
        print("\nCadena no Aceptada\n")
        tok = next(self.tokens, None)
        while tok:
            tok = next(self.tokens, None)
        
        return tok

    @_('')
    def Input(self,p):
        pass

    @_('Input Line ";"')
    def Input(self,p):
        pass
    
    @_('Assign Operation')
    def Line(self,p):
        pass

    @_('')
    def Assign(self,p):
        pass

    @_('Assign ID "="')
    def Assign(self,p):
        pass

    @_('andOp')
    def Operation(self,p):
        pass

    @_('andOp OR Operation')
    def Operation(self,p):
        pass

    @_('equalOp')
    def andOp(self,p):
        pass

    @_('equalOp AND andOp')
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

    @_('prodOp "+" addOp')
    def addOp(self,p):
        pass

    @_('prodOp "-" addOp')
    def addOp(self,p):
        pass

    @_('prodOp')
    def addOp(self,p):
        pass

    @_('fact "*" prodOp')
    def prodOp(self,p):
        pass

    @_('fact "/" prodOp')
    def prodOp(self,p):
        pass

    @_('fact')
    def prodOp(self,p):
        pass

    @_('"-" fact')
    def fact(self,p):
        pass

    @_('"!" fact')
    def fact(self,p):
        pass

    @_('"(" Operation ")"')
    def fact(self,p):
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
    for tok in tokens:
        print(tok)
    #Si el flag se mantuvo en 'False' la cadena fue aceptada
    if not parser.ErrorFlag:
        print("Cadena Aceptada")


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
