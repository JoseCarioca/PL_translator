#   tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA } 
#   literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' }
#   
#
#  
#   funcion -> funcion TIPO ID '(' variables')' '{' Input '}'
#
#   variables -> empty | listavars
#   listavars -> listavars ',' TIPO ID | TIPO ID
#
#   Input -> empty | Input Line ';' 
#   Line  -> Declaracion | Assign Operation | PRINTF '(' CADENA ')'
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
#   fact -> ID | NUM | fcall | '!' fact | '-'fact | '(' Operation ')'
#   fcall -> ID '(' listavars ')'
# 

from sly import Lexer,Parser
import os, sys

class P1Lexer(Lexer):

    tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA} 

    literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' ,'{', '}'}
    ignore = r' \t'
    ignore_newline = r'\n+'

    NUM = r'\d+'
    INT = r'int'
    VOID = r'void'
    RETURN = r'return'
    PRINTF = r'printf'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    EQUAL = r'=='
    LE_EQ = r'<='
    GR_EQ = r'>='
    NOT_EQ = r'!='
    AND = r'&&'
    OR = r'\|\|'
    CADENA = r'\".*\"'
    

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
        self.Funciones = {}
    
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
    def Global(self,p):
        pass

    @_('Global Declaracion ";"')
    def Global(self,p):
        for var in p.Declaracion:
            if (var,"Global") in self.Variables:
                print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                self.ErrorFlag = True
            else:
                self.Variables[(var,"Global")] = None

    @_('Global Funcion')
    def Global(self,p):
        pass

    @_('TIPO ID "(" variables ")" "{" Input RETURN Operation ";" "}" ')
    def Funcion(self,p):
        if p.Input != None:
            for var in p.Input:
                if (var,p.ID) in self.Variables.keys():
                    print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var,p.ID)] = None
            
        if p.ID in self.Funciones.keys():
            print("No puedes declarar funciones con el mismo nombre.")
            self.ErrorFlag = True
        else:
            self.Funciones[p.ID] = (p.variables,"int")

    @_('VOID ID "(" variables ")" "{" Input "}" ')
    def Funcion(self,p):
        if p.Input != None:
            for var in p.Input:
                if (var,p.ID) in self.Variables.keys():
                    print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var,p.ID)] = None
            
        if p.ID in self.Funciones.keys():
            print("No puedes declarar funciones con el mismo nombre.")
            self.ErrorFlag = True
        else:
            self.Funciones[p.ID] = (p.variables,"void")

    # Concatenación de Instrucciones
    @_('')
    def Input(self,p):
        pass

    @_('Input Line ";"')
    def Input(self,p):
        if p.Line != None and p.Input != None:
            return p.Input+p.Line
        elif p.Line != None:
            return p.Line
        elif p.Input != None:
            return p.Input
    
    # Tipos de Instrucciones
    @_('Assign Operation')
    def Line(self,p):
        pass

    @_('Declaracion')
    def Line(self,p):
        return p.Declaracion
    
    @_('PRINTF "(" CADENA ")"')
    def Line(self,p):
        pass

    # Declaraciones
    @_('Declaracion2 Declaracion3')
    def Declaracion(self,p):
        if p.Declaracion2 != "int":
            return p.Declaracion2+p.Declaracion3
        else:
            return p.Declaracion3

    @_('TIPO')
    def Declaracion2(self,p):
        return p.TIPO

    @_('Declaracion2 Declaracion3 ","')
    def Declaracion2(self,p):
        if p.Declaracion2 != "int":
            return p.Declaracion2+p.Declaracion3
        else:
            return p.Declaracion3

    @_('ID')
    def Declaracion3(self,p):
        return [p.ID]

    @_('ID "=" Operation')
    def Declaracion3(self,p):
        return [p.ID]

    @_('INT')
    def TIPO(self,p):
        return "int"

    # Asignaciones
    @_('')
    def Assign(self,p):
        pass

    @_('Assign ID "="') # Retocar
    def Assign(self,p):
        pass

    # Operaciones Aritmetico-Logicas
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

    @_('')
    def variables(self,p):
        return

    @_('listavars')
    def variables(self,p):
        return p.listavars

    @_('TIPO ID')
    def listavars(self,p):
        return [p.ID]

    @_('listavars "," TIPO ID')
    def listavars(self,p):
        return p.listavars+[p.ID]

    @_('ID')
    def fact(self,p):
        return p.ID

    @_('NUM')
    def fact(self,p):
        pass
    
    @_('fcall')
    def fact(self,p):
        pass

    @_('ID "(" listavars ")"')
    def fcall(self,p):
        pass

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
        for key,value in parser.Variables.items():
            print("Variable: "+key[0]+" Ambito: "+key[1])
        for key,value in parser.Funciones.items():
            print("Funcion: "+key+" "+str(value))


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
