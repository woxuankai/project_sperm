#include "ledctrl.h"

#include <stdint.h>
#include "stm32f1xx_hal.h"


int32_t led0changeperiod(int period);
int32_t	led0start(void);
int32_t led0stop(void);
/*
#define LED_DEVICE_NUM 1
#define LED_PERIOD_MAX 1000	//1Hz
#define LED_PERIOD_MIN 50		//20Hz


int32_t ledctl(int32_t dev, uint32_t cmd, int32_t arg);
int32_t ledduty[LED_DEVICE_NUM] = {0};
int32_t ledperiod[LED_DEVICE_NUM] = {0};
*/

/*
int32_t ledctl(int32_t dev, uint32_t cmd, int32_t arg)
{
	if (dev <0 || dev >= LED_DEVICE_NUM)
		return -1;
	switch(cmd)
	{
		case LEDCMD_QUERYPERIOD: 
			break;
		case LEDCMD_QUERYDUTY: 
			break;
		case LEDCMD_SETPERIOD: break;
		case LEDCMD_SETDUTY: break;
		default: 
			return -1;
			break;
	}
	return -1;
}
*/
#include "FreeRTOS.h"
#include "task.h"
#include "mxconstants.h"
#include "cmsis_os.h"

extern osTimerId led0Handle;

int32_t led0changeperiod(int period)
{
	if( xTimerChangePeriod(led0Handle, period/2, 100) == pdPASS )
		return 0;
	else
		return -1;
}
int32_t	led0start(void)
{
	if( xTimerIsTimerActive( led0Handle ) != pdFALSE )
	{//Timer active
		//do nothing
	}
    else
    {//xTimer is not active
         if(xTimerStart( led0Handle, 100) == pdPASS)
			return 0;
		 else return -1;
    }
	//should not come here
	return -1;
}
int32_t led0stop(void)
{
	if( xTimerIsTimerActive( led0Handle ) != pdFALSE )
	{//Timer active
         if(xTimerStop(led0Handle, 100) == pdPASS)
			return 0;
		 else return -1;
	}
    else
    {//xTimer is not active
		//do nothing
    }
	//should not come here
	return -1;
}






void Callback_led0(void const * argument)
{
	HAL_GPIO_TogglePin( LED0_GPIO_Port, LED0_Pin );
}



/*
void func_LEDctrl(void const * argument)
{
	int32_t hightime = 100;
	int32_t lowtime = 100;
	TickType_t xLastWakeTime;
	xLastWakeTime = xTaskGetTickCount();
	while(1)
	{
		HAL_GPIO_WritePin(LED0_GPIO,LED0_Pin,GPIO_PIN_SET);
		vTaskDelayUntil( &xLastWakeTime, xFrequency );
	}
	vTaskDelete( NULL );	
	return ;
}
*/

