#include "console.h"
#include "memblk.h"
#include "stm32f1xx_hal.h"
#include <string.h>
#include "usart.h"
#include "uart_driver.h"

int32_t unreportedwarningcnt = 0;
int32_t unreportedwarningcnt_continues = 0;

char consolersv[MEM_BLOCK_SIZE];

int console_problemhandle(CONSOLE_LEVEL level, char * file, char * line, char* msg)
{
    char* p;
    if(level == CONSOLE_WARNING)
    {
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
        strncat(p, "\r\nWarning Report:",MEM_BLOCK_SIZE - strlen(p)-1);
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
    //system unable to continue to work
    else// if(level == CONSOLE_ERROR)
    {
        osThreadSuspendAll();
        strcpy(consolersv, "\r\nError Report:\r\nSystem halted!");
        strncat(consolersv, "\r\nin line: ", MEM_BLOCK_SIZE - strlen(consolersv)-1);
        strncat(consolersv, line, MEM_BLOCK_SIZE - strlen(consolersv));
        strncat(consolersv, "\r\nin file: ", MEM_BLOCK_SIZE - strlen(consolersv)-1);
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
            
            HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin,  GPIO_PIN_LEDON);
            HAL_Delay(ON_TIME_S);
            HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin,  GPIO_PIN_LEDOFF);
            HAL_Delay(OFF_TIME);
            
            HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin,  GPIO_PIN_LEDON);
            HAL_Delay(ON_TIME_S);
            HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin,  GPIO_PIN_LEDOFF);
            HAL_Delay(OFF_TIME);     
            
            HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin,  GPIO_PIN_LEDON);
            HAL_Delay(ON_TIME_S);
            HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin, GPIO_PIN_LEDOFF);
            HAL_Delay(OFF_TIME);    
            
            HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin,  GPIO_PIN_LEDON);
            HAL_Delay(ON_TIME_L);
            HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin, GPIO_PIN_LEDOFF);
            HAL_Delay(OFF_TIME); 
            
            HAL_UART_Transmit_DMA(&huartctrl,(uint8_t *)consolersv, strlen(consolersv));
        }
    }
    //return 0;
}
