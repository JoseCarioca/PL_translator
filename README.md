Instrucciones de uso:
- Al correr el archivo .py se pedirá al usuario el nombre de un fichero de prueba con formato "ejemplo.c", donde éste deberá encontrarse 
al mismo nivel de ruta que el programa. Si no se proporciona ningun fichero, P2.py buscará el fichero "pruebas.c" (opcion por defecto)
-Se pueden probar otros dos ficheros de ejemplo llamados "prueba_vacia.c" y "prueba_error.c" o ¡escriba el suyo propio!


Los tokens:
- tokens = {ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR }
- literals = { '=', '!', '+', '-', '*', '/', ';', '(', ')', '{', '}' }

La gramática:
-   funcion -> funcion TIPO ID '(' variables')' '{' Input '}'
-   Input -> empty | Input Line ';' 
-   Line  -> Declaracion | Assign Operation
-   
-   Declaracion -> Declaracion2 Declaracion3
-   Declaracion2 -> TIPO | Declaracion2 Declaracion3 ','
-   Declaracion3 -> ID | ID '=' Operation
-   TIPO -> INT
-
-   Assign -> empty | Assign ID '='
-
-   Operation -> andOp | andOp '||' Operation
-   andOp -> equalOp | equalOp '&&' andOp
-   equalOp -> compOp | compOp equalSymbol equalOp
-   compOp -> addOp | addOp compSymbol compOp
-
-   equalSymbol -> '==' | '!='
-   compSymbol -> '>=' | '<='
-
-   addOp -> prodOp '+' addOp
-   addOp -> prodOp '-' addOp
-   addOp -> prodOp
-
-   prodOp -> fact '*' prodOp
-   prodOp -> fact '/' prodOp
-
-   fact -> ID | NUM | '!' fact | '-'fact | '(' Operation ')'
-   listavars -> var | var Tipo ID
-   variables -> empty | listavars
-   listavars -> listavars ',' TIPO ID | TIPO ID
