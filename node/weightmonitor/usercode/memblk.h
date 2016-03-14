#ifndef MEMBLK_H
#define MEMBKL_H

#include "cmsis_os.h"
typedef struct
{
	osMutexId mutex;
	uint8_t blk[64];
	int buff_size;
} memblk_t;

#endif