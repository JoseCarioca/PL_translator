
void main ()
{
    int i,j;
    i = j = 0;
    while(i <= 10) i = i + 1;
    if( j <= 10){
      if (j + i >= 0){
        int k = 0;
        while(k <= 5){
            printf("%d\n",k);
            k = k*2;
        }
      }
    }
    printf("var %d still exists.\n",k);
}


