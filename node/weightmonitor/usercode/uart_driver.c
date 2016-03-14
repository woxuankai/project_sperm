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


uartctrl_package_t_t ctrl_t_buff;
uartctrl_package_r_t ctrl_r_buff;
uartdata_package_t_t data_t_buff;
uartdata_package_r_t data_r_buff;
uartwifi_package_t_t wifi_t_buff;
uartwifi_package_r_t wifi_r_buff;

char UART1_BUFF[UART1_BUFF_SIZE] = {0};
char UART2_BUFF[UART2_BUFF_SIZE] = {0};
char UART3_BUFF[UART3_BUFF_SIZE] = {0};


//reset prepare to receive new message
int uart_start(UART_HandleTypeDef *huart);

//clean buffer and ignore any message
int uart_stop(UART_HandleTypeDef *huart);

//clean buffer and prepare to receive new message
//int uart_reset(UART_HandleTypeDef *huart);

//receive a message
//in block mode
//if pack is null, then will use the default buff
int uart_receive(char *uartname, void* pack);

//transmit a message
//in block mode
//if pack is null, then will use the default buff
int uart_transmit(char *uartname, void* pack);

 
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
//void HAL_UART_TxHalfCpltCallback(UART_HandleTypeDef *huart)
//{
//  UNUSED(huart);
//}
//void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
//{
//  UNUSED(huart);
//}
//void HAL_UART_RxHalfCpltCallback(UART_HandleTypeDef *huart)
//{
//	UNUSED(huart);
//}