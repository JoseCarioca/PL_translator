
void fun (int *c) 
{
    printf("Variable: %d ", c);
}

void empty() {}

void main ()
{
    int Narray[2][3];
    Narray[1][2];

    int a = 4;
    fun(&a);
}

