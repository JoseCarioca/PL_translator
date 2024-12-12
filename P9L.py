#   tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA, SCANF, CADENA_SCANF, IF, ELSE} 
#   literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' ,'{', '}', '&', '[', ']'}
#   
#   Global -> empty | Global Declaracion ';' | Global Funcion
#
#   Funcion -> TIPO_ID setCurrentFunction '(' variables ')' '{' Input RETURN Operation ';' '}'
#   Funcion -> VOID ID setCurrentFunction '(' variables ')' '{' Input '}'
#   setCurrentFunction -> empty
#
#   Input -> empty | Input Line ';' | Input Condicional | Input Bucle 
#
#   Line  -> Declaracion | Assign Operation | PRINTF '(' CADENA ')'
#   | PRINTF '(' CADENA ',' AuxPrintf ')' | SCANF '(' CADENA_SCANF ','  AuxScanf ')' 
#
#   AuxPrintf -> ID | AuxPrintf ',' ID
#   AuxScanf -> ID | '&' ID | AuxScanf ',' ID | AuxScanf ',' '&' ID
#
#   Declaracion -> TIPO_ID | TIPO_ID CORCHETES | TIPO_ID '=' Operation | Declaracion2 Declaracion3
#   Declaracion2 -> TIPO_ID ',' | TIPO_ID CORCHETES ',' | TIPO_ID '=' Operation ',' | Declaracion2 Declaracion3 ','
#   Declaracion3 -> ID | ID CORCHETES | ID '=' Operation 
#
#   TIPO_ID -> TIPO ID
#   TIPO -> INT
#   CORCHETES -> '[' NUM ']' | Corchetes '[' NUM ']'
#
#   Assign -> empty | Assign ID posCorchete '='
#
#   variables -> empty | listavars
#   listavars -> listavars ',' TIPO ASTERISCO ID posCorchete| TIPO ASTERISCO ID posCorchete
#   ASTERISCO -> empty | ASTERISCO '*'
#   posCorchete -> empty | CORCHETES
#
#   Condicional -> IF '(' Operation ')' ';' Condicional_ELSE | IF '(' Operation ')' Line ';' Condicional_ELSE | IF '(' Operation ')' '{' Input '}' Condicional_ELSE
#   Condicional_ELSE -> empty | ELSE Line ';' | ELSE '{' Input '}'
#
#   Bucle -> WHILE '(' Operation ')' ';' | WHILE '(' Operation ')' Line ';' | WHILE '(' Operation ')' '{' Input '}'
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
#   prodOp -> fact
#
#   fact -> ID | ID CORCHETES | NUM | fcall | '!' fact | '-'fact | '(' Operation ')'
#   fcall -> ID '(' entradaID ')'
#   entradaID -> empty | listaID
#   listaID -> AMPERSAN ID | listaID ',' AMPERSAN ID
#   AMPERSAN -> empty | '&'


import math
from sly import Lexer,Parser
import os, sys, re

