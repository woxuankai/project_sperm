#include "ledctrl.h"

#include <stdint.h>
#include "stm32f1xx_hal.h"

#include "FreeRTOS.h"
#include "task.h"
#include "mxconstants.h"
#include "cmsis_os.h"

extern osTimerId led0Handle;


int32_t ledflash(int dev, int time)
{
    int osstatus;
    switch(dev)
    {
        case devLED0: 
        {
            LED_ON(devLED0);
            osstatus = osTimerStart( led0Handle, time);
            if(osstatus == osOK)
                return 0;
            else 
                return -1;
        }
        default:
            return -1;       
    }
}



void Callback_led0(void const * argument)
{
	HAL_GPIO_TogglePin(devLED0_GPIO_Port, devLED0_Pin );
    return;
}
