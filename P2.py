#   tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT }
#   literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' }
#   

#  
#   funcion -> funcion TIPO ID '(' variables')' '{' Input '}'
#   Input -> empty | Input Line ';' 
#   Line  -> Declaracion | Assign Operation
#   
#   Declaracion -> Declaracion2 Declaracion3
#   Declaracion2 -> TIPO | Declaracion2 Declaracion3 ','
#   Declaracion3 -> ID | ID '=' Operation
#   TIPO -> INT
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
#   listavars -> var | var Tipo ID
#   variables -> empty | listavars
#   listavars -> listavars ',' TIPO ID | TIPO ID
# 

from sly import Lexer,Parser
import os, sys

class P1Lexer(Lexer):

    tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT } 

    literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' ,'{', '}'}
    ignore = r' \t'
    ignore_newline = r'\n+'

    NUM = r'\d+'
    INT = r'int'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    EQUAL = r'=='
    LE_EQ = r'<='
    GR_EQ = r'>='
    NOT_EQ = r'!='
    AND = r'&&'
    OR = r'\|\|'
    

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
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
    debugfile = "parse.out"
    tokens = P1Lexer.tokens

    # Constructor
    def __init__(self):
        self.ErrorFlag = False 
        self.Variables = {}
    
    # Error
    def error(self, t):
        self.ErrorFlag = True
        print("\nCadena no Aceptada\n")
        tok = next(self.tokens, None)
        while tok:
            tok = next(self.tokens, None)
        
        return tok

    # concatenacion de funciones
    @_('')
    def funcion(self,p):
        pass

    @_('funcion TIPO ID "(" variables ")" "{" Input "}" ')
    def funcion(self,p):
        pass

    # Concatenación de Instrucciones
    @_('')
    def Input(self,p):
        pass

    @_('Input Line ";"')
    def Input(self,p):
        pass
    
    # Tipos de Instrucciones
    @_('Assign Operation')
    def Line(self,p):
        if p.Assign != None:
            self.Variables[p.Assign] = p.Operation

    @_('Declaracion')
    def Line(self,p):
        pass

    # Declaraciones
    @_('Declaracion2 Declaracion3')
    def Declaracion(self,p):
        pass

    @_('TIPO')
    def Declaracion2(self,p):
        pass

    @_('Declaracion2 Declaracion3 ","')
    def Declaracion2(self,p):
        pass

    @_('ID')
    def Declaracion3(self,p):
        if self.Variables.get(p.ID) != None:
            print("Variable \""+p.ID+"\" no puede ser declarada mas de una vez.")
            self.ErrorFlag = True
        self.Variables[p.ID] = 0

    @_('ID "=" Operation')
    def Declaracion3(self,p):
        if self.Variables.get(p.ID) != None:
            print("Variable \""+p.ID+"\" no puede ser declarada mas de una vez.")
            self.ErrorFlag = True
        self.Variables[p.ID] = p.Operation

    @_('INT')
    def TIPO(self,p):
        pass

    # Asignaciones
    @_('')
    def Assign(self,p):
        return None

    @_('Assign ID "="') # Retocar
    def Assign(self,p):
        return p.ID

    # Operaciones Aritmetico-Logicas
    @_('andOp')
    def Operation(self,p):
        return p.andOp

    @_('andOp OR Operation')
    def Operation(self,p):
        return p.andOp or p.Operation

    @_('equalOp')
    def andOp(self,p):
        return p.equalOp

    @_('equalOp AND andOp')
    def andOp(self,p):
        return p.equalOp and p.andOp
    
    @_('compOp')
    def equalOp(self,p):
        return p.compOp

    @_('compOp equalSymbol equalOp')
    def equalOp(self,p):
        if p.equalSymbol == "==":
            return p.compOp == p.equalOp
        if p.equalSymbol == "!=":
            return p.compOp != p.equalOp

    @_('addOp')
    def compOp(self,p):
        return p.addOp

    @_('addOp compSymbol compOp')
    def compOp(self,p):
        if p.compSymbol == ">=":
            return p.addOp == p.compOp
        if p.compSymbol == "<=":
            return p.compOp != p.compOp

    @_('EQUAL')
    def equalSymbol(self,p):
        return "=="

    @_('NOT_EQ')
    def equalSymbol(self,p):
        return "!="

    @_('LE_EQ')
    def compSymbol(self,p):
        return "<="

    @_('GR_EQ')
    def compSymbol(self,p):
        return ">="

    @_('prodOp "+" addOp')
    def addOp(self,p):
        return p.prodOp + p.addOp

    @_('prodOp "-" addOp')
    def addOp(self,p):
        return p.prodOp - p.addOp

    @_('prodOp')
    def addOp(self,p):
        return p.prodOp

    @_('fact "*" prodOp')
    def prodOp(self,p):
        return p.fact * p.prodOp

    @_('fact "/" prodOp')
    def prodOp(self,p):
        return p.fact / p.prodOp

    @_('fact')
    def prodOp(self,p):
        return p.fact

    @_('"-" fact')
    def fact(self,p):
        return -p.fact

    @_('"!" fact')
    def fact(self,p):
        return not p.fact

    @_('"(" Operation ")"')
    def fact(self,p):
        return p.Operation

    @_('')
    def variables(self,p):
        pass

    @_('listavars')
    def variables(self,p):
        pass

    @_('TIPO ID')
    def listavars(self,p):
        pass

    @_('listavars "," TIPO ID')
    def listavars(self,p):
        pass

    @_('ID')
    def fact(self,p):
        if self.Variables.get(p.ID) == None:
            print("Variable \""+p.ID+"\" no existe.")
            self.ErrorFlag = True
        return self.Variables.get(p.ID)

    @_('NUM')
    def fact(self,p):
        return int(p.NUM)

if __name__ == '__main__':
   
    lexer = P1Lexer()
    parser = P1Parser()
    fichero = input('escribe nombre del archivo (ejemplo: hola.c) > ')
    if not fichero: #si esta vacio
        fichero = "prueba.c"

    with open(os.path.join(sys.path[0], fichero), "r") as file:
        inputs = file.read()
    tokens = lexer.tokenize(inputs)
    parser.parse(tokens)
    #Si el flag se mantuvo en 'False' la cadena fue aceptada
    if not parser.ErrorFlag:
        print("\nCadena Aceptada\n")
        for var,value in parser.Variables.items():
            print(var+" = "+str(value)+"\n")


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
