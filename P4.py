#   tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA, SCANF, CADENA_SCANF } 
#   literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' }
#   
#   Global -> empty | Global Declaracion ';' | Global Funcion
#
#   Funcion -> TIPO_ID '(' variables ')' '{' Input RETURN Operation ';' '}'
#   Funcion -> VOID ID '(' variables ')' '{' Input '}'
#
#   variables -> empty | listavars
#   listavars -> listavars ',' TIPO ID | TIPO ID
#
#   Input -> empty | Input Line ';' 
#   Line  -> Declaracion | Assign Operation | PRINTF '(' CADENA ',' AuzPrintf ')' | SCANF '(' CADENA_SCANF ')'
#   AuxPrintf -> empty | AuxPrintf ',' ID
#   
#   Declaracion -> TIPO_ID | TIPO_ID '=' Operation | Declaracion2 Declaracion3
#   Declaracion2 -> TIPO_ID ',' | TIPO_ID '=' Operation ',' | Declaracion2 Declaracion3 ','
#   Declaracion3 -> ID | ID '=' Operation
#   TIPO_ID -> TIPO ID
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
import os, sys, re

class P1Lexer(Lexer):

    tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA_SCANF, CADENA, SCANF } 

    literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' ,'{', '}','&'}
    ignore = r' \t'
    ignore_newline = r'\n+'

    NUM = r'\d+'
    INT = r'int'
    VOID = r'void'
    RETURN = r'return'
    PRINTF = r'printf'
    SCANF = r'scanf'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    EQUAL = r'=='
    LE_EQ = r'<='
    GR_EQ = r'>='
    NOT_EQ = r'!='
    AND = r'&&'
    OR = r'\|\|'
    CADENA_SCANF = r'\"%(d|i|u|f|s|)\"' # "%d" #de momento solo acepta tipos id
    CADENA = r'\"[^\"\']*\"'

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
        self.has_main = False
        self.Variables = {}
        self.Funciones = {}
        self.Traduccion = ""
    
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

    @_('TIPO_ID "(" variables ")" "{" Input RETURN Operation ";" "}"')
    def Funcion(self,p):
        if p.variables != None:
            for var in p.variables:
                if(var,p.TIPO_ID[1]) in self.Variables.keys():
                    print("variable '" + var + "' ya declarada en '" + p.TIPO_ID[1] + "' previamente")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var,p.TIPO_ID[1])] = None
        if p.TIPO_ID[1] =="main":
            self.has_main = True
        if p.Input != None:
            p.Input.pop(0) # el primer elemento es el nombre de la funcion
            for var in p.Input:
                if (var,p.TIPO_ID[1]) in self.Variables.keys():
                    print("variable '" + var + "' ya declarada en '" + p.TIPO_ID[1] + "' previamente")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var,p.TIPO_ID[1])] = None
            
        if p.TIPO_ID[1] in self.Funciones.keys():
            print("No puedes declarar funciones con el mismo nombre.")
            self.ErrorFlag = True
        else:
            self.Funciones[p.TIPO_ID[1]] = (p.variables,p.TIPO_ID[0])

    @_('VOID ID "(" variables ")" "{" Input "}"')
    def Funcion(self,p):
        if p.variables != None:
            for var in p.variables:
                if(var,p.ID) in self.Variables.keys():
                    print("variable '" + var + "' ya declarada en '" + p.ID + "' previamente")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var,p.ID)] = None
        if p.ID =="main":
            self.has_main = True
        if p.Input != None:
            p.Input.pop(0) # el primer elemento es el nombre de la funcion
            for var in p.Input:
                if (var,p.ID) in self.Variables.keys():
                    print("variable '" + var + "' ya declarada en '" + p.ID + "' previamente")
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
        self.print = None
        if isinstance(p[-5], tuple):
            print("ambito es: "+ str(p[-5][1]))
            return [p[-5][1]]
        elif isinstance(p[-5], str):
            print("ambito de funcion void es: "+ str(p[-5]))
            return [p[-5]]

    @_('Input Line ";"')
    def Input(self,p): 
        self.current_function = p.Input[0] #ambito (no es la mejor solucion, quizas debamos subir todo y tener fun auxiliares en Funcion)
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
        if re.findall(r'\%[a-z]',p.CADENA):
            print("Error: Faltan las variables a imprimir en el printf")
            self.ErrorFlag = True

    @_('PRINTF "(" CADENA "," AuxPrintf ")"')
    def Line(self,p):
        print("ambito printf con vars: " + str(self.current_function))
        lpalabras = re.findall(r'\%[a-z]',p.CADENA)
        if len(lpalabras) == len(p.AuxPrintf):
             print("Num % y num vars igual :)")
        else:
            print("Warning: argumentos en printf no coinciden")
            self.ErrorFlag = True
        self.print = lpalabras+p.AuxPrintf # no lo vamos a usar
      

    @_('AuxPrintf "," ID')
    def AuxPrintf(self,p): 
        return p.AuxPrintf+[p.ID]


    @_('ID')
    def AuxPrintf(self,p):
        return [p.ID]

    @_('SCANF "(" CADENA_SCANF "," "&" ID ")"')
    def Line(self,p):
        flag =  False
        for (id,ambito) in self.Variables.keys():
            if id == p.ID and (ambito == self.current_function or ambito == 'Global'):
                flag = True
                break
        if flag:    
            if any(char in p.CADENA_SCANF for char in "udi"):
                print("SE METE TIPO ENTERO en " + str(p.ID))
            else:
                print("SE PIDE DE OTRO TIPO")
        else:
            print("Error: variable en SCANF no declarada")
            self.ErrorFlag = True

        

    # Declaraciones
    @_('Declaracion2 Declaracion3')
    def Declaracion(self,p):
        return p.Declaracion2+p.Declaracion3
        
    @_('TIPO_ID')
    def Declaracion(self,p):
        return [p.TIPO_ID[1]]
    
    @_('TIPO_ID "=" Operation')
    def Declaracion(self,p):
        return [p.TIPO_ID[1]]

    @_('TIPO_ID "=" Operation ","')
    def Declaracion2(self,p):
        return [p.TIPO_ID[1]]
    
    @_('TIPO_ID ","')
    def Declaracion2(self,p):
        return [p.TIPO_ID[1]]

    @_('Declaracion2 Declaracion3 ","')
    def Declaracion2(self,p):
        return p.Declaracion2+p.Declaracion3

    @_('ID')
    def Declaracion3(self,p):
        return [p.ID]

    @_('ID "=" Operation')
    def Declaracion3(self,p):
        return [p.ID]
    
    @_('TIPO ID')
    def TIPO_ID(self,p):
        return (p.TIPO,p.ID)

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
        # self.Traduccion = resta_unaria(p.fact,self.Traduccion)
        pass

    @_('"!" fact')
    def fact(self,p):
        # self.Traduccion = negacion(p.fact,self.Traduccion)
        pass

    @_('"(" Operation ")"')
    def fact(self,p):
        # self.Traduccion = parentesis(p.fact,self.Traduccion)
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
        return p.NUM
    
    @_('fcall')
    def fact(self,p):
        pass

    @_('ID "(" listavars ")"')
    def fcall(self,p):
        pass

    def parse(self, data):
        super().parse(data)
        if not self.has_main:
            print("Error: No se encontró la función main")
            self.ErrorFlag = True

def negacion(id,trad):
    trad += "!" + str(id)
    return (id,trad)

def resta_unaria(id,trad):
    trad += "-" + str(id)
    return (id, trad)

def parentesis(id, trad):
    trad += "(" + str(id) +")"
    return (id,trad)

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
    for t in tokens:
        print(t.type+ " "+ t.value+ "  \n")
    #Si el flag se mantuvo en 'False' la cadena fue aceptada
    if not parser.ErrorFlag:
        print("\nCadena Aceptada\n")
        with open(os.path.join(sys.path[0], "traduccion.txt"), "w") as file:
            file.write(parser.Traduccion)
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
