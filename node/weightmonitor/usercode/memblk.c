#include "memblk.h"

#include "cmsis_os.h"

osPoolDef(mempool_name, MEM_BLOCK_NUM, memblk_t);

osPoolId mempool;


int memblk_init(void)
{
	mempool = osPoolCreate(osPool(mempool_name));
	if(mempool == NULL)
	  return -1;
	return 0;
}



void* memblk_take(void)
{
	return NULL;
}
int memblk_free(void* p)
{
	return 0;
}
