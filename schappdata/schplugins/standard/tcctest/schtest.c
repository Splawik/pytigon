long long silnia(long long l)
{   long long s, i;
    i=l-1; s=l;
    while(i>1)
    { s=s*i;
      i--;
    }
    return s;
}
