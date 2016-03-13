#ifndef LEDCTRL_H
#define LEDCTRL_H

#include <stdint.h>
/*

enum LEDCMD
{
//	LEDCMD_QUERYPERIOD,
	LEDCMD_QUERYDUTY,
//	LEDCMD_SETPERIOD,
	LEDCMD_SETDUTY,
};

extern int32_t ledctl(int32_t dev, uint32_t cmd, int32_t arg);



*/

int32_t led0changeperiod(int period);
int32_t	led0start(void);
int32_t led0stop(void);




#endif
