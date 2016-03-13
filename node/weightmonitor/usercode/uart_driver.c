#include "uart_driver.h"
#include "usart.h"

#include "stm32f1xx_hal.h"

#include "buffpool.h"



#include <stdint.h>
#define UART_QUIERY_INTERVAL 20
//115200 bps
#define UART1_BUFF_SIZE (((uint32_t)(115200/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4)
//115200 bps
#define UART2_BUFF_SIZE (((uint32_t)(115200/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4)
//9600 bps
#define UART3_BUFF_SIZE (((uint32_t)(9600/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4)

#define UARTCTRL_BUFF_SIZE UART1_BUFF_SIZE
#define UARTWIFI_BUFF_SIZE UART2_BUFF_SIZE
#define UARTDATA_BUFF_SIZE UART3_BUFF_SIZE

char UART1_BUFF[UART1_BUFF_SIZE] = {0};
char UART2_BUFF[UART2_BUFF_SIZE] = {0};
char UART3_BUFF[UART3_BUFF_SIZE] = {0};

//reset prepare to receive new message
int uart_start(UART_HandleTypeDef *huart);

//clean buffer and ignore any message
int uart_stop(UART_HandleTypeDef *huart);

//clean buffer and prepare to receive new message
int uart_reset(UART_HandleTypeDef *huart);

//receive a message
//in block mode
int uart_receive(UART_HandleTypeDef *huart, p_buff_block_t);

//transmit a message
//in block mode if uart device is busy
int uart_transmit(UART_HandleTypeDef *huart,p_buff_block_t);


void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
  UNUSED(huart);
}


void HAL_UART_TxHalfCpltCallback(UART_HandleTypeDef *huart)
{
  UNUSED(huart);
}


void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
  UNUSED(huart);

}

void HAL_UART_RxHalfCpltCallback(UART_HandleTypeDef *huart)
{
}



void func_recv_data(void const * argument)
{
  for(;;)
  {
    osDelay(1);
  }
}


void func_recv_ctrl(void const * argument)
{
  for(;;)
  {
    osDelay(1);
  }
}


void func_recv_wifi(void const * argument)
{
  for(;;)
  {
    osDelay(1);
  }
}


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
