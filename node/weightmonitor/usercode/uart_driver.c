#include "uart_driver.h"
#include "usart.h"

#include "stm32f1xx_hal.h"

#include "buffpool.h"



#include <stdint.h>
#define UART_QUIERY_INTERVAL 20 //ms
//115200 bps
#define UART1_BUFF_SIZE (((uint32_t)(115200/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4)
//9600 bps
#define UART2_BUFF_SIZE (((uint32_t)(9600/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4)
//115200 bps
#define UART3_BUFF_SIZE (((uint32_t)(115200/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4)

#define UARTCTRL_BUFF_SIZE UART1_BUFF_SIZE
#define UARTDATA_BUFF_SIZE UART2_BUFF_SIZE
#define UARTWIFI_BUFF_SIZE UART3_BUFF_SIZE

char UART1_BUFF[UART1_BUFF_SIZE] = {0};
char UART2_BUFF[UART2_BUFF_SIZE] = {0};
char UART3_BUFF[UART3_BUFF_SIZE] = {0};

#define UARTCTRL_BUFF UART1_BUFF
#define UARTDATA_BUFF UART2_BUFF
#define UARTWIFI_BUFF UART3_BUFF

//reset prepare to receive new message
int uart_start(UART_HandleTypeDef *huart);

//clean buffer and ignore any message
int uart_stop(UART_HandleTypeDef *huart);

//clean buffer and prepare to receive new message
int uart_reset(UART_HandleTypeDef *huart);

//receive a message
//in block mode
int uart_receive(UART_HandleTypeDef *huart, p_buffblock_t);

//transmit a message
//in block mode if uart device is busy
int uart_transmit(UART_HandleTypeDef *huart,p_buffblock_t);


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

#include "FreeRTOS.h"
#include "task.h"
#include "timers.h"
#include "queue.h"
#include "semphr.h"
#include "event_groups.h"



typedef struct QueueDefinition
{
	int8_t *pcHead;					/*< Points to the beginning of the queue storage area. */
	int8_t *pcTail;					/*< Points to the byte at the end of the queue storage area.  Once more byte is allocated than necessary to store the queue items, this is used as a marker. */
	int8_t *pcWriteTo;				/*< Points to the free next place in the storage area. */

	union							/* Use of a union is an exception to the coding standard to ensure two mutually exclusive structure members don't appear simultaneously (wasting RAM). */
	{
		int8_t *pcReadFrom;			/*< Points to the last place that a queued item was read from when the structure is used as a queue. */
		UBaseType_t uxRecursiveCallCount;/*< Maintains a count of the number of times a recursive mutex has been recursively 'taken' when the structure is used as a mutex. */
	} u;

	List_t xTasksWaitingToSend;		/*< List of tasks that are blocked waiting to post onto this queue.  Stored in priority order. */
	List_t xTasksWaitingToReceive;	/*< List of tasks that are blocked waiting to read from this queue.  Stored in priority order. */

	volatile UBaseType_t uxMessagesWaiting;/*< The number of items currently in the queue. */
	UBaseType_t uxLength;			/*< The length of the queue defined as the number of items it will hold, not the number of bytes. */
	UBaseType_t uxItemSize;			/*< The size of each items that the queue will hold. */

	volatile BaseType_t xRxLock;	/*< Stores the number of items received from the queue (removed from the queue) while the queue was locked.  Set to queueUNLOCKED when the queue is not locked. */
	volatile BaseType_t xTxLock;	/*< Stores the number of items transmitted to the queue (added to the queue) while the queue was locked.  Set to queueUNLOCKED when the queue is not locked. */

	#if ( configUSE_TRACE_FACILITY == 1 )
		UBaseType_t uxQueueNumber;
		uint8_t ucQueueType;
	#endif

	#if ( configUSE_QUEUE_SETS == 1 )
		struct QueueDefinition *pxQueueSetContainer;
	#endif

} xQUEUE;


void func_recv_wifi(void const * argument)
{
  uint32_t temp;
	for(;;)
  {
		temp = sizeof( Queue_t );
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
