#   tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA, SCANF, CADENA_SCANF } 
#   literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')', '&'}
#   
#   Global -> empty | Global Declaracion ';' | Global Funcion
#
#   Funcion -> TIPO_ID '(' variables ')' '{' Input RETURN Operation ';' '}'
#   Funcion -> VOID ID '(' variables ')' '{' Input '}'
#
#   variables -> empty | listavars
#   listavars -> listavars ',' TIPO ASTERISCO ID | TIPO ASTERISCO ID 
#   ASTERISCO -> empty | ASTERISCO '*'
#
#   Input -> empty | Input Line ';' 
#   Line  -> Declaracion | Assign Operation | PRINTF '(' CADENA ',' AuxPrintf ')'
#  | SCANF '(' CADENA_SCANF ','  AuxScanf ')'
#   AuxPrintf -> empty | AuxPrintf ',' ID
#   AuxScanf -> '&' ID | AuxScanf '&' ID
#
#   Declaracion -> TIPO_ID | TIPO_ID CORCHETES | TIPO_ID '=' Operation | Declaracion2 Declaracion3
#   Declaracion2 -> TIPO_ID ',' | TIPO_ID CORCHETES ',' | TIPO_ID '=' Operation ',' | Declaracion2 Declaracion3 ','
#   Declaracion3 -> ID | ID CORCHETES | ID '=' Operation
#   TIPO_ID -> TIPO ID
#   TIPO -> INT
#   CORCHETES -> '[' NUM ']' | Corchetes '[' NUM ']'
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
#   fact -> ID | ID CORCHETES | NUM | fcall | '!' fact | '-'fact | '(' Operation ')'
#   fcall -> ID '(' lista_IDs ')'
#   entradaID -> empty | listaID
#   listaID -> AMPERSAN ID | listaID',' AMPERSAN ID
#   AMPERSAN -> empty | AMPERSAN '&'


from sly import Lexer,Parser
import os, sys, re

