#include "buffpool.h"

#include "FreeRTOS.h"
#include "task.h"
#include "mxconstants.h"
#include "cmsis_os.h"

#include <stdbool.h>

#define BUFF_256_NUM 5
//#define BUFF_128_NUM 10
//#define BUFF_64_NUM 20



bool if_init = false;

buffblock_t  buff_pool[BUFF_256_NUM];

uint8_t memoryblock256[BUFF_256_NUM][256];

osMutexDef(mempoolpublicmutex);

int32_t init_buffpool(void)
{
	int buff256cnt;
	for (buff256cnt = 0; buff256cnt < BUFF_256_NUM ; buff256cnt++)
	{
		buff_pool[buff256cnt].p = memoryblock256[buff256cnt];
		buff_pool[buff256cnt].mutex = osMutexCreate(osMutex(mempoolpublicmutex));
		if( buff_pool[buff256cnt].mutex == NULL)
			return -1;
	}
	if_init = true;
	return 0;
 }

p_buffblock_t take_buff(uint32_t waittime)
{
	int buff256cnt;
	if( if_init == false )
		return NULL;
	for (buff256cnt = 0; buff256cnt < BUFF_256_NUM ; buff256cnt++)
	{
		if(xSemaphoreTake( buff_pool[buff256cnt].mutex, 0 ) == pdTRUE)
				return buff_pool + buff256cnt;
	}
	return NULL;
}

int32_t give_buff(p_buffblock_t p)
{
	if ( xSemaphoreGive(p->mutex) != pdTRUE)
		return -1;
	return 0;
}
