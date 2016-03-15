#ifndef UART_DRIVER_H
#define UART_DRIVER_H

#include "memblk.h"

//buff size setting
/////////////////////////////////////////////////////////////////////////////
#define UART_QUIERY_INTERVAL 20 //ms
//115200 bps
//(((uint32_t)(115200/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4) = 460.8
#define UARTCTRL_BUFF_SIZE 464
//9600 bps
//(((uint32_t)(9600/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4) = 38.4
#define UARTDATA_BUFF_SIZE 40
//115200 bps
//(((uint32_t)(115200/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4) = 460.8
#define UARTWIFI_BUFF_SIZE  464

//uart redifine
////////////////////////////////////////////////////////////////////////////
#define UART1_BUFF_SIZE UARTCTRL_BUFF_SIZE
#define UART2_BUFF_SIZE UARTDATA_BUFF_SIZE
#define UART3_BUFF_SIZE UARTWIFI_BUFF_SIZE

#define UARTCTRL_BUFF UART1_BUFF
#define UARTDATA_BUFF UART2_BUFF
#define UARTWIFI_BUFF UART3_BUFF

#define UART_MEM_BLOCK_SIZE MEM_BLOCK_SIZE
#define uart_mempool mempool
//typedef
////////////////////////////////////////////////////////////////////////////
typedef memblk_t uart_memblk_t;
typedef uart_memblk_t* uart_memblk_pt;

#endif 
