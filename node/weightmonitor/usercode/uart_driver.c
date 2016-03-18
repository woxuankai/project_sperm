//data path:
//TX:
//transmit =queue=> threadtx =dma= TX
//TX =intterrupt--semphore=> threadtx
//RX:
//threadrx =quiery-queue=> recv

#include <stdint.h>
#include <string.h>
#include "uart_driver.h"
#include "usart.h"
#include "stm32f1xx_hal.h"
#include "cmsis_os.h"
#include "memblk.h"
#include "usart.h"
#include "console.h"

char UART1_BUFF[UART1_BUFF_SIZE] = {0};
char UART2_BUFF[UART2_BUFF_SIZE] = {0};
char UART3_BUFF[UART3_BUFF_SIZE] = {0};


extern osMessageQId data_r_queueHandle;
extern osMessageQId data_t_queueHandle;
extern osMessageQId wifi_r_queueHandle;
extern osMessageQId wifi_t_queueHandle;
extern osMessageQId ctrl_r_queueHandle;
extern osMessageQId ctrl_t_queueHandle;
extern osSemaphoreId data_t_cpltHandle;
extern osSemaphoreId wifi_t_cpltHandle;
extern osSemaphoreId ctrl_t_cpltHandle;


//receive a message
uart_memblk_pt uart_receive(char *uartname, uint32_t time);

//transmit a message
int uart_transmit(char *uartname, uart_memblk_pt pack, uint32_t time);


void func_recv_data(void const * argument)
{
	uint32_t PreviousWakeTime;
	PreviousWakeTime = osKernelSysTick();
  for(;;)
  {		
    osDelayUntil(&PreviousWakeTime, UART_QUIERY_INTERVAL);
  }

//	if(osThreadTerminate(NULL) != osOK)
//	{
//		//something went wrong
//	}
//	return ;
}
void func_recv_ctrl(void const * argument)
{
	uint32_t PreviousWakeTime;
	PreviousWakeTime = osKernelSysTick();
  for(;;)
  {		
    osDelayUntil(&PreviousWakeTime, UART_QUIERY_INTERVAL);
  }
	
//	if(osThreadTerminate(NULL) != osOK)
//	{
//		//something went wrong
//	}
//	return ;
}
void func_recv_wifi(void const * argument)
{
	uint32_t PreviousWakeTime;
	PreviousWakeTime = osKernelSysTick();
  for(;;)
  {
    osDelayUntil(&PreviousWakeTime, UART_QUIERY_INTERVAL);
  }
//	if(osThreadTerminate(NULL) != osOK)
//	{
//		//something went wrong
//	}
//	return ;
}


#define FUNC_SEND_COMMON_GENERATOR(TYPE)				\
void func_send_##TYPE(void const * argument)		\
{																								\
	uart_memblk_pt rptr = NULL;										\
	osEvent  evt;																	\
	int32_t len=0;																\
	HAL_StatusTypeDef halstatus;									\
	int32_t osstatus;															\
	int status;																		\
																								\
	goto waitfor_package;													\
	/*osSemaphoreRelease(ctrl_t_cpltHandle);*/		\
	for(;;)																				\
	{																							\
waitfor_package:																\
		/*step 1*/																	\
		/*wait and check event and package*/				\
		evt = 																			\
			osMessageGet(ctrl_t_queueHandle,					\
										osWaitForever);							\
		if (evt.status != osEventMessage)						\
		{																						\
			console_runtimereport(CONSOLE_WARNING,						\
											"unknown msg");						\
			continue;																	\
		}																						\
		rptr = (uart_memblk_pt)evt.value.v;					\
		if(rptr == NULL)														\
		{																						\
			console_runtimereport(CONSOLE_WARNING,						\
											"NULL memblk ptr");				\
			continue;																	\
		}																						\
		goto send_package;													\
																								\
send_package:																		\
		/*step 2*/																	\
		/*successed receive block*/									\
		/*try to send package*/											\
		/*need to free block before next loop;*/		\
																								\
		/*in case of invalid string*/								\
		((uint8_t *)rptr)[MEM_BLOCK_SIZE-1] = 0;		\
		len = strlen((char*)rptr);									\
		if(len <= 0)																\
		{																						\
			console_runtimereport(CONSOLE_WARNING,						\
											"empty string");					\
			goto free_memblk;													\
		}																						\
		osSemaphoreWait(ctrl_t_cpltHandle, 0);			\
		/*//clean semaphore//no check*/							\
		halstatus = 																\
			HAL_UART_Transmit_DMA(&huart##TYPE,				\
														(uint8_t *)rptr,		\
														len);								\
		if(halstatus != HAL_OK)											\
		{																						\
			console_runtimereport(CONSOLE_WARNING,						\
											"failed to start dma");		\
			goto free_memblk;													\
		}																						\
		/*wait for dma transmit cplt*/							\
		osstatus = 																	\
			osSemaphoreWait(ctrl_t_cpltHandle,				\
											osWaitForever);						\
		if(osstatus != osOK)												\
		{																						\
			console_runtimereport(CONSOLE_ERROR,							\
										"failed to wait");					\
			goto free_memblk;													\
		}																						\
																								\
free_memblk:																		\
		/*step 3*/																	\
		/*free memory block*/												\
		status = memblk_free((void*)rptr);					\
		if(status < 0)															\
		{																						\
			console_runtimereport(CONSOLE_ERROR,							\
											"failed to free memblk");	\
			goto waitfor_package;											\
		}																						\
		goto waitfor_package;												\
	}																							\
	/*return;*/																		\
}																								\

FUNC_SEND_COMMON_GENERATOR(wifi)
FUNC_SEND_COMMON_GENERATOR(ctrl)
FUNC_SEND_COMMON_GENERATOR(data)


void func_handle_data(void const * argument)
{
  for(;;)
  {
    osDelay(1);
  }
}
void func_handle_ctrl(void const * argument)
{
  for(;;)
  {
		osDelay(1);
  }
}
void func_handle_wifi(void const * argument)
{
  for(;;)
  {
    osDelay(1);
  }
}

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
  if(huart == &huartdata)
		osSemaphoreRelease(data_t_cpltHandle);
	else if(huart == &huartctrl)
		osSemaphoreRelease(ctrl_t_cpltHandle);
	else if(huart == &huartwifi)
		osSemaphoreRelease(wifi_t_cpltHandle);
	else
		console_runtimereport(CONSOLE_WARNING,"unknown huart");//error report
}