class P1Lexer(Lexer):

    tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA, SCANF, CADENA_SCANF} 

    literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' ,'{', '}', '&', '[', ']'}
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
            if (var[1],"Global") in self.Variables:
                print("No puedes declarar variables con el mismo nombre en el mismo ámbito.")
                self.ErrorFlag = True
            else:
                self.Variables[(var[1],"Global")] = varAux(var[0],var[2])

    @_('Global Funcion')
    def Global(self,p):
        pass

    @_('TIPO_ID setCurrentFunction "(" variables ")" "{" Input RETURN Operation ";" "}"')
    def Funcion(self,p):
        if p.TIPO_ID[1] =="main":
            self.has_main = True            
        if p.TIPO_ID[1] in self.Funciones.keys():
            print("No puedes declarar funciones con el mismo nombre.")
            self.ErrorFlag = True
        else:
            self.Funciones[p.TIPO_ID[1]] = (p.variables,p.TIPO_ID[0])

    @_('VOID ID setCurrentFunction "(" variables ")" "{" Input "}"')
    def Funcion(self,p):
        if p.ID =="main":
            self.has_main = True 
        if p.ID in self.Funciones.keys():
            print("No puedes declarar funciones con el mismo nombre.")
            self.ErrorFlag = True
        else:
            self.Funciones[p.ID] = (p.variables,"void")

    @_("")
    def setCurrentFunction(self,p):
        if isinstance(p[-1], tuple):
            self.current_function = p[-1][1]
        elif isinstance(p[-1], str):
            self.current_function = p[-1]

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
        if p.Declaracion != None:
            for var in p.Declaracion:
                if (var[1],self.current_function) in self.Variables.keys():
                    print("Variable '" + var[1] + "' ya declarada en '" + self.current_function + "' previamente")
                    self.ErrorFlag = True
                else:
                    self.Variables[(var[1],self.current_function)] = varAux(var[0],var[2])
        return p.Declaracion
    
    @_('PRINTF "(" CADENA ")"')
    def Line(self,p):
        if re.findall(r'\%[a-z]',p.CADENA):
            print("Error: Faltan las variables a imprimir en el printf")
            self.ErrorFlag = True

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

    @_('AuxPrintf "," ID')
    def AuxPrintf(self,p):
        return p.AuxPrintf+[p.ID]

    @_('ID')
    def AuxPrintf(self,p):
        return [p.ID]

    @_('SCANF "(" CADENA_SCANF "," AuxScanf ")"')
    def Line(self,p):
        entrada = re.findall(r'%(u|d|i)',p.CADENA_SCANF)
        if len(entrada) == len(p.AuxScanf):
            for var in p.AuxScanf:
                if all( (var, self.current_function) != (id,ambito) for (id,ambito) in self.Variables.keys()) and all((var,"Global") != (id,ambito) for (id,ambito) in self.Variables.keys()):
                    print("Error: Variables en el scanf no existen en su ambito")
                    self.ErrorFlag = True
                else:
                    print("Bien. Variables scanf coinciden")
        else:
            print("Error: No se usan el mismo numero de variables que se le pasa al scanf")
            self.ErrorFlag = True

    @_('AuxScanf "," "&" ID')
    def AuxScanf(self,p):
        return p.AuxScanf+[p.ID]

    @_('"&" ID')
    def AuxScanf(self,p):
        return [p.ID]
    
    # Para punteros
    @_('AuxScanf "," ID')
    def AuxScanf(self,p):
        var = self.Variables.get((p.ID,self.current_function)) or self.Variables.get((p.ID,"Global"))
        if var == None:
            print("Error: Variable "+p.ID+" no está declarada")
            self.ErrorFlag = True
        elif var.tipo != "int*":
            print("Error: Variable "+p.ID+" NO ES UN PUNTERO")
            self.ErrorFlag = True
        else:
            print("Bien. variable "+p.ID+" es puntero")

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
        else:
            pass #print("Bien. variable "+p.ID+" es puntero")

        return [p.ID]

    # Declaraciones
    @_('Declaracion2 Declaracion3')
    def Declaracion(self,p):
        return p.Declaracion2+p.Declaracion3
    
    @_('TIPO_ID')
    def Declaracion(self,p):
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1])]

    @_('TIPO_ID CORCHETES')
    def Declaracion(self,p):
        return [(p.TIPO_ID[0]+len(p.CORCHETES)*"*",p.TIPO_ID[1],p.CORCHETES)]
    
    @_('TIPO_ID "=" Operation')
    def Declaracion(self,p):
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1])]
    
    @_('TIPO_ID ","')
    def Declaracion2(self,p):
        self.current_tipo = p.TIPO_ID[0]
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1])]

    @_('TIPO_ID CORCHETES ","')
    def Declaracion2(self,p):
        self.current_tipo = p.TIPO_ID[0]
        return [(p.TIPO_ID[0]+len(p.CORCHETES)*"*",p.TIPO_ID[1],p.CORCHETES)]

    @_('TIPO_ID "=" Operation ","')
    def Declaracion2(self,p):
        return [(p.TIPO_ID[0],p.TIPO_ID[1],[1])]

    @_('Declaracion2 Declaracion3 ","')
    def Declaracion2(self,p):
        return p.Declaracion2+p.Declaracion3
    
    @_('ID')
    def Declaracion3(self,p):
        return [(self.current_tipo,p.ID,[1])]

    @_('ID CORCHETES')
    def Declaracion3(self,p):
        return [(self.current_tipo+len(p.CORCHETES)*"*",p.ID,p.CORCHETES)]

    @_('ID "=" Operation')
    def Declaracion3(self,p):
        return [(self.current_tipo,p.ID,[1])]

    @_('TIPO ID')
    def TIPO_ID(self,p):
        return (p.TIPO,p.ID)

    @_('INT')
    def TIPO(self,p):
        return "int"
    
    # @_('INT "*"')
    # def TIPO(self,p):
    #     return "int*"
    
    @_('"[" NUM "]"')
    def CORCHETES(self,p):
        return [p.NUM]
    
    @_('CORCHETES "[" NUM "]"')
    def CORCHETES(self,p):
        return p.CORCHETES + [p.NUM]
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
                self.Variables[(var[1],self.current_function)] = varAux(var[0],var[2])
        return p.listavars

    @_('TIPO ASTERISCO ID')
    def listavars(self,p):
        cadena = p.TIPO
        if p.ASTERISCO != None:
            cadena = cadena + p.ASTERISCO
        return [(cadena,p.ID,[1])]

    @_('listavars "," TIPO ASTERISCO ID')
    def listavars(self,p):
        cadena = p.TIPO
        if p.ASTERISCO != None:
            cadena = cadena + p.ASTERISCO
        return p.listavars+[(cadena,p.ID,[1])] #concatenado
    
    @_('')
    def ASTERISCO(self,p):
        pass

    @_('ASTERISCO "*"')
    def ASTERISCO(self,p):
        if p.ASTERISCO == None:
            return "*"
        else: 
            return str(p.ASTERISCO+"*")

    @_('ID')
    def fact(self,p):
        return str(p.ID)
    
    @_('ID CORCHETES')
    def fact(self,p):
        var = self.Variables.get((p.ID,self.current_function)) or self.Variables.get((p.ID,"Global"))
        if var == None:
            print("Error: Variable "+p.ID+" no declarada")
            self.ErrorFlag = True
        elif len(p.CORCHETES) != len(var.tam):
            print("Error: Variable "+p.ID+" tamaño incorrecto")
            self.ErrorFlag = True
        else:
            if p.CORCHETES != None:
                for t in p.CORCHETES:
                    for tam in var.tam:
                        if tam <= t:
                            print("Error: Posicion inalcanzable de "+p.ID)
                            self.ErrorFlag = True
        return str(p.ID)

    @_('NUM')
    def fact(self,p):
        return str(p.NUM)
    
    @_('fcall')
    def fact(self,p):
        pass
    
    @_('ID "(" entradaID ")"')
    def fcall(self,p):
        #print("funciones existentes:" + str(self.Funciones))
        if p.entradaID is not None:
            for (AMP,var) in p.entradaID:
                if all( (var, self.current_function) != (id,ambito) for (id,ambito) in self.Variables.keys()) and all((var,"Global") != (id,ambito) for (id,ambito) in self.Variables.keys()):
                    print("Error: Variables en llamada de " + p.ID + " no existen en su ambito")
                    self.ErrorFlag = True

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
        def __init__(self,t,tam):
            self.tipo = t
            self.tam = tam

