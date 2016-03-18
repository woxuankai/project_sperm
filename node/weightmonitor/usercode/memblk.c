#include "memblk.h"

#include "cmsis_os.h"

#include <stdbool.h>

osPoolDef(mempool_name, MEM_BLOCK_NUM, memblk_t);

osPoolId mempool;

bool ifmemblk_inited = false;

int memblk_init(void)
{
	mempool = osPoolCreate(osPool(mempool_name));
	if(mempool == NULL)
	  return -1;
    ifmemblk_inited = true;
	return 0;
}



void* memblk_take(void)
{
    void* p;
    if(ifmemblk_inited != true)
        return NULL;
    p = osPoolAlloc(mempool);
	return p;
}
int memblk_free(void* p)
{
    int32_t status;
    if(ifmemblk_inited != true)
        return NULL;
    status = osPoolFree(mempool, p);
    if(status == osOK )
        return 0;
    else
        return -1;
}
