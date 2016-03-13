#ifndef BUFFPOOL_H
#define BUFFPOOL_H

#include "FreeRTOS.h"
#include "task.h"
#include "mxconstants.h"
#include "cmsis_os.h"
#include <stdint.h>

typedef 
struct
{
	osMutexId mutex;
	uint8_t* p_buff_block;
	int buff_size;
} 
buff_block_t;

typedef buff_block_t* p_buff_block_t;


int32_t init_buffpool(void);
p_buff_block_t claim_buff(int size);
int32_t free_buff(p_buff_block_t p);


#endif
