#include "console.h"
#include "memblk.h"
#include "stm32f1xx_hal.h"
#include <string.h>
#include "usart.h"
#include "uart_driver.h"

int32_t unreportedwarningcnt = 0;
int32_t unreportedwarningcnt_continues = 0;

char consolersv[MEM_BLOCK_SIZE];

int console_messagehandle(char * file, char * line, char* msg);
int console_warninghandle(char * file, char * line, char* msg);
int console_errorhandle(char * file, char * line, char* msg);

int console_problemhandle(CONSOLE_LEVEL level, char * file, char * line, char* msg)
{
    switch(level)
    {
        case CONSOLE_MESSAGE:
            return console_messagehandle(file, line, msg);
        case CONSOLE_WARNING:
            return console_warninghandle(file, line, msg);
        default ://ERROR and others//
            return console_errorhandle(file, line, msg);
    }
}


int console_messagehandle(char * file, char * line, char* msg)
{
    char* p;
    p = memblk_take();
    if(p == NULL)
    {
        console_problemhandle(CONSOLE_WARNING , file, line,\
                "failed to get memblk");
        return -1;
    }
    strncpy(p,"",MEM_BLOCK_SIZE-1);
    strncat(p, "\r\nMSG!",MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, "\r\nfile: ", MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, file, MEM_BLOCK_SIZE - strlen(p));
    strncat(p, "\r\nline: ", MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, line, MEM_BLOCK_SIZE - strlen(p));
    strncat(p, "\r\nMSG: ", MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, msg, MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, "\r\n", MEM_BLOCK_SIZE - strlen(p)-1);
    if(osOK == osMessagePut(ctrl_t_queueHandle,(uint32_t)p,0))
    {
        return 0;
    }
    else
    {
        memblk_free(p);
        console_problemhandle(CONSOLE_WARNING , file, line, \
                "failed to put message to queue");
        return -1;
    }
}

int console_warninghandle(char * file, char * line, char* msg)
{
    char* p;
    if(unreportedwarningcnt_continues > 20)
    {
        console_problemhandle(CONSOLE_ERROR , file, line, msg);
    }
    p = memblk_take();
    if(p == NULL)
    {
        unreportedwarningcnt++;
        unreportedwarningcnt_continues++;
        return -1;
    }
    if(unreportedwarningcnt == 0)
        strncpy(p,"",MEM_BLOCK_SIZE-1);
    else
        snprintf(p, MEM_BLOCK_SIZE-1, "\r\nlost warnings cnt : %d",unreportedwarningcnt);
    strncat(p, "\r\nWarning!!",MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, "\r\nfile: ", MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, file, MEM_BLOCK_SIZE - strlen(p));
    strncat(p, "\r\nline: ", MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, line, MEM_BLOCK_SIZE - strlen(p));
    strncat(p, "\r\nMSG: ", MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, msg, MEM_BLOCK_SIZE - strlen(p)-1);
    strncat(p, "\r\n", MEM_BLOCK_SIZE - strlen(p)-1);
    if(osOK == osMessagePut(ctrl_t_queueHandle,(uint32_t)p,0))
    {
        unreportedwarningcnt_continues = 0;
        return 0;
    }
    else
    {
        memblk_free(p);
        unreportedwarningcnt++;
        unreportedwarningcnt_continues++;
        return -1;
    }
}
int console_errorhandle(char * file, char * line, char* msg)
{
    //system unable to continue to work
    osThreadSuspendAll();
    strcpy(consolersv, "\r\nError!!");
    strncat(consolersv, "\r\nline: ", MEM_BLOCK_SIZE - strlen(consolersv)-1);
    strncat(consolersv, line, MEM_BLOCK_SIZE - strlen(consolersv));
    strncat(consolersv, "\r\nfile: ", MEM_BLOCK_SIZE - strlen(consolersv)-1);
    strncat(consolersv, file, MEM_BLOCK_SIZE - strlen(consolersv)-1);
    strncat(consolersv, "\r\nMSG: ", MEM_BLOCK_SIZE - strlen(consolersv)-1);
    strncat(consolersv, msg, MEM_BLOCK_SIZE - strlen(consolersv)-1);
    strncat(consolersv, "\r\n", MEM_BLOCK_SIZE - strlen(consolersv)-1);
    //in case
    consolersv[MEM_BLOCK_SIZE-1] = 0;
    for(;;)
    {
        #define ON_TIME_S 50
        #define ON_TIME_L 500
        #define OFF_TIME 200
        #define GPIO_PIN_LEDON GPIO_PIN_RESET
        #define GPIO_PIN_LEDOFF GPIO_PIN_SET
        
        HAL_GPIO_WritePin(devLED0_GPIO_Port, devLED0_Pin,  GPIO_PIN_LEDON);
        HAL_Delay(ON_TIME_S);
        HAL_GPIO_WritePin(devLED0_GPIO_Port, devLED0_Pin,  GPIO_PIN_LEDOFF);
        HAL_Delay(OFF_TIME);
        
        HAL_GPIO_WritePin(devLED0_GPIO_Port, devLED0_Pin,  GPIO_PIN_LEDON);
        HAL_Delay(ON_TIME_S);
        HAL_GPIO_WritePin(devLED0_GPIO_Port, devLED0_Pin,  GPIO_PIN_LEDOFF);
        HAL_Delay(OFF_TIME);     
        
        HAL_GPIO_WritePin(devLED0_GPIO_Port, devLED0_Pin,  GPIO_PIN_LEDON);
        HAL_Delay(ON_TIME_S);
        HAL_GPIO_WritePin(devLED0_GPIO_Port, devLED0_Pin, GPIO_PIN_LEDOFF);
        HAL_Delay(OFF_TIME);    
        
        HAL_GPIO_WritePin(devLED0_GPIO_Port, devLED0_Pin,  GPIO_PIN_LEDON);
        HAL_Delay(ON_TIME_L);
        HAL_GPIO_WritePin(devLED0_GPIO_Port, devLED0_Pin, GPIO_PIN_LEDOFF);
        HAL_Delay(OFF_TIME); 
        
        HAL_UART_Transmit_DMA(&huartctrl,(uint8_t *)consolersv, strlen(consolersv));
    }
}