class P1Lexer(Lexer):

    tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA, SCANF, CADENA_SCANF, IF, ELSE, WHILE} 

    literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' ,'{', '}', '&', '[', ']'}
    ignore = r' \t'
    ignore_newline = r'\n+'

    NUM = r'\d+'
    INT = r'int'
    VOID = r'void'
    RETURN = r'return'
    PRINTF = r'printf'
    SCANF = r'scanf'
    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    EQUAL = r'=='
    LE_EQ = r'<='
    GR_EQ = r'>='
    NOT_EQ = r'!='
    AND = r'&&'
    OR = r'\|\|'
    CADENA_SCANF = r'\"(%(d|i|u|f|s))+\"' # "%d" #de momento solo acepta tipos id
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
        self.rodata = {}
        self.Traduccion = ""
        self.tradGlobal = "" #para concatenar globales al final
        self.ebp = 0
        self.cadenas = 0
        self.cond_tag = 0
        self.if_else_tag = 0
        self.pila_if_else = []
    
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
        #todo tradGlobal será donde se guarde todo la primera parte
        self.Traduccion += "\t.file prueba.c\n" #cambiar a file
        #variables globales y cadenas
        self.Traduccion += "\n\t.text\n"
        pass

    @_('Global Declaracion ";"')
    def Global(self,p):
        for var in p.Declaracion:
            if (var[1],"Global") in self.Variables:
                print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                self.ErrorFlag = True
            else:
                self.Variables[(var[1],"Global")] = varAux(var[0],var[2],var[3])

    @_('Global Funcion')
    def Global(self,p):
        pass

    @_('TIPO_ID setCurrentAmbito "(" variables ")" setCurrentFunction "{" Input RETURN Operation ";" "}"')
    def Funcion(self,p):        
        self.Traduccion += "\n    popl %eax\n"
        self.Traduccion += "    movl %ebp, %esp\n"
        self.Traduccion += "    popl %ebp\n"
        self.Traduccion += "    ret\n"

    @_('VOID ID setCurrentAmbito "(" variables ")" setCurrentFunction "{" Input "}"')
    def Funcion(self,p):
        self.Traduccion += "    movl %ebp, %esp\n"
        self.Traduccion += "    popl %ebp\n"
        self.Traduccion += "    ret\n"

    @_("")
    def setCurrentAmbito(self,p):
        if isinstance(p[-1], tuple):
            self.current_function = p[-1][1]
        elif isinstance(p[-1], str):
            self.current_function = p[-1]

        self.ebp = 0

        self.Traduccion += "\t.globl " + self.current_function + "\n\t.type " + self.current_function + ", @function\n"
        self.Traduccion += self.current_function + ":\n"
        self.Traduccion += "    pushl %ebp\n"
        self.Traduccion += "    movl %esp, %ebp\n"

    @_("")
    def setCurrentFunction(self, p):
        if isinstance(p[-5], tuple):
            id = p[-5][1]
            tipo = p[-5][0]
        elif isinstance(p[-5], str):
            id = p[-5]
            tipo = "void"

        if id == "main":
            self.has_main = True
        if id in self.Funciones.keys():
            print("No puedes declarar funciones con el mismo nombre.")
            self.ErrorFlag = True
        else:
            self.Funciones[id] = (p[-2], tipo)

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
    
    @_('Input Condicional')
    def Input(self,p):
        pass

    @_('Input Bucle')
    def Input(self,p):
        pass

    # Tipos de Instrucciones
    @_('Assign Operation')
    def Line(self,p):
        self.Traduccion += p.Assign

    @_('Declaracion')
    def Line(self,p):
        if p.Declaracion != None:
            for var in p.Declaracion:
                if (var[1],self.current_function) in self.Variables.keys():
                    print("Variable '" + var[1] + "' ya declarada en '" + self.current_function + "' previamente")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var[1],self.current_function)] = varAux(var[0],var[2],var[3])
        return p.Declaracion
    
    @_('PRINTF "(" CADENA ")"')
    def Line(self,p):
        if re.findall(r'\%[a-z]',p.CADENA):
            print("Error: Faltan las variables a imprimir en el printf")
            self.ErrorFlag = True
        
        self.cadenas += 1
        self.Traduccion += "\n\t#printf"
        self.Traduccion += "\n\tpushl $s" + str(self.cadenas)
        self.Traduccion += "\n\tcall printf\n"

    @_('PRINTF "(" CADENA "," AuxPrintf ")"')
    def Line(self,p):
        lpalabras = re.findall(r'%(u|d|i)',p.CADENA)
        if not len(lpalabras):
                print("Error: Tipo a recibir no coincide con tipo de variable en printf")
                self.ErrorFlag = True
        elif len(lpalabras) != len(p.AuxPrintf):
            print("Error: No se usan el mismo numero de variables que se le pasa al printf")
            self.ErrorFlag = True
        else:
            for var in p.AuxPrintf:
                if all((var,self.current_function) != (id,ambito) for (id,ambito) in self.Variables.keys()) and all((var,"Global") != (id,ambito) for (id,ambito) in self.Variables.keys()):
                    print("Error: Variables en el printf no existen en su ambito")
                    self.ErrorFlag = True
        
        self.Traduccion += "\n\t##printf"
        for var in p.AuxPrintf:
            aux = self.Variables.get( (var, self.current_function))
            if aux is not None:
                self.Traduccion += "\n\tpushl " + str(aux.registro) + "(%ebp)"
            else:
                aux = self.Variables.get( (var, "Global"))
                self.Traduccion += "\n\tpushl " + str(var)

        self.cadenas += 1
        self.Traduccion += "\n\tpushl $s" + str(self.cadenas)
        self.Traduccion += "\n\tcall printf\n"

    @_('PRINTF "(" CADENA_SCANF "," AuxPrintf ")"')
    def Line(self,p):
        lpalabras = re.findall(r'%(u|d|i)',p.CADENA_SCANF)
        if not len(lpalabras):
                print("Error: Tipo a recibir no coincide con tipo de variable en printf")
                self.ErrorFlag = True
        elif len(lpalabras) != len(p.AuxPrintf):
            print("Error: No se usan el mismo numero de variables que se le pasa al printf")
            self.ErrorFlag = True
        else:
            for var in p.AuxPrintf:
                if all((var,self.current_function) != (id,ambito) for (id,ambito) in self.Variables.keys()) and all((var,"Global") != (id,ambito) for (id,ambito) in self.Variables.keys()):
                    print("Error: Variables en el printf no existen en su ambito")
                    self.ErrorFlag = True
        
        self.Traduccion += "\n\t##printf"
        for var in p.AuxPrintf:
            aux = self.Variables.get( (var, self.current_function))
            if aux is not None:
                self.Traduccion += "\n\tpushl " + str(aux.registro) + "(%ebp)"
            else:
                aux = self.Variables.get( (var, "Global"))
                self.Traduccion += "\n\tpushl " + str(var)

        self.cadenas += 1
        self.Traduccion += "\n\tpushl $s" + str(self.cadenas)
        self.Traduccion += "\n\tcall printf\n"

    @_('SCANF "(" CADENA_SCANF "," AuxScanf ")"')
    def Line(self,p):
        entrada = re.findall(r'%(u|d|i)',p.CADENA_SCANF)
        if len(entrada) == len(p.AuxScanf):
            for var in p.AuxScanf:
                if all( (var, self.current_function) != (id,ambito) for (id,ambito) in self.Variables.keys()) and all((var,"Global") != (id,ambito) for (id,ambito) in self.Variables.keys()):
                    print("Error: Variables en el scanf no existen en su ambito")
                    self.ErrorFlag = True
        else:
            print("Error: No se usan el mismo numero de variables que se le pasa al scanf")
            self.ErrorFlag = True

        self.cadenas += 1
        self.Traduccion += "\n\t##scanf"
        for var in p.AuxScanf:
            aux = self.Variables.get( (var, self.current_function))
            if aux is not None:
                self.Traduccion += "\n\tleal " + str(aux.registro) + "(%ebp), %eax"
                self.Traduccion += "\n\tpushl %eax" 
            else:
                aux = self.Variables.get( (var, "Global"))
                self.Traduccion += "\n\tpushl " + str(var) #id de var

        self.Traduccion += "\n\tpushl $s" + str(self.cadenas)
        self.Traduccion += "\n\tcall scanf"
        self.Traduccion += "\n\taddl " + str( (len(p.AuxScanf)+1) * 4 ) + ", %esp\n"

    # Auxiliar para PRINTF
    @_('AuxPrintf "," ID')
    def AuxPrintf(self,p):
        return p.AuxPrintf+[p.ID]

    @_('ID')
    def AuxPrintf(self,p):
        return [p.ID]

    # Auxiliar para SCANF
    @_('AuxScanf "," "&" ID')
    def AuxScanf(self,p):
        return p.AuxScanf+[p.ID]

    @_('"&" ID')
    def AuxScanf(self,p):
        return [p.ID]
    
    # Auxiliar para SCANF para punteros
    @_('AuxScanf "," ID')
    def AuxScanf(self,p):
        var = self.Variables.get((p.ID,self.current_function)) or self.Variables.get((p.ID,"Global"))
        if var == None:
            print("Error: Variable "+p.ID+" no está declarada")
            self.ErrorFlag = True
        elif var.tipo != "int*":
            print("Error: Variable "+p.ID+" NO ES UN PUNTERO")
            self.ErrorFlag = True

        return p.AuxScanf+[p.ID]
    
    @_('ID')
    def AuxScanf(self,p):
        var = self.Variables.get((p.ID,self.current_function)) or self.Variables.get((p.ID,"Global"))
        if var == None:
            print("Error: Variable "+p.ID+" no está declarada")
            self.ErrorFlag = True
        elif var.tipo != "int*":
            print("Error: Variable "+p.ID+" NO ES UN PUNTERO")
            self.ErrorFlag = True

        return [p.ID]

    #Condicionales
    @_('IF "(" Operation ")" if_aux_1 Line ";" if_aux_2 Condicional_ELSE')
    def Condicional(self,p):
        c = self.pila_if_else.pop()
        self.Traduccion += "final" + str(c) + ":\n"

    @_('IF "(" Operation ")" if_aux_1 "{" Input "}" if_aux_2 Condicional_ELSE')
    def Condicional(self,p):
        c = self.pila_if_else.pop()
        self.Traduccion += "final" + str(c) + ":\n"

    @_('IF "(" Operation ")" if_aux_1 ";" if_aux_2 Condicional_ELSE')
    def Condicional(self,p):
        c = self.pila_if_else.pop()
        self.Traduccion += "final" + str(c) + ":\n"

    @_('')
    def Condicional_ELSE(self,p):
        pass

    @_('ELSE Line ";"')
    def Condicional_ELSE(self,p):
        pass

    @_('ELSE "{" Input "}"')
    def Condicional_ELSE(self,p):
        pass

    @_('')
    def if_aux_1(self,p):
        self.if_else_tag += 1
        self.pila_if_else.append(self.if_else_tag)
        self.Traduccion += "\n"
        self.Traduccion += "\tpopl %eax\n"
        self.Traduccion += "\tcmpl &0,%eax\n"
        self.Traduccion += "\tje else" + str(self.if_else_tag) + "\n"
        return self.if_else_tag

    @_('')
    def if_aux_2(self,p):
        c = self.pila_if_else.pop()
        self.Traduccion += "\n"
        self.Traduccion += "\tjmp if_else_final" + str(c) + "\n"
        self.Traduccion += "else" + str(c) + ":\n"
        self.pila_if_else.append(c)

    # Bucles
    @_('WHILE "(" Operation ")" ";"')
    def Bucle(self,p):
        pass

    @_('WHILE "(" Operation ")" Line ";"')
    def Bucle(self,p):
        pass

    @_('WHILE "(" Operation ")" "{" Input "}"')
    def Bucle(self,p):
        pass

    # Declaraciones
    @_('Declaracion2 Declaracion3')
    def Declaracion(self,p):
        return p.Declaracion2+p.Declaracion3
    
    @_('TIPO_ID')
    def Declaracion(self,p):
        self.ebp += 4
        self.Traduccion += "## Declaracion " + p.TIPO_ID[1] + "\n"
        self.Traduccion += "    subl $4, %esp\n"
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1],-self.ebp)]
    
    @_('TIPO_ID CORCHETES')
    def Declaracion(self,p):
        arrayEBP = self.ebp + 4 #posicion 0 del array para acceder a el

        reserva = 4*math.prod(p.CORCHETES)
        self.ebp += reserva
        self.Traduccion += "    subl $" + str(reserva) + ", %esp ##dec1 " + p.TIPO_ID[1] + "\n"
        return [(p.TIPO_ID[0]+len(p.CORCHETES)*"*", p.TIPO_ID[1], p.CORCHETES, -arrayEBP)]
    
    @_('TIPO_ID "=" Operation')
    def Declaracion(self,p):
        self.ebp += 4
        self.Traduccion += "## Declaracion " + p.TIPO_ID[1] + "\n"
        self.Traduccion += "    subl $4, %esp\n"
        self.Traduccion += "    popl %eax\n"
        self.Traduccion += "    movl %eax, -" + str(self.ebp) + "(%ebp)\n"
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1],-self.ebp)]
    
    @_('TIPO_ID ","')
    def Declaracion2(self,p):
        self.current_tipo = p.TIPO_ID[0]
        self.ebp += 4
        self.Traduccion += "## Declaracion " + p.TIPO_ID[1] + "\n"
        self.Traduccion += "    subl $4, %esp\n"
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1],-self.ebp)]

    @_('TIPO_ID CORCHETES ","')
    def Declaracion2(self,p):
        arrayEBP = self.ebp + 4 #posicion 0 del array para acceder a el

        reserva = 4*math.prod(p.CORCHETES)
        self.ebp += reserva
        self.Traduccion += "    subl $" + str(reserva) + ", %esp ##dec2 " + p.TIPO_ID[1] + "\n"
        self.current_tipo = p.TIPO_ID[0]
        return [(p.TIPO_ID[0]+len(p.CORCHETES)*"*",p.TIPO_ID[1],p.CORCHETES,-arrayEBP)]

    @_('TIPO_ID "=" Operation ","')
    def Declaracion2(self,p):
        self.ebp += 4
        self.Traduccion += "## Declaracion " + p.TIPO_ID[1] + "\n"
        self.Traduccion += "    subl $4, %esp\n"
        self.Traduccion += "    popl %eax\n"
        self.Traduccion += "    movl %eax, -" + str(self.ebp) + "(%ebp)\n"
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1],-self.ebp)]

    @_('Declaracion2 Declaracion3 ","')
    def Declaracion2(self,p):
        return p.Declaracion2+p.Declaracion3
    
    @_('ID')
    def Declaracion3(self,p):
        self.ebp += 4
        self.Traduccion += "## Declaracion " + p.ID + "\n"
        self.Traduccion += "    subl $4, %esp\n"
        return [(self.current_tipo,p.ID,[1],-self.ebp)]

    @_('ID CORCHETES')
    def Declaracion3(self,p):
        reserva = 4*math.prod(p.CORCHETES)
        self.ebp += reserva
        self.Traduccion += "    subl $" + str(reserva) + ", %esp ##dec3 " + p.ID + "\n"
        return [(self.current_tipo+len(p.CORCHETES)*"*",p.ID,p.CORCHETES,-self.ebp)]

    @_('ID "=" Operation')
    def Declaracion3(self,p):
        self.ebp += 4
        self.Traduccion += "## Declaracion " + p.ID + "\n"
        self.Traduccion += "    subl $4, %esp\n"
        self.Traduccion += "    popl %eax\n"
        self.Traduccion += "    movl %eax, -" + str(self.ebp) + "(%ebp)\n"
        return [(self.current_tipo,p.ID,[1],-self.ebp)]

    @_('TIPO ID')
    def TIPO_ID(self,p):
        return (p.TIPO,p.ID)

    @_('INT')
    def TIPO(self,p):
        return "int"
    
    @_('"[" NUM "]"')
    def CORCHETES(self,p):
        return [p.NUM]
    
    @_('CORCHETES "[" NUM "]"')
    def CORCHETES(self,p):
        return p.CORCHETES + [p.NUM]
    
    # Asignaciones
    @_('')
    def Assign(self,p):
        return ""

    #se contemplan entero simple y arrays N-D
    @_('Assign ID posCorchete "="')
    def Assign(self,p):
        if (p.ID,self.current_function) not in self.Variables.keys():
            print("Variable "+p.ID+" no declarada")
            self.ErrorFlag = True
        else:
            aux = self.Variables.get((p.ID,self.current_function))

            apuntar = aux.registro
            Dimension = len(aux.tam)
            if len(p.posCorchete) != Dimension:
                self.ErrorFlag = True
            elif Dimension == 1:
                if aux.tam[0] <= p.posCorchete[0] and p.posCorchete[0] > 1: # tam = [1] indice tipo entero simple y por tanto se puede acceder
                    #posCorchetes si vacio devuelve [1] que indica llamar a entero simple
                    self.ErrorFlag = True
                    print("Acceso a " +p.ID + str(p.PosCorchete) + " fuera de rango.")
                else:
                    apuntar -= 4*(p.posCorchete[0] - 1)
            elif Dimension > 1:
                for dim, idx in zip(aux.tam, p.posCorchete):
                    if dim <= idx:
                        self.ErrorFlag = True
                        print("Acceso a " +p.ID + str(p.PosCorchete) + " fuera de rango.")
                        break
                if not self.ErrorFlag: # si no ha saltado error, y bueno en general 
                    apuntar -= linear_index(aux.tam,p.posCorchete)
     
        texto = "\n"
        texto += "    popl %eax\n"
        texto += "    movl %eax, " + str(apuntar) + "(%ebp)\n"
        return texto

    # Operaciones Aritmetico-Logicas
    @_('andOp')
    def Operation(self,p):
        return p.andOp

    @_('andOp OR Operation')
    def Operation(self,p):
        (text,self.Traduccion) = disyuncion(p.andOp,p.Operation,self.Traduccion)
        return text

    @_('equalOp')
    def andOp(self,p):
        return p.equalOp

    @_('equalOp AND andOp')
    def andOp(self,p):
        (text,self.Traduccion) = conjuncion(p.equalOp,p.andOp,self.Traduccion)
        return text
    
    @_('compOp')
    def equalOp(self,p):
        return p.compOp

    @_('compOp equalSymbol equalOp')
    def equalOp(self,p):
        if p.equalSymbol == "==":
            (text,self.Traduccion) = igual(p.compOp,p.equalOp,self.Traduccion)
        if p.equalSymbol == "!=":
            (text,self.Traduccion) = distinto(p.compOp,p.equalOp,self.Traduccion)
        return text

    @_('addOp')
    def compOp(self,p):
        return p.addOp

    @_('addOp compSymbol compOp')
    def compOp(self,p):
        if p.compSymbol == ">=":
            (text,self.Traduccion) = mayor_o_igual(p.addOp,p.compOp,self.Traduccion)
        if p.compSymbol == "<=":
            (text,self.Traduccion) = menor_o_igual(p.addOp,p.compOp,self.Traduccion)
        return text

    @_('EQUAL')
    def equalSymbol(self,p):
        return p.EQUAL

    @_('NOT_EQ')
    def equalSymbol(self,p):
        return p.NOT_EQ

    @_('LE_EQ')
    def compSymbol(self,p):
        return p.LE_EQ

    @_('GR_EQ')
    def compSymbol(self,p):
        return p.GR_EQ

    @_('prodOp "+" addOp')
    def addOp(self,p):
        (text,self.Traduccion) = suma(p.prodOp,p.addOp,self.Traduccion)
        return text

    @_('prodOp "-" addOp')
    def addOp(self,p):
        (text,self.Traduccion) = resta(p.prodOp,p.addOp,self.Traduccion)
        return text

    @_('prodOp')
    def addOp(self,p):
        return p.prodOp

    @_('fact "*" prodOp')
    def prodOp(self,p):
        (text,self.Traduccion) = multiplicacion(p.fact,p.prodOp,self.Traduccion)
        return text

    @_('fact "/" prodOp')
    def prodOp(self,p):
        (text,self.Traduccion) = division(p.fact,p.prodOp,self.Traduccion)
        return text

    @_('fact')
    def prodOp(self,p):
        #print(p.fact)
        return p.fact

    @_('"-" fact')
    def fact(self,p):
        (text,self.Traduccion) = resta_unaria(p.fact,self.Traduccion)
        return text

    @_('"!" fact')
    def fact(self,p):
        (text,self.Traduccion) = negacion(p.fact,self.Traduccion)
        return text

    @_('"(" Operation ")"')
    def fact(self,p):
        (text,self.Traduccion) = parentesis(p.Operation,self.Traduccion)
        return text

    @_('')
    def variables(self,p):
        pass

    @_('listavars')
    def variables(self,p):
        for var in p.listavars:
            if(var[1],self.current_function) in self.Variables.keys():
                print("Variable '" + var + "' ya declarada en '" + self.current_function + "' previamente")
                self.ErrorFlag = True
            else:
                self.Variables[(var[1],self.current_function)] = varAux(var[0],var[2],var[3])
        return p.listavars

    @_('TIPO ASTERISCO ID posCorchete')
    def listavars(self,p):
        self.ebpbasura = 0
        cadena = p.TIPO
        if p.ASTERISCO != None:
            cadena = cadena + p.ASTERISCO
        if p.posCorchete != [1]:
            cadena = cadena + "*" * len(p.posCorchete) #AVISO ESTO ES UN ARREGLO TEMPORAL
        return [(cadena,p.ID,p.posCorchete,self.ebpbasura+4)]

    @_('listavars "," TIPO ASTERISCO ID posCorchete')
    def listavars(self,p):
        print("posCor:" + str(p.posCorchete))
        cadena = p.TIPO
        if p.ASTERISCO != None:
            cadena = cadena + p.ASTERISCO
        if p.posCorchete != [1]:
            cadena = cadena + "*" * len(p.posCorchete)
        return p.listavars+[(cadena,p.ID,p.posCorchete,self.ebpbasura+4)] #concatenado
    
    @_('')
    def ASTERISCO(self,p):
        pass

    @_('ASTERISCO "*"')
    def ASTERISCO(self,p):
        if p.ASTERISCO == None:
            return "*"
        else: 
            return str(p.ASTERISCO+"*")
        
    @_('')
    def posCorchete(self,p):
        return [1]

    @_('CORCHETES')
    def posCorchete(self,p):
        return p.CORCHETES

    @_('ID')
    def fact(self,p):
        var = self.Variables.get((p.ID,self.current_function))
        if var is None:
            var = self.Variables.get((p.ID,self.current_function))
            if var is not None:
                i = p.ID #si la global existe
            else:
                print("Error: Variable "+p.ID+" no declarada")
                self.ErrorFlag = True
        else:
            i = var.registro

        self.Traduccion += "\n"
        texto = "\tpushl  " + str(i) + "\n"
        return [str(p.ID), texto]
    
    @_('ID CORCHETES')
    def fact(self,p):
        var = self.Variables.get((p.ID,self.current_function))
        flagGlobal = False

        if var is None:
            var = self.Variables.get((p.ID,self.current_function))
            if var is not None:
                i = str(p.ID) #si la global existe
                flagGlobal = True
            else:
                print("Error: Variable "+p.ID+" no declarada")
                self.ErrorFlag = True
        else:
            if len(p.CORCHETES) != len(var.tam):
                print("Error: Variable "+p.ID+" tamaño incorrecto")
                self.ErrorFlag = True
            else:
                if var.tam == [1]:
                    print(f"Error: {p.ID} no es tipo array")
                    self.ErrorFlag = True
                else:
                    for tam, t in zip(var.tam, p.CORCHETES):  
                        if t >= tam:  # Compara el índice con el tamaño máximo
                            print(f"Error: Posición inalcanzable de {p.ID}")
                            self.ErrorFlag = True
                            break  
              
        if var is not None and not self.ErrorFlag:
            if flagGlobal:
                i += "+" + str(linear_index(var.tam,p.CORCHETES))
                self.Traduccion += "\n"
                #self.Traduccion += "\tmovl " + str(i) + "(%ebp), %eax\n"
                texto = "\tpushl " + str(i)
            else:
                indice = linear_index(var.tam, p.CORCHETES)
                i = var.registro - indice*4
                self.Traduccion += "\n"
                #self.Traduccion += "\tmovl " + str(i) + "(%ebp), %eax\n"
                texto = "\tpushl " + str(i) + "(%ebp)"
        #si da error no lo traduce... ver qué es mejor...

        return [str(p.ID), texto]

    @_('NUM')
    def fact(self,p):
        n = str(p.NUM)
        self.Traduccion += "\n"
        texto =  "\tpushl $" + n + "\n"
        return [n, texto]
    
    @_('fcall')
    def fact(self,p):
        pass
    
    @_('ID "(" entradaID ")"')
    def fcall(self,p):
        params = self.Funciones.get(p.ID)
        if params != None:
            if len(params[0]) == len(p.entradaID):
                for i in range(len(p.entradaID)):
                    (AMP,var) = p.entradaID[i]
                    aux = self.Variables.get((var, self.current_function))
                    if aux is None: #si no existe en ambito de funcion, mirar en global
                        aux = self.Variables.get((var, "Global")) 
                    if aux is None:
                        print("Error: Variable" + var + " en llamada de " + p.ID + " no existen en su ambito")
                        self.ErrorFlag = True
                    else:
                        tipo = aux.tipo
                        if AMP is not None:
                            tipo = tipo + "*"
                        if tipo != params[0][i][0]:
                            print(tipo)
                            print(params[0][i][0])
                            print("Error: Variable " + tipo +" "+ var + " no coincide con funcion")
                            self.ErrorFlag = True  
                        if aux.tam != params[0][i][2]:
                            print("Warning: Tamaño de "+ tipo +" "+ var +" no coincide con " + params[0][i][0] + " " + params[0][i][1] + " de " + p.ID + ". Posible fuga de memoria")
                    i = i+1
            else:
                print("Error: Nº Parametros de llamada no coinciden con Nº parametros de funcion " + str(p.ID))
                self.ErrorFlag = True
        else:
            print("Error: Funcion no se encuentra declarada (en este nivel)")
            self.ErrorFlag = True

        self.Traduccion += "\n"
        cont = 0
        for a,id in p.entradaID:
            cont += 1
            aux = self.Variables.get((id, self.current_function))
            self.Traduccion += "    pushl " + str(aux.registro) +"(%ebp)\n"
        self.Traduccion += "    call " + p.ID + "\n"
        self.Traduccion += "    addl $" + str(cont*4) + " ,%esp\n"
        self.Traduccion += "    pushl %eax\n"

    @_('')
    def entradaID(self,p):
        pass

    @_('listaID')
    def entradaID(self,p):
        return p.listaID

    @_('AMPERSAN ID')
    def listaID(self,p):
        
        return [(p.AMPERSAN,p.ID)]

    @_('listaID "," AMPERSAN ID')
    def listaID(self,p):
        return p.listaID+[(p.AMPERSAN,p.ID)]
    
    @_('')
    def AMPERSAN(self,p):
        pass

    @_('"&"')
    def AMPERSAN(self,p):
        return "&"


    def parse(self, data):
        super().parse(data)
        if not self.has_main and self.Funciones != {}: #debe aceptar fichero vacio (o sin otras funciones)
            print("Error: No se encontró la función main")
            self.ErrorFlag = True

