#include "mainthread.h"
#include "cmsis_os.h"
#include "memblk.h"
#include <stdint.h>
#include "mxconstants.h"
#include "wifictrl.h"
#include "console.h"

char* string_ready =    "dy\r\n";
char* string_OK =       "OK\r\n";
char* string_ERROR =    "OR\r\n"; 
char* string_IP =       "IP\r\n";

//typedef enum {
//    nostring,
//    //ready,
//    OK,
//    ERROR,
//    IP,//gotten ip
//} returnstring;

//state machine
char* waitforstring(uint32_t timeout,osMessageQId* queue_p)
{
    uint32_t outtime;
    uint32_t timeleft;
    char gotchar;
    osEvent  evt;
    
    outtime = osKernelSysTick() + osKernelSysTickMicroSec(timeout*1000);
    
#define TIMELEFT \
            (outtime > osKernelSysTick()/osKernelSysTickMicroSec(1000))?\
            (outtime - osKernelSysTick()/osKernelSysTickMicroSec(1000)):0
    
#define WAITCHAR(ch) \
        {\
            timeleft = TIMELEFT;\
            evt = osMessageGet(*queue_p,timeleft);\
            if(evt.status != osEventMessage)\
                return NULL;\
            ch = evt.value.v;\
        }
        
    start:
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    gotO:
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case 'K': goto gotOK;
        case 'R': goto gotOR;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    gotOK:
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case '\r': break;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case '\n': goto gotOKrn;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    gotOR:
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case '\r': break;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case '\n': goto gotORrn;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    gotI:
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case 'P': goto gotIP;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    gotIP:
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case '\r': break;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case '\n': goto gotIPrn;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    gotd:
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case 'y': goto gotdy;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    gotdy:
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case '\r': break;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    WAITCHAR(gotchar);
    switch(gotchar)
    {
        case '\n': goto gotdyrn;
        case 'O': goto gotO;
        case 'I': goto gotI;
        case 'd': goto gotd;
        default : goto start;
    };
    gotORrn:
    return string_ERROR;
    gotIPrn:
    return string_IP;
    gotdyrn:
    return string_ready;
    gotOKrn:
    return string_OK;
#undef TIMELEFT 
#undef WAITCHAR
}


int waitfordata(memblk_t* memblk, uint32_t timeout,osMessageQId* queue_p)
{
    
    uint32_t outtime;
    uint32_t timeleft;
    char gotchar;
    osEvent  evt;
    
    outtime = osKernelSysTick() + osKernelSysTickMicroSec(timeout*1000);
    
#define TIMELEFT \
            (outtime > osKernelSysTick()/osKernelSysTickMicroSec(1000))?\
            (outtime - osKernelSysTick()/osKernelSysTickMicroSec(1000)):0
    
#define WAITCHAR(ch) \
        {\
            timeleft = TIMELEFT;\
            evt = osMessageGet(*queue_p,timeleft);\
            if(evt.status != osEventMessage)\
                return -1;\
            ch = evt.value.v;\
        }
        
    char* pdata = (char*)memblk;
    int i;

    if(pdata == NULL)
        return -1;
    for(i=0; i<= MEM_BLOCK_SIZE-1; i++)
    {
        WAITCHAR(gotchar)
        if(gotchar == '\r')
        {
            *pdata = '\0';
            WAITCHAR(gotchar);//assum there is a \n after \n
            return 0;
        }
        *pdata = gotchar;
        pdata++;
    }
    //WTF?
    *pdata = '\0';
    return -1;//overflow
#undef TIMELEFT 
#undef WAITCHAR
}


void func_mainthread(void const * argument)
{
    char * returnstr;
    init:
    WIFI_OFF;
    osDelay(2000);
    WIFI_ON;
    returnstr = waitforstring(2000,&wifirecv_queueHandle);
    if(returnstr == NULL)
    {
        console_runtimereport(CONSOLE_ERROR,\
                    "sourec: func_mainthread: "\
                    "failed to communicate with wifi");
    }
    else if(returnstr != string_ready)
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "wifi didn't return ready\r\n retry");
        goto init;
    }
    returnstr = waitforstring(10000,&wifirecv_queueHandle);
    if(returnstr != string_IP)
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "wifi didn't return get ip\r\n retry");
        goto init;
    }
    for(;;)
    {
        osDelay(10086);
    }
}
