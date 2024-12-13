A continuación se presenta una explicación de la gramática de este C reducido, con puntos de lo que acepta o deja de aceptar.
** Gramática **

Se permite:
-Declaración y asignación de varibales de tipo enteros y arreglos de cualquier dimensión (no hay un límite establecido).
- Realizar operaciones aritmeticológicas básicas como: {+,-,*,/}, { == , !=, <=, >=}, negación y resta unaria.
- Declaración y uso de funciones (tipo void y entero). 
- No hay limitaciones en las declaraciones de globales / funciones, el orden puede ser cualquiera.
- Recursividad.
- Existe paso por valor y por referencia; a las funciones se les permite pedir paso por punteros.
- Declaraciones globales.
- Bloques de sentencia if-else y sus variantes.
- Bloques de sentencia while.
- Uso de funciones 'printf' y 'scanf'.

Limitaciones:
- No se permite declaracion de punteros (sí se permite el paso por referencia).
- No se contempla la declaración adelantada de funciones. Para el uso de las mismas deben declararse antes de su llamada (parte superior del código).
- La función scanf no permite cualquier cadena, sino que se asigna un tipo de cadena especial (CADENA_SCANF) que sigue la regla: (%(u|d|i|f|s))+

________________________________________________

** Traducción **

A partir de la gramática permitida, se escribe la traducción, la cual se encuentra en el siguiente punto:

Bondades:
- La declaración de variables de cualquier tipo permitido se realiza con éxito en los ambitos de las funciones.
- Todas las operaciones se realizan correctamente, concatenaciones incluidas.
-...


Limitaciones de la versión actual (sujeto a cambio):
- No se realiza la traduccion de declaraciones globales.
- Las cadenas constantes de scanf y printf no se guardan.
- Los bloques anidados no se traducen correctamente.
-...

