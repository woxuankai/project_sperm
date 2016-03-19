//data path:
//TX:
//transmit =queue=> threadtx =dma= TX
//TX =intterrupt--semphore=> threadtx
//RX:
//threadrx =quiery-queue=> recv

#include <stdint.h>
#include <string.h>
#include <stdio.h>
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

//receive a message
uart_memblk_pt uart_receive(char *uartname, uint32_t time);

////warning!!!!!!!!!!!!!!!input of uart should not be '\0'//////
///or there may be err///
#define FUNC_RECV_COMMON_GENERATOR(TYPE)\
void func_recv_##TYPE(void const * argument)\
{\
	uint32_t taskinterval = UART##TYPE##_QUIERY_INTERVAL;\
    uint32_t PreviousWakeTime;\
    HAL_StatusTypeDef halstatus;\
    osStatus osstatus;\
    UART_HandleTypeDef* huart_p = &huart##TYPE;\
    \
    /*v <-- buff_base           */\
    /*0 1 2 3 4 5 6 7 8 9 10    */\
    /*x x x d d d d d x x x     */\
    /*      ^         ^         */\
    /*lastread:3 dma_offset:8   */\
    /*offset range 0:buff_size-1*/\
    /*lastread_offset: points to first   valid data*/\
    /*dma_offset     : points to first invalid data*/\
    /*in stm32, dma_offset = buff_size - CNDTR*/\
    \
    /*if dma reloaded           */\
    /*v <-- buff_base           */\
    /*0 1 2 3 4 5 6 7 8 9 10    */\
    /*d d d x x x x x d d d     */\
    /*      ^         ^         */\
    /*dma_offset:3 lastoffset:8 */\
    const char* buff_base = UART##TYPE##_BUFF;\
    const int32_t buff_size = UART##TYPE##_BUFF_SIZE;\
    uint32_t buff_dma_offset   = 0;\
    uint32_t buff_last_offset  = 0;\
    uint8_t* memblkstart_p;\
    int32_t memblkleft;\
    int32_t size2cpy;\
    \
    uint8_t* memblk_p = NULL;\
    const int32_t memblk_size = MEM_BLOCK_SIZE;\
    /*uint8_t* memblk_last_p;*/\
    \
    const osMessageQId queue = TYPE##_r_queueHandle;\
    \
    /*start dma in circulate mode*/\
    halstatus = HAL_UART_Receive_DMA(huart_p, \
            (uint8_t*)UART##TYPE##_BUFF, buff_size);\
    \
    if(halstatus != HAL_OK)\
    {/*failed to start dma*/\
        console_runtimereport(CONSOLE_ERROR,\
            "FUNC_RECV_"#TYPE": failed to start dma");\
        goto taskfailure;\
    }\
    \
    /*infinite loop*/\
	PreviousWakeTime = osKernelSysTick();\
    for(;;)\
    {\
preparepackage:\
        buff_dma_offset = buff_size - \
                huart_p->hdmarx->Instance->CNDTR;\
        if(buff_dma_offset == buff_last_offset)\
        {/*no message available*/\
            goto taskwait;\
        }\
        memblk_p = memblk_take();\
        if(memblk_p == NULL)\
        {/*no space left*/\
            console_runtimereport(CONSOLE_WARNING,\
                    "FUNC_RECV_"#TYPE":\
                    failed to take memblk, \
                    uart package may get lost");\
            goto taskwait;\
        }\
        /*message available and fetched memblk*/\
        /*prepare memblk*/\
        memblkstart_p = memblk_p;\
        memblkleft = memblk_size;\
        do{\
            if(buff_last_offset < buff_dma_offset)\
            {/*dma not reloaded*/\
                size2cpy = buff_dma_offset - buff_last_offset;\
            }else\
            {/*dma reloaded*/\
                size2cpy = buff_size - buff_last_offset;\
            }\
            if(size2cpy > memblkleft-1)\
                size2cpy = memblkleft-1;\
            memcpy(memblkstart_p, \
                    (void*)(buff_base+buff_last_offset),size2cpy);\
            memblkstart_p[size2cpy] = '\0';\
            \
            memblkstart_p = memblkstart_p + size2cpy;\
            memblkleft = memblkleft - size2cpy;\
            buff_last_offset = buff_last_offset + size2cpy;\
            buff_last_offset = buff_last_offset % buff_size;\
        }while((memblkstart_p - memblk_p != memblk_size-1)&&\
                (buff_last_offset != buff_dma_offset));\
        /*reaching here means memblk is full or message is empty*/\
        osstatus = osMessagePut(queue,(uint32_t)memblk_p,0);\
        if(osstatus != osOK)\
        {\
            console_runtimereport(CONSOLE_WARNING,"FUNC_RECV_"#TYPE": \
                    failed put package to the queue! \
                    packages is dropped!");\
           \
            if(memblk_free(memblk_p) != 0)\
            {\
                console_runtimereport(CONSOLE_WARNING,\
                        "FUNC_RECV_"#TYPE": \
                        failed to free memblk, memory lost!");\
            }\
        }\
        if(buff_last_offset != buff_dma_offset)\
        {/*message left*/\
            goto preparepackage;\
        }\
taskwait:\
        osDelayUntil(&PreviousWakeTime, taskinterval);\
    }\
taskfailure:\
	console_runtimereport(CONSOLE_ERROR,\
            "FUNC_RECV_"#TYPE": failed to start");\
    if(osThreadTerminate(NULL) != osOK)\
        console_runtimereport(CONSOLE_ERROR,\
                "FUNC_RECV_"#TYPE": failed to terminate thread");\
    return ;\
}
FUNC_RECV_COMMON_GENERATOR(wifi)
FUNC_RECV_COMMON_GENERATOR(ctrl)
FUNC_RECV_COMMON_GENERATOR(data)


#define SEND_TIME_OUT 100
#define FUNC_SEND_COMMON_GENERATOR(TYPE)\
void func_send_##TYPE(void const * argument)\
{\
	uart_memblk_pt rptr = NULL;\
	osEvent  evt;\
	int32_t len=0;\
	HAL_StatusTypeDef halstatus;\
	int32_t osstatus;\
	int status;\
\
	goto waitfor_package;\
	/*osSemaphoreRelease(TYPE##_t_cpltHandle);*/\
	for(;;)\
	{\
waitfor_package:\
		/*step 1*/\
		/*wait and check event and package*/\
		evt = osMessageGet(TYPE##_t_queueHandle, osWaitForever);\
		if (evt.status != osEventMessage)\
		{\
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_send_"#TYPE": unknown msg");\
			continue;\
		}\
		rptr = (uart_memblk_pt)evt.value.v;\
		if(rptr == NULL)\
		{\
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_send_"#TYPE": NULL memblk ptr");\
			continue;\
		}\
\
		goto send_package;\
send_package:\
		/*step2*/\
		/*successed receive block*/\
		/*try to send package*/\
		/*need to free block before next loop;*/\
\
		/*in case of invalid string*/\
		((uint8_t *)rptr)[MEM_BLOCK_SIZE-1] = 0;\
		len = strlen((char*)rptr);\
		if(len <= 0)\
		{\
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_send_"#TYPE": empty string");\
			goto free_memblk;\
		}\
		osSemaphoreWait(TYPE##_t_cpltHandle, 0);\
		/*//clean semaphore//no check*/\
		halstatus =	HAL_UART_Transmit_DMA(&huart##TYPE,(uint8_t *)rptr,len);\
		if(halstatus != HAL_OK)\
		{\
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_send_"#TYPE": failed to start dma");\
			goto free_memblk;\
		}\
		/*wait for dma transmit cplt*/\
		osstatus = osSemaphoreWait(TYPE##_t_cpltHandle,SEND_TIME_OUT);\
		if(osstatus != osOK)\
		{\
			console_runtimereport(CONSOLE_ERROR,\
                "sourec: func_send_"#TYPE": tx dma time out");\
			goto free_memblk;\
		}\
\
free_memblk:\
		/*step 3*/\
		/*free memory block*/\
		status = memblk_free((void*)rptr);\
		if(status < 0)\
		{\
			console_runtimereport(CONSOLE_ERROR,\
                "sourec: func_send_"#TYPE": failed to free memblk");\
			goto waitfor_package;\
		}\
		goto waitfor_package;\
	}\
	/*return;*/\
}

FUNC_SEND_COMMON_GENERATOR(wifi)
FUNC_SEND_COMMON_GENERATOR(data)
FUNC_SEND_COMMON_GENERATOR(ctrl)




void func_handle_data(void const * argument)
{
    uart_memblk_pt rptr = NULL;
	osEvent  evt;
    for(;;)
    {
        //p = memblk_take();
        //if(p == NULL)
        //    continue;
        //snprintf(p, MEM_BLOCK_SIZE,"hello!\r\n");
		//uart_transmit(ctrl,p,100);
        //osMessagePut(ctrl_t_queueHandle,(uint32_t)p,0);
        //osDelay(1000);
        
        //p = memblk_take();
        //if(p == NULL)
        //    continue;
        //snprintf(p, MEM_BLOCK_SIZE,"this is uartctrl!\r\n");
        //uart_transmit(ctrl,p,100);
		//osMessagePut(ctrl_t_queueHandle,(uint32_t)p,0);
        //osDelay(1000);
        
        //console_runtimereport(CONSOLE_WARNING,"fuck! ""unknown huart");
        //console_runtimereport(CONSOLE_WARNING,"fuck! ""unknown huart");
        //osDelay(1000);
        evt = osMessageGet(ctrl_r_queueHandle, osWaitForever);
		if (evt.status != osEventMessage)
		{
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_test : unknown msg");
			continue;
		}
        rptr = (uart_memblk_pt)evt.value.v;
		if(rptr == NULL)
		{
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_test: NULL memblk ptr");
			continue;
		}
        if(memblk_free(rptr) != 0)
            console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_test: failed to free package");
    }
}

void func_handle_ctrl(void const * argument)
{
    uart_memblk_pt rptr = NULL;
	osEvent  evt;
    osMessageQId* queue = &ctrl_r_queueHandle;
    for(;;)
    {
        evt = osMessageGet(*queue, osWaitForever);
		if (evt.status != osEventMessage)
		{
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_test : unknown msg");
			continue;
		}
        rptr = (uart_memblk_pt)evt.value.v;
		if(rptr == NULL)
		{
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_test: NULL memblk ptr");
			continue;
		}
        
        if(osMessagePut(wifi_t_queueHandle,(uint32_t)rptr,0) != osOK)
        {    
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_test: failed to put package");
            if(memblk_free(rptr) != 0)
                console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_test: failed to free package");
        }
    }
}

void func_handle_wifi(void const * argument)
{
    uart_memblk_pt rptr = NULL;
	osEvent  evt;
    osMessageQId* queue = &wifi_r_queueHandle;
    for(;;)
    {
        evt = osMessageGet(*queue, osWaitForever);
		if (evt.status != osEventMessage)
		{
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_test : unknown msg");
			continue;
		}
        rptr = (uart_memblk_pt)evt.value.v;
		if(rptr == NULL)
		{
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_test: NULL memblk ptr");
			continue;
		}
        
        if(osMessagePut(ctrl_t_queueHandle,(uint32_t)rptr,0) != osOK)
        {    
			console_runtimereport(CONSOLE_WARNING,\
                "sourec: func_handle_wifi: failed to put package");
            if(memblk_free(rptr) != 0)
                console_runtimereport(CONSOLE_WARNING,\
                    "sourec: func_handle_wifi: failed to free package");
        }
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
		console_runtimereport(CONSOLE_WARNING,"unknown txcplt huart");
}



