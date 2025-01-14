#   tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA, SCANF, CADENA_SCANF, IF, ELSE} 
#   literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' ,'{', '}', '&', '[', ']'}
#   
#   Global -> empty | Declaracion ';' Global | Funcion Global
#
#   Funcion -> TIPO_ID '(' variables ')' '{' Input RETURN Operation ';' '}'
#   Funcion -> VOID ID '(' variables ')' '{' Input '}'
#
#   Input -> empty | Input Line ';' | Input Condicional | Input Bucle 
#
#   Line  -> Declaracion | Assign Operation | PRINTF '(' CADENA ')'
#           | PRINTF '(' CADENA ',' AuxPrintf ')' | Line -> PRINTF '(' CADENA_SCANF ',' AuxPrintf ')' 
#           | SCANF '(' CADENA_SCANF ','  AuxScanf ')' 
#
#   AuxPrintf -> ID posCorchete | AuxPrintf ',' ID posCorchete
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
#   Operation -> andOp | andOp OR Operation
#   andOp -> equalOp | equalOp AND andOp
#   equalOp -> compOp | compOp equalSymbol equalOp
#   compOp -> addOp | addOp compSymbol compOp
#
#   equalSymbol -> EQUAL | NOT_EQ
#   compSymbol -> GR_EQ | LE_EQ
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
#   listaID -> AMPERSAN ID posCorchete | listaID ',' AMPERSAN ID posCorchete
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
    CADENA_SCANF = r'\"(%(d|i|u|f|s)| )+\"' # "%d" #de momento solo acepta tipos id
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
        self.cadenas = []
        self.sectiondata = "" #seccion de datos globales
        self.Traduccion = ""
        self.tradGlobal = "" #para concatenar globales al final
        self.ebp = 0
        self.ncadenas = 0
        self.cond_tag = 0
        self.if_else_tag = 0
        self.while_tag = 0
        self.pila_if_else = []
        self.pila_while = []
    
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
        # Inicializar tradGlobal con el archivo y sección de texto
        self.tradGlobal = "\t.file prueba.c\n"
        self.tradGlobal += "\t.section .rodata\n"

        # Agregar las cadenas en el orden correcto
        for i, cadena in enumerate(self.cadenas, start=1):
            self.tradGlobal += f".LC{i}:\n"
            self.tradGlobal += f"\t{cadena}\n"
        
        self.tradGlobal += "\n"
        # Combinar con el resto de la traducción
        #self.Traduccion = self.tradGlobal + self.Traduccion

    @_('Global Declaracion ";"')
    def Global(self,p):
        for var in p.Declaracion:
            if var[3] == 0:
                if (var[1],"Global") in self.Variables:
                    print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var[1],"Global")] = varAux(var[0],var[2],-1)
                self.sectiondata += ".lcomm " + var[1] + ", 4\n"
            
            elif var[3] == 1:
                if (var[1],"Global") in self.Variables:
                    print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var[1],"Global")] = varAux(var[0],var[2],-1)
                
                reserva = 4*math.prod(var[2])
                self.sectiondata += ".lcomm " + var[1] + ", " + str(reserva) + "\n"

            else:
                if (var[1],"Global") in self.Variables:
                    print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var[1],"Global")] = varAux(var[0],var[2],-1)
                
                self.sectiondata += ".lcomm " + var[1] + ", 4\n"
                self.sectiondata += var[1] + ":\n"
                self.sectiondata += "\t.long " + str(0) + "\n"

        return p.Declaracion

    @_('Global Funcion')
    def Global(self,p):
        pass

    @_('TIPO_ID setCurrentAmbito "(" variables ")" setCurrentFunction "{" Input RETURN Operation ";" "}"')
    def Funcion(self,p):        
        self.Traduccion += "\n\tpopl %eax\n"
        self.Traduccion += "\tmovl %ebp, %esp\n"
        self.Traduccion += "\tpopl %ebp\n"
        self.Traduccion += "\tret\n"

    @_('VOID ID setCurrentAmbito "(" variables ")" setCurrentFunction "{" Input "}"')
    def Funcion(self,p):
        self.Traduccion += "\n\tmovl %ebp, %esp\n"
        self.Traduccion += "\tpopl %ebp\n"
        self.Traduccion += "\tret\n"

    @_("")
    def setCurrentAmbito(self,p):
        if isinstance(p[-1], tuple):
            self.current_function = p[-1][1]
        elif isinstance(p[-1], str):
            self.current_function = p[-1]

        self.ebp = 0

        self.Traduccion += "\t.globl " + self.current_function + "\n\t.type " + self.current_function + ", @function\n"
        self.Traduccion += self.current_function + ":\n"
        self.Traduccion += "\tpushl %ebp\n"
        self.Traduccion += "\tmovl %esp, %ebp\n"

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
        for var in p.Declaracion:
            if var[3] == 0:
                self.ebp += 4

                if (var[1],self.current_function) in self.Variables:
                    print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var[1],self.current_function)] = varAux(var[0],var[2],-self.ebp)

                self.Traduccion += "\n\tsubl $4, %esp\n"
            
            elif var[3] == 1:
                arrayEBP = self.ebp + 4 #posicion 0 del array para acceder a el
                reserva = 4*math.prod(var[2])
                self.ebp += reserva

                if (var[1],self.current_function) in self.Variables:
                    print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var[1],self.current_function)] = varAux(var[0],var[2],-arrayEBP)

                self.Traduccion += "\n\tsubl $" + str(reserva) + ", %esp\n"

            else:
                self.ebp += 4

                if (var[1],self.current_function) in self.Variables:
                    print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var[1],self.current_function)] = varAux(var[0],var[2],-self.ebp)

                self.Traduccion += "\n\tsubl $4, %esp\n"
                self.Traduccion += "\tpopl %eax\n"
                self.Traduccion += "\tmovl %eax, -" + str(self.ebp) + "(%ebp)\n"

        return p.Declaracion
    
    @_('PRINTF "(" CADENA ")"')
    def Line(self,p):
        if re.findall(r'\%[a-z]',p.CADENA):
            print("Error: Faltan las variables a imprimir en el printf")
            self.ErrorFlag = True
        
        if not self.ErrorFlag:
            self.cadenas += [p.CADENA]
            self.ncadenas += 1
            self.Traduccion += "\n\tpushl $LC" + str(self.ncadenas) + "\n"
            self.Traduccion += "\tcall printf\n"
            self.Traduccion += "\taddl $4, %esp\n"

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
                if all((var[0],self.current_function) != (id,ambito) for (id,ambito) in self.Variables.keys()) and all((var[0],"Global") != (id,ambito) for (id,ambito) in self.Variables.keys()):
                    print("Error: Variables en el printf no existen en su ambito")
                    self.ErrorFlag = True
        
        self.Traduccion += "\n"
        for id, corchetes in p.AuxPrintf:
            var,flagGlobal = variable_in_ambito(self.Variables, id, self.current_function, self.ErrorFlag)
            if not self.ErrorFlag:
                if flagGlobal:
                    self.Traduccion += "\tpushl $" + id + "\n" #id de var
                else:
                    pos = var.registro
                    if corchetes:
                        pos -= 4*linear_index(var.tam,corchetes)
                    self.Traduccion += "\tpushl " + str(pos) + "(%ebp)\n" 

        if not self.ErrorFlag:
            self.cadenas += [p.CADENA]
            self.ncadenas += 1
            self.Traduccion += "\tpushl $LC" + str(self.ncadenas) + "\n"
            self.Traduccion += "\tcall printf\n"
            self.Traduccion += "\taddl $" + str((len(p.AuxPrintf)+1) * 4 ) + ", %esp\n"

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
                if all((var[0],self.current_function) != (id,ambito) for (id,ambito) in self.Variables.keys()
                       ) and all((var[0],"Global") != (id,ambito) for (id,ambito) in self.Variables.keys()):
                    print("Error: Variables en el printf no existen en su ambito")
                    self.ErrorFlag = True
        
        self.Traduccion += "\n"
        for id, corchetes in p.AuxPrintf:
            var,flagGlobal = variable_in_ambito(self.Variables, id, self.current_function, self.ErrorFlag)
            if not self.ErrorFlag:
                if flagGlobal:
                    self.Traduccion += "\tpushl $" + id + "\n" #id de var
                else:
                    pos = var.registro
                    if corchetes:
                        pos -= 4*linear_index(var.tam,corchetes)
                    self.Traduccion += "\tpushl " + str(pos) + "(%ebp)\n" 

        if not self.ErrorFlag:
            self.cadenas += [p.CADENA_SCANF]
            self.ncadenas += 1
            self.Traduccion += "\tpushl $LC" + str(self.ncadenas) + "\n"
            self.Traduccion += "\tcall printf\n"
            self.Traduccion += "\taddl $" + str((len(p.AuxPrintf)+1) * 4 ) + ", %esp\n"

    @_('SCANF "(" CADENA_SCANF "," AuxScanf ")"')
    def Line(self,p):
        entrada = re.findall(r'%(u|d|i)',p.CADENA_SCANF)
        if len(entrada) != len(p.AuxScanf):
            print("Error: No se usan el mismo numero de variables que se le pasa al scanf")
            self.ErrorFlag = True
        else:
            for var in p.AuxScanf:
                if all( (var, self.current_function) != (id,ambito) for (id,ambito) in self.Variables.keys()
                       ) and all((var,"Global") != (id,ambito) for (id,ambito) in self.Variables.keys()):
                    print("Error: Variables en el scanf no existen en su ambito")
                    self.ErrorFlag = True
        
        self.Traduccion += "\n"
        for id in p.AuxScanf:
            var,flagGlobal = variable_in_ambito(self.Variables, id, self.current_function, self.ErrorFlag)
            if not self.ErrorFlag:
                if flagGlobal:
                    self.Traduccion += "\tpushl $" + id + "\n" #id de var
                else:
                    self.Traduccion += "\tleal " + str(var.registro) + "(%ebp), %eax\n"
                    self.Traduccion += "\tpushl %eax\n" 

        if not self.ErrorFlag:
            self.cadenas += [p.CADENA_SCANF]
            self.ncadenas += 1
            self.Traduccion += "\tpushl $LC" + str(self.ncadenas) + "\n"
            self.Traduccion += "\tcall scanf\n"
            self.Traduccion += "\taddl " + str( (len(p.AuxScanf)+1) * 4 ) + ", %esp\n"

    # Auxiliar para PRINTF #p.posCorchete es una lista del tipo [-1] si var es entero o [n,m,p,...] si array
    @_('AuxPrintf "," ID posCorchete')
    def AuxPrintf(self, p):
        #AuxPrintf devuelve una lista de tuplas
        return p.AuxPrintf + [(p.ID, p.posCorchete)]

    #p.posCorchete es una lista del tipo [-1] si var es entero o [n,m,p,...] si array
    @_('ID posCorchete')
    def AuxPrintf(self, p):
        return [(p.ID, p.posCorchete)]

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
        var,flagGlobal = variable_in_ambito(self.Variables, p.ID, self.current_function, self.ErrorFlag)
        if var.tipo != "int*":
            print("Error: Variable "+p.ID+" NO ES UN PUNTERO")
            self.ErrorFlag = True

        return p.AuxScanf+[p.ID]
    
    @_('ID')
    def AuxScanf(self,p):
        var,flagGlobal = variable_in_ambito(self.Variables, p.ID, self.current_function, self.ErrorFlag)
        if var.tipo != "int*":
            print("Error: Variable "+p.ID+" NO ES UN PUNTERO")
            self.ErrorFlag = True

        return [p.ID]

    #Condicionales
    @_('IF "(" Operation ")" if_aux_1 Line ";" if_aux_2 Condicional_ELSE')
    def Condicional(self,p):
        c = self.pila_if_else.pop()
        self.Traduccion += "if_else_final" + str(c) + ":\n"

    @_('IF "(" Operation ")" if_aux_1 "{" Input "}" if_aux_2 Condicional_ELSE')
    def Condicional(self,p):
        c = self.pila_if_else.pop()
        self.Traduccion += "if_else_final" + str(c) + ":\n"

    @_('IF "(" Operation ")" if_aux_1 ";" if_aux_2 Condicional_ELSE')
    def Condicional(self,p):
        c = self.pila_if_else.pop()
        self.Traduccion += "if_else_final" + str(c) + ":\n"

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
    @_('WHILE while_aux_1 "(" Operation ")" while_aux_2 ";"')
    def Bucle(self,p):
        c = self.pila_while.pop()
        self.Traduccion += "\n"
        self.Traduccion += "\tjmp start_while" + str(c) + "\n"
        self.Traduccion += "final_while" + str(c) + ":\n"

    @_('WHILE while_aux_1 "(" Operation ")" while_aux_2 Line ";"')
    def Bucle(self,p):
        c = self.pila_while.pop()
        self.Traduccion += "\n"
        self.Traduccion += "\tjmp start_while" + str(c) + "\n"
        self.Traduccion += "final_while" + str(c) + ":\n"

    @_('WHILE while_aux_1 "(" Operation ")" while_aux_2 "{" Input "}"')
    def Bucle(self,p):
        c = self.pila_while.pop()
        self.Traduccion += "\n"
        self.Traduccion += "\tjmp start_while" + str(c) + "\n"
        self.Traduccion += "final_while" + str(c) + ":\n"

    @_("")
    def while_aux_1(self,p):
        self.while_tag += 1
        self.pila_while.append(self.while_tag)
        self.Traduccion += "\nstart_while" + str(self.while_tag) + ":\n"

    @_("")
    def while_aux_2(self,p):
        c = self.pila_while.pop()
        self.Traduccion += "\n"
        self.Traduccion += "\tpopl %eax\n"
        self.Traduccion += "\tcmpl $0, %eax\n"
        self.Traduccion += "\tjne final_while" + str(c) + "\n"
        self.pila_while.append(c)

    # Declaraciones
    @_('Declaracion2 Declaracion3')
    def Declaracion(self,p):        
        return p.Declaracion2+p.Declaracion3
    
    @_('TIPO_ID')
    def Declaracion(self,p):
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1],0)]
    
    @_('TIPO_ID CORCHETES')
    def Declaracion(self,p):
        return [(p.TIPO_ID[0]+len(p.CORCHETES)*"*", p.TIPO_ID[1], p.CORCHETES,1)]
    
    @_('TIPO_ID "=" Operation')
    def Declaracion(self,p):
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1],2)]
    
    @_('TIPO_ID ","')
    def Declaracion2(self,p):
        self.current_tipo = p.TIPO_ID[0]
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1],0)]

    @_('TIPO_ID CORCHETES ","')
    def Declaracion2(self,p):
        self.current_tipo = p.TIPO_ID[0]
        return [(p.TIPO_ID[0]+len(p.CORCHETES)*"*",p.TIPO_ID[1],p.CORCHETES,1)]

    @_('TIPO_ID "=" Operation ","')
    def Declaracion2(self,p):
        self.current_tipo = p.TIPO_ID[0]
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1],2)]

    @_('Declaracion2 Declaracion3 ","')
    def Declaracion2(self,p):
        return p.Declaracion2+p.Declaracion3
    
    @_('ID')
    def Declaracion3(self,p):
        return [(self.current_tipo,p.ID,[1],0)]

    @_('ID CORCHETES')
    def Declaracion3(self,p):
        return [(self.current_tipo+len(p.CORCHETES)*"*",p.ID,p.CORCHETES,1)]

    @_('ID "=" Operation')
    def Declaracion3(self,p):
        return [(self.current_tipo,p.ID,[1],2)]

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
        return "\n\tpopl %eax\n"

    #se contemplan entero simple y arrays N-D
    @_('Assign ID posCorchete "="')
    def Assign(self,p):
        texto = ""
        var,flagGlobal = variable_in_ambito(self.Variables, p.ID, self.current_function, self.ErrorFlag)
        if var is not None:
            if not self.ErrorFlag:
                if flagGlobal:
                    apuntar = 0
                else:
                    apuntar = var.registro
                if len(p.posCorchete) != len(var.tam):
                    print("No se ha proporcionado indices a " + p.ID + ".")
                    self.ErrorFlag = True
                elif var.tam != [1]:
                    for dim, idx in zip(var.tam, p.posCorchete):
                        if dim <= idx:
                            self.ErrorFlag = True
                            print("Acceso a " +p.ID + " fuera de rango.")
                            break
                    if not self.ErrorFlag: # si no ha saltado error, y bueno en general 
                        apuntar -= linear_index(var.tam,p.posCorchete)*4

            
            if not self.ErrorFlag:
                if flagGlobal:
                    texto = "\n"
                    texto += "\tpopl %eax\n"
                    if var.tam != [1]:
                        texto += "\tmovl %eax, $" + p.ID + str(apuntar) + "\n"
                        texto += "\tpushl $" + p.ID + str(apuntar) + "\n"
                    else:
                        texto += "\tmovl %eax, $" + p.ID + "\n"
                        texto += "\tpushl $" + p.ID + "\n"
                else:
                    texto = "\n"
                    texto += "\tpopl %eax\n"
                    texto += "\tmovl %eax, " + str(apuntar) + "(%ebp)\n"
                    texto += "\tpushl " + str(apuntar) + "(%ebp)\n"
                texto += p.Assign
        else:
            print(str(p.ID))
        return texto

    # Operaciones Aritmetico-Logicas
    @_('andOp')
    def Operation(self,p):
        pass

    @_('andOp OR Operation')
    def Operation(self,p):
        self.cond_tag += 1
        self.Traduccion = disyuncion(self.Traduccion,self.cond_tag)

    @_('equalOp')
    def andOp(self,p):
        pass

    @_('equalOp AND andOp')
    def andOp(self,p):
        self.cond_tag += 1
        self.Traduccion = conjuncion(self.Traduccion,self.cond_tag)
    
    @_('compOp')
    def equalOp(self,p):
        pass

    @_('compOp equalSymbol equalOp')
    def equalOp(self,p):
        if p.equalSymbol == "==":
            self.cond_tag += 1
            self.Traduccion = igual(self.Traduccion,self.cond_tag)
            self.cond_tag += 1
        if p.equalSymbol == "!=":
            self.Traduccion = distinto(self.Traduccion,self.cond_tag)

    @_('addOp')
    def compOp(self,p):
        pass

    @_('addOp compSymbol compOp')
    def compOp(self,p):
        if p.compSymbol == ">=":
            self.cond_tag += 1
            self.Traduccion = mayor_o_igual(self.Traduccion,self.cond_tag)
        if p.compSymbol == "<=":
            self.cond_tag += 1
            self.Traduccion = menor_o_igual(self.Traduccion,self.cond_tag)

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
        self.Traduccion = suma(self.Traduccion)

    @_('prodOp "-" addOp')
    def addOp(self,p):
        self.Traduccion = resta(self.Traduccion)

    @_('prodOp')
    def addOp(self,p):
        pass

    @_('fact "*" prodOp')
    def prodOp(self,p):
        self.Traduccion = multiplicacion(self.Traduccion)

    @_('fact "/" prodOp')
    def prodOp(self,p):
        self.Traduccion = division(self.Traduccion)

    @_('fact')
    def prodOp(self,p):
        pass

    @_('"-" fact')
    def fact(self,p):
        self.Traduccion = resta_unaria(self.Traduccion)

    @_('"!" fact')
    def fact(self,p):
        self.cond_tag += 1
        self.Traduccion = negacion(self.Traduccion,self.cond_tag)

    @_('"(" Operation ")"')
    def fact(self,p):
        pass

    @_('')
    def variables(self,p):
        return []

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
        var,flagGlobal = variable_in_ambito(self.Variables, p.ID, self.current_function, self.ErrorFlag)

        if not self.ErrorFlag:
            pos = var.registro
            if flagGlobal:
                self.Traduccion += "\n"
                self.Traduccion += "\tpushl $" + p.ID + "\n"
            else:
                self.Traduccion += "\n"
                self.Traduccion += "\tpushl " + str(pos) + "(%ebp)\n"
    
    @_('ID CORCHETES')
    def fact(self,p):
        var,flagGlobal = variable_in_ambito(self.Variables, p.ID, self.current_function, self.ErrorFlag)

        if len(p.CORCHETES) != len(var.tam):
            print("Error: Variable "+p.ID+" tamaño incorrecto")
            self.ErrorFlag = True
        else:
            for tam, t in zip(var.tam, p.CORCHETES):  
                if t >= tam:  # Compara el índice con el tamaño máximo
                    print(f"Error: Posición inalcanzable de {p.ID}")
                    self.ErrorFlag = True
                    break  
              
        if not self.ErrorFlag:
            pos = linear_index(var.tam,p.CORCHETES)
            if flagGlobal:
                self.Traduccion += "\n"
                self.Traduccion += "\tpushl $" + p.ID + " + " + str(pos)*4 + "\n"
            else:
                pos = var.registro - pos*4
                self.Traduccion += "\n"
                self.Traduccion += "\tpushl " + str(pos) + "(%ebp)\n"

    @_('NUM')
    def fact(self,p):
        n = str(p.NUM)
        self.Traduccion += "\n"
        self.Traduccion +=  "\tpushl $" + n + "\n"
    
    @_('fcall')
    def fact(self,p):
        pass
    
    @_('ID "(" entradaID ")"')
    def fcall(self,p):
        params = self.Funciones.get(p.ID)
        if params != None:
            if len(params[0]) == len(p.entradaID):
                for i in range(len(p.entradaID)):
                    (AMP,var,corchetes) = p.entradaID[i]
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
        for a,id,corchetes in p.entradaID:
            cont += 1
            aux = self.Variables.get((id, self.current_function))
            self.Traduccion += "\tpushl " + str(aux.registro - 4*linear_index(aux.tam,corchetes)) +"(%ebp)\n"
        self.Traduccion += "\tcall " + p.ID + "\n"
        self.Traduccion += "\taddl $" + str(cont*4) + " ,%esp\n"
        if params[1] != "void":
            self.Traduccion += "\tpushl %eax\n"

    @_('')
    def entradaID(self,p):
        return []
    
    @_('listaID')
    def entradaID(self,p):
        return p.listaID

    @_('AMPERSAN ID posCorchete')
    def listaID(self,p):
        return [(p.AMPERSAN,p.ID,p.posCorchete)]

    @_('listaID "," AMPERSAN ID posCorchete')
    def listaID(self,p):
        return p.listaID+[(p.AMPERSAN,p.ID,p.posCorchete)]
    
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
        
        self.sectiondata = "\tsection .data\n" + self.sectiondata + "\n"
        self.Traduccion = self.tradGlobal + self.sectiondata + self.Traduccion

