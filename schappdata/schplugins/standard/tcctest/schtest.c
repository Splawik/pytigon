#include <pytigon.h>

DLL_EXPORT long long silnia(long long l)
{   long long s, i;
    i=l-1; s=l;
    while(i>1)
    { s=s*i;
      i--;
    }
    //MessageBox(NULL, "Hello!", "Caption", MB_OK);
    return s;
}
