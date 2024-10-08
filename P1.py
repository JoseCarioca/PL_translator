#   tokens = {CONST,ID,INT}
#   literals = {'=','==','<=','>=','!=','&&','||','!','+','-','*','/',';'}
#   
#   Input -> empty | Input Line ';' 
#   Line  -> Assign Operation
#   Operation -> '(' Operation ')' | addOp | equalOp
#
#   Assign -> empty | Assign ID '='
#
#   equalOp -> compOp | compOp equalSymbol Operation
#   compOp -> unary | unary compSymbol Operation
#
#   compSymbol -> '>=' | '<='
#   equalSymbol -> '==' | '!='
#
#   addOp -> '(' addOp ')'
#   addOp -> prodOp '+' Operation
#   addOp -> prodOp '-' Operation
#   addOp -> prodOp
#
#   prodOp -> unary '*' Operation
#   prodOp -> unary '/' Operation
#   prodOp -> unary
#   
#   unary -> fact | '!' Operation | '-' Operation
#
#   fact -> ID | NUM


from sly import Lexer,Parser
