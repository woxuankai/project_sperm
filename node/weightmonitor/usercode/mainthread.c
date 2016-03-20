#include "mainthread.h"
#include "cmsis_os.h"
#include "memblk.h"
#include <stdint.h>
#include "mxconstants.h"
#include "wifictrl.h"
#include "console.h"
#include "uart_driver.h"
#include <string.h>
#include "ledctrl.h"

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

    //-2:timeout
    //-1:error
    //0:succeed
#define WAITCHAR(ch) \
        {\
            timeleft = TIMELEFT;\
            evt = osMessageGet(*queue_p,timeleft);\
            if(evt.status != osEventMessage)\
                return -2;\
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

char mainthreaddatabuff[MEM_BLOCK_SIZE] = {0};
char cmdsendstr[] = "AT+CIPSEND=008\r\n";
void func_mainthread(void const * argument)
{
    char * returnstr;
    osEvent  evt;
    char * p;
    int status;
    int failedtime=0;
    int datalen;
#define ESP8266sendcmd(cmd,failedtag,retrytime,waittime) \
{\
    failedtime=0;\
    do{\
        p = memblk_take();\
        if(p == NULL)\
        {\
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: ESP8266sendcmd: "\
                        "failed to fetch memblk,\r\nretry");\
            failedtime ++;\
            if(failedtime > retrytime)\
            {\
                console_runtimereport(CONSOLE_WARNING,\
                            "sourec: ESP8266sendcmd: "\
                            "failed to execute cmd"\
                            "\r\ngoto failtag ");\
                goto failedtag;\
            }\
            osDelay(waittime);\
        }\
    }while(p==NULL);\
    failedtime=0;\
    strcpy(p,cmd);\
    /*dump all character*/\
    do\
    {\
        returnstr = waitforstring(0,&wifirecv_queueHandle);\
    }while(returnstr != NULL);\
    while(uart_transmit(wifi,p,1000) != osOK)\
    {\
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: ESP8266sendcmd: "\
                    "failed to send command,\r\nretry");\
        failedtime++;\
        if(failedtime > retrytime)\
        {\
            if(memblk_free(p) != 0)\
                console_runtimereport(CONSOLE_WARNING,\
                            "sourec: ESP8266sendcmd: "\
                            "failed to free membkl")\
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: ESP8266sendcmd: "\
                        "failed to send cmd"\
                        "\r\ngoto failtag");\
            goto failedtag;\
        }\
    }\
}

init:
    LED_ON(devLED0);
    WIFI_OFF;
    osDelay(2000);
    WIFI_ON;
    returnstr = waitforstring(2000,&wifirecv_queueHandle);
    if(returnstr == NULL)
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "failed to shake hand with ESP8266: time out"\
                    "\r\nretry");
        goto init;
    }
    else if(returnstr != string_ready)
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "wifi didn't return ready"\
                    "\r\nretry");
        goto init;
    }
    else
    {
        console_runtimereport(CONSOLE_MESSAGE,\
                "sourec: func_mainthread: "\
                "ESP8266 connected");
        goto setESP8266mode;
    }
setESP8266mode:
    ESP8266sendcmd("AT+CWMODE=1\r\n",init,3,5000);
    returnstr = waitforstring(2000,&wifirecv_queueHandle);
    if(returnstr == NULL)
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "response time out"\
                    "\r\nreinit");
        goto init;
    }
    else if(returnstr == string_OK)
    {
        console_runtimereport(CONSOLE_MESSAGE,\
                "sourec: func_mainthread: "\
                "ESP8266 mode changed");
        goto reinit;
    }
    else
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "wifi didn't return OK"\
                    "\r\nreinit");
        goto init;
    }
reinit:
    WIFI_OFF;
    osDelay(2000);
    WIFI_ON;
    returnstr = waitforstring(2000,&wifirecv_queueHandle);
    if(returnstr == NULL)
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "failed to shake hand with ESP8266: time out"\
                    "\r\nretry");
        goto init;
    }
    else if(returnstr != string_ready)
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "wifi didn't return ready"\
                    "\r\nretry");
        goto init;
    }
    else
    {
        console_runtimereport(CONSOLE_MESSAGE,\
                "sourec: func_mainthread: "\
                "ESP8266 reinit succeed!");
        goto setESP8266wifiinfo;
    }
setESP8266wifiinfo:
    ESP8266sendcmd("AT+CWJAP=\"CMCC_WIFI\",\"qwertyuiop\"\r\n",init,3,5000);
    returnstr = waitforstring(10000,&wifirecv_queueHandle);
    if(returnstr == NULL)
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "response time out"\
                    "\r\nreinit");
        goto init;
    }
    else if(returnstr == string_IP)
    {
        console_runtimereport(CONSOLE_MESSAGE,\
                "sourec: func_mainthread: "\
                "ESP8266 ssid and pwd changed"\
                "\r\nIP got");
        goto infiniteloop;
    }
    else
    {
        console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_mainthread: "\
                    "wifi didn't return OK"\
                    "\r\nreinit");
        goto init;
    }