class varAux():
        def __init__(self,t,tam,n):
            self.tipo = t
            self.tam = tam
            self.registro = n

        def __str__(self):
            print(self.tipo+" "+self.tam+" "+self.registro)

def disyuncion(trad,cond_tag):
    trad += "\n"
    trad += "\tpopl %eax\n"
    trad += "\tcmpl &0,%eax\n"
    trad += "\tjne cond_true" + str(cond_tag) + "\n"
    trad += "\tpopl %eax\n"
    trad += "\tcmpl &0,%eax\n"
    trad += "\tje cond_true" + str(cond_tag) + "\n"
    trad += "\tpushl &0\n"
    trad += "\tjmp cond_final" + str(cond_tag) + "\n"
    trad += "cond_true" + str(cond_tag) + ":\n"
    trad += "\tpushl &1\n"
    trad += "cond_final" + str(cond_tag) + ":\n"
    #cond_tag += 1
    return trad

def conjuncion(trad,cond_tag):
    trad += "\n"
    trad += "\tpopl %eax\n"
    trad += "\tcmpl &0,%eax\n"
    trad += "\tje cond_false" + str(cond_tag) + "\n"
    trad += "\tpopl %eax\n"
    trad += "\tcmpl &0,%eax\n"
    trad += "\tje cond_false" + str(cond_tag) + "\n"
    trad += "\tpushl &1\n"
    trad += "\tjmp cond_final" + str(cond_tag) + "\n"
    trad += "cond_false" + str(cond_tag) + ":\n"
    trad += "\tpushl &0\n"
    trad += "cond_final" + str(cond_tag) + ":\n"
    #cond_tag += 1
    return trad

