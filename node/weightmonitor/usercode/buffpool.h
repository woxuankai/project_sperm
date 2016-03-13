#ifndef BUFFPOOL_H
#define BUFFPOOL_H

#include "FreeRTOS.h"
#include "task.h"
#include "mxconstants.h"
#include "cmsis_os.h"
#include <stdint.h>

typedef struct 
{
	uint8_t* p;
	osMutexId mutex;
	int buff_size;
} buffblock_t;

typedef buffblock_t* p_buffblock_t;




int32_t init_buffpool(void);
int get_buff_size(p_buffblock_t p);
p_buffblock_t claim_buff(int size);
int32_t free_buff(p_buffblock_t p);


#endif