class varAux():
        def __init__(self,t,tam,n):
            self.tipo = t
            self.tam = tam
            self.registro = n

        def __str__(self):
            print(self.tipo+" "+self.tam+" "+self.registro)

def disyuncion(id1,id2,trad,cond_tag):
    text = id1 + "||" + id2
    trad += "\n"
    trad += id1[1]
    trad += id2[1]
    trad += "\tpopl %eax\n"
    trad += "\tcompl &0,%eax\n"
    trad += "\tjne cond_true" + cond_tag + "\n"
    trad += "\tpopl %eax\n"
    trad += "\tcompl &0,%eax\n"
    trad += "\tje cond_true" + cond_tag + "\n"
    trad += "\tpushl &0\n"
    trad += "\tjmp cond_final" + cond_tag + "\n"
    trad += "cond_true" + cond_tag + ":\n"
    trad += "\tpushl &1\n"
    trad += "cond_final" + cond_tag + ":\n"
    cond_tag += 1
    return (text,trad)

def conjuncion(id1,id2,trad,cond_tag):
    text = id1 + "&&" + id2
    trad += "\n"
    trad += id1[1]
    trad += id2[1]
    trad += "\tpopl %eax\n"
    trad += "\tcompl &0,%eax\n"
    trad += "\tje cond_false" + cond_tag + "\n"
    trad += "\tpopl %eax\n"
    trad += "\tcompl &0,%eax\n"
    trad += "\tje cond_false" + cond_tag + "\n"
    trad += "\tpushl &1\n"
    trad += "\tjmp cond_final" + cond_tag + "\n"
    trad += "cond_false" + cond_tag + ":\n"
    trad += "\tpushl &0\n"
    trad += "cond_final" + cond_tag + ":\n"
    cond_tag += 1
    return (text,trad)