def igual(trad,cond_tag):
    trad += "\n"
    trad += "\tpopl %ebx\n"
    trad += "\tpopl %eax\n"
    trad += "\tcmpl &ebx,%eax\n"
    trad += "\tjne cond_false" + str(cond_tag) + "\n"
    trad += "\tpushl &1\n"
    trad += "\tjmp cond_final" + str(cond_tag) + "\n"
    trad += "cond_false" + str(cond_tag) + ":\n"
    trad += "\tpushl &0\n"
    trad += "cond_final" + str(cond_tag) + ":\n"
    #cond_tag += 1
    return trad

def distinto(trad,cond_tag):
    trad += "\n"
    trad += "\tpopl %ebx\n"
    trad += "\tpopl %eax\n"
    trad += "\tcmpl &ebx,%eax\n"
    trad += "\tje cond_false" + str(cond_tag) + "\n"
    trad += "\tpushl &1\n"
    trad += "\tjmp cond_final" + str(cond_tag) + "\n"
    trad += "cond_false" + str(cond_tag) + ":\n"
    trad += "\tpushl &0\n"
    trad += "cond_final" + str(cond_tag) + ":\n"
    #cond_tag += 1
    return trad

def mayor_o_igual(trad,cond_tag):
    trad += "\n"
    trad += "\tpopl %ebx\n"
    trad += "\tpopl %eax\n"
    trad += "\tcmpl &ebx,%eax\n"
    trad += "\tjl cond_false" + str(cond_tag) + "\n"
    trad += "\tpushl &1\n"
    trad += "\tjmp cond_final" + str(cond_tag) + "\n"
    trad += "cond_false" + str(cond_tag) + ":\n"
    trad += "\tpushl &0\n"
    trad += "cond_final" + str(cond_tag) + ":\n"
    #cond_tag += 1
    return trad

