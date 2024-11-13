Instrucciones de uso:
- Al correr el archivo .py se pedirá al usuario el nombre de un fichero de prueba con formato "ejemplo.c", donde éste deberá encontrarse 
al mismo nivel de ruta que el programa. Si no se proporciona ningun fichero, P2.py buscará el fichero "pruebas.c" (opcion por defecto)
-Se pueden probar otros dos ficheros de ejemplo llamados "prueba_vacia.c" y "prueba_error.c" o ¡escriba el suyo propio!

Cambios respecto a la P2:
- Se añadieron funciones globales
- Se modifico la regla de funciones
- Se añadio una regla TIPO_ID -> TIPO ID
- Se modificaron las declaraciones
- La estructura donde se almacenan las variables ha sido modificada y ahora es un diccionario donde el key es (ID,Ambito) y su valor None
- Se han añadido mensajes de error referente a las redeclaraciones y la necesidad del main

Decisiones de la P3:
- las funciones se separan en dos tipos (que devuelvan o no un valor) y esto se refleja en las reglas 
- La estructura para almacenar las funciones es un diccionario donde el key es la ID y los valores son TIPO a devolver y parametros de entrada
- Se pueden declarar variables globales tanto al principio como al final como entre funciones
- El main siempre esta y puede encontrarse en cualquier parte del fichero, ya que se comprueba despues del parsing (sobrecargando la operacion)

Decisiones de la P4:
- Para guardar el ambito se usa el caracter terminador 'setCurrentFunction' que podrá usarse en el cuerpo de dicha función
- Las funciones scanf y printf aceptan cualquier indicador de formato referente a enteros: u | d | i. Además de otros formatos como "%f" y "%s".
- No se aceptan formatos de printf con distinto número de indicadores y de variables o con diferente tipo (conversion en momento de escritura)

Cambios respecto a la P3:
- Se añade la regla SCANF y nodos para la creación del AST
- Se añade un nodo por cada regla aritmética-lógica con la que luego se escribe un fichero txt con cada operación.
- Para evitar el uso de atributos heredados, las variables se guardan en la regla "Line -> Declaracion".

Decisiones de la P5:
- A la hora de declarar variables, no hay límites en el tamaño o dimensiones de los array a nivel de sintaxis.
- No es posible la declaración de punteros pero sí el paso por referencia de variables ( funcion(&entero) )
- Se restinge la falta de '&' en la llamada de scanf a tipos de dato simple (puntero a entero int*)

Cambios respecto a la P4:
- La gramática acepta arrays de 1 o varias dimensiones (no hay límite) y el paso por referencia de variables
- Se ha modificado la funcion scanf para que acepte variables tipo puntero y varios parámetros en una misma llamada
- Se añaden las reglas 'ASTERISCO' y 'AMPERSAN' para la declaración y llamada de variables respectivamente

Decisiones de la P6:
- Se permite llamar a funciones con argumentos de diferente tamaño y saltará un aviso al respecto.

Cambios respecto a la P5:
- Se añade la posibilidad de crear funciones con arreglos constantes como parametro



Los tokens:
-   tokens = { ID, NUM, EQUAL, LE_EQ, GR_EQ, NOT_EQ, AND, OR, INT, VOID, RETURN, PRINTF, CADENA_SCANF, CADENA, SCANF } 
- literals = { '=', '!', '+', '-', '*', '/', ',', ';', '(', ')' ,'{', '}','&'}

La gramática:
-   Global -> empty | Global Declaracion ';' | Global Funcion
-   Funcion -> TIPO_ID '(' variables ')' '{' Input RETURN Operation ';' '}'
-   Funcion -> VOID ID '(' variables ')' '{' Input '}'

-   variables -> empty | listavars
-   listavars -> listavars ',' TIPO ID | TIPO ID

-   Input -> empty | Input Line ';' 
-   Line  -> Declaracion | Assign Operation | PRINTF '(' CADENA ',' AuxPrintf ')' | SCANF '(' CADENA_SCANF ')'
-   AuxPrintf -> empty | AuxPrintf ',' ID
-   Assign -> empty | Assign ID '='
-   
-   Declaracion -> TIPO_ID | TIPO_ID '=' Operation | Declaracion2 Declaracion3
-   Declaracion2 -> TIPO_ID ',' | TIPO_ID '=' Operation ',' | Declaracion2 Declaracion3 ','
-   Declaracion3 -> ID | ID '=' Operation
-   TIPO_ID -> TIPO ID
-   TIPO -> INT

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
-   fact -> ID | NUM | fcall | '!' fact | '-'fact | '(' Operation ')'
-   fcall -> ID '(' listavars ')'