def igual(id1,id2,trad):
    text = id1 + "==" + id2
    #trad += text + "\n"
    return (text,trad)

def distinto(id1,id2,trad):
    text = id1 + "!=" + id2
    #trad += text + "\n"
    return (text,trad)

def mayor_o_igual(id1,id2,trad):
    text = id1 + ">=" + id2
    #trad += text + "\n"
    return (text,trad)

def menor_o_igual(id1,id2,trad):
    text = id1 + "<=" + id2
    #trad += text + "\n"
    return (text,trad)

def suma(id1,id2,trad):
    text = "\n"
    text += id1[1]
    text += id2[1]
    text += "\tpopl %ebx\n"
    text += "\tpopl %eax\n"
    text += "\taddl %ebx, %eax\n"
    text += "\tpushl %eax\n"
    trad += text
    return (text,trad)

def resta(id1,id2,trad):
    text = "\n"
    text += id1[1]
    text += id2[1]
    text += "\tpopl %ebx\n"
    text += "\tpopl %eax\n"
    text += "\tsubl %ebx, %eax\n"
    text += "\tpushl %eax\n"
    trad += text
    return (text,trad)

def multiplicacion(id1,id2,trad):
    text = "\n"
    text += id1[1]
    text += id2[1]
    text += "\tpopl %ebx\n"
    text += "\tpopl %eax\n"
    text += "\timull %ebx, %eax\n"
    text += "\tpushl %eax\n"
    trad += text
    return (text,trad)