def menor_o_igual(trad,cond_tag):
    trad += "\n"
    trad += "\tpopl %ebx\n"
    trad += "\tpopl %eax\n"
    trad += "\tcmpl &ebx,%eax\n"
    trad += "\tjg cond_false" + str(cond_tag) + "\n"
    trad += "\tpushl &1\n"
    trad += "\tjmp cond_final" + str(cond_tag) + "\n"
    trad += "cond_false" + str(cond_tag) + ":\n"
    trad += "\tpushl &0\n"
    trad += "cond_final" + str(cond_tag) + ":\n"
    #cond_tag += 1
    return trad

def suma(trad):
    text = "\n"
    text += "\tpopl %ebx\n"
    text += "\tpopl %eax\n"
    text += "\taddl %ebx, %eax\n"
    text += "\tpushl %eax\n"
    trad += text
    return trad

def resta(trad):
    text = "\n"
    text += "\tpopl %ebx\n"
    text += "\tpopl %eax\n"
    text += "\tsubl %ebx, %eax\n"
    text += "\tpushl %eax\n"
    trad += text
    return trad

def multiplicacion(trad):
    text = "\n"
    text += "\tpopl %ebx\n"
    text += "\tpopl %eax\n"
    text += "\timull %ebx, %eax\n"
    text += "\tpushl %eax\n"
    trad += text
    return trad

