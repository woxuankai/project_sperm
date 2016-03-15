//data path:
//TX:
//transmit =queue=> threadtx =dma= TX
//TX =intterrupt--semphore=> threadtx
//RX:
//threadrx =quiery-queue=> recv

#include <stdint.h>
#include "uart_driver.h"
#include "usart.h"
#include "stm32f1xx_hal.h"
#include "cmsis_os.h"

char UART1_BUFF[UART1_BUFF_SIZE] = {0};
char UART2_BUFF[UART2_BUFF_SIZE] = {0};
char UART3_BUFF[UART3_BUFF_SIZE] = {0};


//receive a message
uart_memblk_pt uart_receive(char *uartname, uint32_t time);

//transmit a message
int uart_transmit(char *uartname, uart_memblk_pt pack, uint32_t time);

 
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

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
  UNUSED(huart);
}
