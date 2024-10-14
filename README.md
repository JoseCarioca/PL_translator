Instrucciones de uso:
- Para que el script de Python funcione el fichero de "pruebas.c" debe estar en la misma carpeta que "P1.py". Para usar el programa, ejecutar desde terminal el script de Python que mostrara "Cadena Aceptada" en caso de que el texto en "prueba.c" sea correcto.
-Se pueden probar otros dos ficheros de ejemplo llamados "prueba_vacia.c" y "prueba_error.c" cambiando el nombre en el propio main de P1.py 
donde se muestra cómo se acepta la cadena vacía y cómo se lanza un error de Cadena no Aceptada respectivamente.

Los tokens:
- tokens = {ID,NUM,EQUAL,LE_EQ, GR_EQ, NOT_EQ, AND, OR }
- literals = {'=','!','+','-','*','/',';','(',')'}

La gramática:
- Input -> empty | Input Line ';' 
- Line  -> Assign Operation

- Assign -> empty | Assign ID '='
- Operation -> andOp | andOp '||' Operation

- andOp -> equalOp | equalOp '&&' andOp
- equalOp -> compOp | compOp equalSymbol equalOp
- compOp -> addOp | addOp compSymbol compOp

- equalSymbol -> '==' | '!='
- compSymbol -> '>=' | '<='

- addOp -> prodOp '+' addOp
- addOp -> prodOp '-' addOp
- addOp -> prodOp

- prodOp -> fact '*' prodOp
- prodOp -> fact '/' prodOp

- fact -> ID | NUM | '!' fact | '-'fact | '(' Operation ')'