def disyuncion(id1,id2,trad):
    text = id1 + "||" + id2
    trad += text + "\n"
    return (text,trad)

def conjuncion(id1,id2,trad):
    text = id1 + "&&" + id2
    trad += text + "\n"
    return (text,trad)

def igual(id1,id2,trad):
    text = id1 + "==" + id2
    trad += text + "\n"
    return (text,trad)

def distinto(id1,id2,trad):
    text = id1 + "!=" + id2
    trad += text + "\n"
    return (text,trad)

def mayor_o_igual(id1,id2,trad):
    text = id1 + ">=" + id2
    trad += text + "\n"
    return (text,trad)

def menor_o_igual(id1,id2,trad):
    text = id1 + "<=" + id2
    trad += text + "\n"
    return (text,trad)

def suma(id1,id2,trad):
    text = id1 + "+" + id2
    trad += text + "\n"
    return (text,trad)

def resta(id1,id2,trad):
    text = id1 + "-" + id2
    trad += text + "\n"
    return (text,trad)

def multiplicacion(id1,id2,trad):
    text = id1 + "*" + id2
    trad += text + "\n"
    return (text,trad)

def division(id1,id2,trad):
    text = id1 + "/" + id2
    trad += text + "\n"
    return (text,trad)

def resta_unaria(id,trad):
    text = "-" + id
    trad += text + "\n"
    return (text,trad)

def negacion(id,trad):
    text = "!" + id
    trad += text + "\n"
    return (text,trad)

def parentesis(id, trad):
    text = "(" + id +")"
    trad += text + "\n"
    return (text,trad)

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
            print("Variable: "+key[0]+" Ambito: "+key[1]+" Tipo: "+value.tipo+" Tamaño: "+str(value.tam))
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
