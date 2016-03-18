#ifndef MEMBLK_H
#define MEMBKL_H

#include "cmsis_os.h"
#define MEM_BLOCK_SIZE 64
#define MEM_BLOCK_NUM 32

typedef char memblk_t[MEM_BLOCK_SIZE]; 


int memblk_init(void);
void *memblk_take(void);
int memblk_free(void* p);
//see how many blocks left
//int memblk_peek(void);

#endif