def division(id1,id2,trad):
    text = "\n"
    text += id1[1]
    text += id2[1]
    text += "\tpopl %ebx\n"
    text += "\tpopl %eax\n"
    text += "\tcdq\n"
    text += "\tdivl %ebx"
    text += "\tpushl %eax\n"
    trad += text
    return (text,trad)

def resta_unaria(id,trad):
    text = "\n"
    text += id[1]
    text += "\tpopl %ebx\n"
    text += "\tmovl &0,%eax\n"
    text += "\tsubl %ebx, %eax\n"
    text += "\tpushl %eax\n"
    trad += text
    return (text,trad)

def negacion(id,trad):
    text = "!" + id
    #trad += text + "\n"
    return (text,trad)

def parentesis(id, trad):
    text = "(" + id +")"
    #trad += text + "\n"
    return (text,trad)

"""Def auxiliar para calculo de indice Lineal de tamaño N"""
def linear_index(dims, subindex):
    """
        dims (list): Lista de Dimension de array (empieza en 1)
        subindex (list): Lista de indices pedidos (empieza en 0)

    Returns:
        int: Indice lineal para posicion en pila
    """
    stride = 1
    linear_idx = 0

    # Iterate from the last dimension to the first
    for dim, idx in zip(reversed(dims), reversed(subindex)):
        linear_idx += idx * stride
        stride *= dim

    return linear_idx

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
        with open(os.path.join(sys.path[0], "traduccion.txt"), "w") as file:
            file.write(parser.Traduccion)
        print("VARIABLES")
        for key,value in parser.Variables.items():
            print("Variable: "+key[0]+" Ambito: "+key[1]+" Tipo: "+value.tipo+" Tamaño: "+str(value.tam) +" EBP: "+str(value.registro) )
        print("\nFUNCIONES")
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
