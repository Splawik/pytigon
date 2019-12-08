#include <pytigon.h>
#include <string.h>
#include <stdlib.h>

DLL_EXPORT long long silnia(long long l)
{   long long s, i;
    i=l-1; s=l;
    while(i>1)
    { s=s*i;
      i--;
    }
    return s;
}

DLL_EXPORT char * passed(char * arg)
{   char *buf = (char *)malloc(1024);
    strcpy(buf, arg);
    strcat(buf, ": PASSED!");
    return buf;
}

DLL_EXPORT int free_memory(void *ptr)
{ free(ptr);
  return 1;
}

DLL_EXPORT void message(char * msg)
{
#ifdef WIN32 or WIN64
    MessageBox(NULL, msg, "Caption", MB_OK);
#else
    printf(msg); printf("\n");
#endif
}
