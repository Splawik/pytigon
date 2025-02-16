#include <windows.h>
#include <winapi/winreg.h>
#include <stdio.h>
#include <string.h>

int key(char *bufor)
{  HKEY hKey;
    int ret = 0;
    LONG returnStatus;
    DWORD dwType=REG_SZ;
    DWORD dwSize=255;
    returnStatus = RegOpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\pytigon", 0,  KEY_ALL_ACCESS, &hKey);
    if (returnStatus == ERROR_SUCCESS)
    {  returnStatus = RegQueryValueEx(hKey, NULL, NULL, &dwType,(LPBYTE)bufor, &dwSize);
        if (returnStatus == ERROR_SUCCESS) ret=1; 
    }
    RegCloseKey(hKey);
    return ret;
}

int get_program_path(char * pBuf, int len)
{
    int bytes = GetModuleFileName(NULL, pBuf, len), i;
    if(bytes == 0)        
        pBuf[0]=0;
    else
        if(bytes>0)
        {  for(i=bytes-1; i>0; i--)
            {  if(pBuf[i]=='/' || pBuf[i]=='\\')
                {  pBuf[i]=0;
                    break;
                }
            }
        }
}


int WINAPI WinMain(
	HINSTANCE hInstance,
	HINSTANCE hPrevInstance,
	LPSTR lpCmdLine,
	int nCmdShow)
{
    char bufor[256], bufor2[256];    
    if(key(bufor)!=1) get_program_path(bufor,256);
    chdir(bufor);
    strcat(bufor, "\\python\\pythonw.exe");
    strcpy(bufor2, "pytigon ");
    strcat(bufor2, lpCmdLine);
    execl(bufor, bufor, bufor2, NULL);
    
    return 0;
}