def division(trad):
    text = "\n"
    text += "\tpopl %ebx\n"
    text += "\tpopl %eax\n"
    text += "\tcdq\n"
    text += "\tdivl %ebx\n"
    text += "\tpushl %eax\n"
    trad += text
    return trad

def resta_unaria(trad):
    text = "\n"
    text += "\tpopl %ebx\n"
    text += "\tmovl &0,%eax\n"
    text += "\tsubl %ebx, %eax\n"
    text += "\tpushl %eax\n"
    trad += text
    return trad

def negacion(trad,counter):
    text = "\tpopl %eax\n"
    text += "\tcmpl $0, %eax\n"
    text += "\tjne cond_final" + str(counter) + " \n"
    text += "\tmovl $0, %eax\n"
    text += "cond_final" + str(counter) + ": \n"
    text += "\tpushl %eax\n\n"
    trad += text
    return trad

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

def variable_in_ambito(variables, id, ambito, error):
    """ variable_in_ambito devuelve la variable si existe y si su ambito es global o no"""
    #print("varx:"+str(id) + str(ambito))
    var = variables.get((id,ambito))
    flagGlobal = False
    if var is None:
        var = variables.get((id,"Global"))
        flagGlobal = True
    if var is None:
        print("Error: Variable "+id+" no declarada")
        error = True
    #else:
        #print(var.tipo)
        #print(var.tam)
        #print(var.registro)
    return var, flagGlobal

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
        with open(os.path.join(sys.path[0], "traduccion"+fichero+".txt"), "w") as file:
            file.write(parser.Traduccion)
        print("VARIABLES")
        for key,value in parser.Variables.items():
            print("Variable: "+key[0]+" Ambito: "+key[1]+" Tipo: "+value.tipo+" Tamaño: "+str(value.tam) +" EBP: "+str(value.registro) )
        print("\nFUNCIONES")
        for key,value in parser.Funciones.items():
            print("Funcion: "+key+" "+str(value))
