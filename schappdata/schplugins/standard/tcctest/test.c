#include <stdio.h>
#include <time.h>

int main(void)
{  long long i, sum;
    clock_t t;
    t = clock();
    sum=0;
    for(i=0;i<10000000;i++)
    { sum += i;
    }
    t = clock() - t;
    printf ("It took me %d clicks (%f seconds).\n",t,((float)t)/CLOCKS_PER_SEC);
    printf("%lld", sum);
}