//joinwifi:
//    returnstr = waitforstring(10000,&wifirecv_queueHandle);
//    if(returnstr != string_IP)
//    {
//        console_runtimereport(CONSOLE_WARNING,\
//                    "sourec: func_mainthread: "\
//                    "EPS8266 didn't get ip\r\n retry");
//        goto init;
//    }
//    else
//    {
//        console_runtimereport(CONSOLE_MESSAGE,\
//                "sourec: func_mainthread: "\
//                "EPS8266 connected to wifi");
//    }
    for(;;)
    {
/*
AT+CIPSTART="TCP","192.168.1.164",2333
CONNECT
OK
AT+CIPSEND=9
OK
> 
busy s...
Recv 9 bytes
SEND OK
CLOSED
*/
infiniteloop:
        console_runtimereport(CONSOLE_MESSAGE,\
                "sourec: func_mainthread: "\
                "Initialization finished!");
        LED_OFF(devLED0);
waitfordata:
        //osEventTimeout = 
        do{
            evt = osMessageGet(datarecv_queueHandle, 0);
        }while(evt.status == osEventMessage);
        do{
        #define WAITFORDATATIMEOUT 60000
            status = waitfordata((memblk_t*)mainthreaddatabuff,\
                            WAITFORDATATIMEOUT,&datarecv_queueHandle);
            if(status == -2)
            {
                console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "timeout :no data"\
                        "\r\ncontinue to wait");
            }
            else if(status != 0)
            {
                console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "waitfordata returned error"\
                        "\r\nretry");
            }
        }while(status != 0);
        //strcpy(mainthreaddatabuff,"c2:135.45\r\n");
        datalen = strlen(mainthreaddatabuff) - 2;
        goto tcpconnect;
tcpconnect:
        osDelay(2000);
        ESP8266sendcmd("AT+CIPSTART=\"TCP\",\"192.168.1.164\",2333\r\n",init,3,5000);
        returnstr = waitforstring(5000,&wifirecv_queueHandle);
        if(returnstr == NULL)
        {
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "response time out"\
                        "\r\nreinit");
            goto init;
        }
        else if(returnstr == string_OK)
        {
            console_runtimereport(CONSOLE_MESSAGE,\
                    "sourec: func_mainthread: "\
                    "TCP Connected");
            goto sendpackprepare;
        }
        else
        {
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "wifi didn't return OK"\
                        "\r\nreinit");
            goto init;
        }
sendpackprepare:
        osDelay(2000);
        if(strlen(cmdsendstr) > 999)
        {
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "data message package too long(> 999)"\
                        "\r\naborted");
            goto waitfordata;
        }
        cmdsendstr[strlen(cmdsendstr)-1-2-2] = (datalen/100)%10+'0';
        cmdsendstr[strlen(cmdsendstr)-1-2-1] = (datalen/10)%10+'0';
        cmdsendstr[strlen(cmdsendstr)-1-2-0] = (datalen/1)%10+'0';
        ESP8266sendcmd(cmdsendstr,init,3,5000);
        returnstr = waitforstring(5000,&wifirecv_queueHandle);
        if(returnstr == NULL)
        {
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "response time out"\
                        "\r\nreinit");
            goto init;
        }
        else if(returnstr == string_OK)
        {
            console_runtimereport(CONSOLE_MESSAGE,\
                    "sourec: func_mainthread: "\
                    "setted data size");
            goto sendpackage;
        }
        else
        {
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "wifi didn't return OK"\
                        "\r\nreinit");
            goto init;
        }
sendpackage:
        osDelay(4000);
        //ESP8266sendcmd("c2:13.45\r\n",init,3,5000);
        ESP8266sendcmd(mainthreaddatabuff,init,3,5000);
//        osDelay(200);
//        ESP8266sendcmd("+++\r\n",init,3,5000);
        returnstr = waitforstring(5000,&wifirecv_queueHandle);
        if(returnstr == NULL)
        {
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "response time out"\
                        "\r\nreinit");
            goto init;
        }
        else if(returnstr == string_OK)
        {
            console_runtimereport(CONSOLE_MESSAGE,\
                    "sourec: func_mainthread: "\
                    "sent data");
            goto finishtransmit;
        }
        else
        {
            console_runtimereport(CONSOLE_WARNING,\
                        "sourec: func_mainthread: "\
                        "wifi didn't return OK"\
                        "\r\nreinit");
            goto init;
        }
finishtransmit:
        ledflash(devLED0,200);
        goto waitfordata;
    }
}
