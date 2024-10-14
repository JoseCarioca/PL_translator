Instrucciones de uso:
- Para que el script de Python funcione el fichero de "pruebas.c" debe estar en la misma carpeta que "P1.py". Para usar el programa, ejecutar desde terminal el script de Python que mostrara "Cadena Aceptada" en caso de que el texto en "prueba.c" sea correcto.

Los tokens:
    tokens = {ID,NUM,EQUAL,LE_EQ, GR_EQ, NOT_EQ, AND, OR }
    literals = {'=','!','+','-','*','/',';','(',')'}

La gramática:
    Input -> empty | Input Line ';' 
    Line  -> Assign Operation
    Assign -> empty | Assign ID '='
    Operation -> andOp | andOp '||' Operation
    andOp -> equalOp | equalOp '&&' andOp
    equalOp -> compOp | compOp equalSymbol equalOp
    compOp -> addOp | addOp compSymbol compOp
    equalSymbol -> '==' | '!='
    compSymbol -> '>=' | '<='
    addOp -> prodOp '+' addOp
    addOp -> prodOp '-' addOp
    addOp -> prodOp
    prodOp -> unary '*' prodOp
    prodOp -> unary '/' prodOp
    fact -> ID | NUM | '!' fact | '-'fact | '(' Operation ')'
