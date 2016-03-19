#ifndef MAINTHREAD_H
#define MAINTHREAD_H


#include "cmsis_os.h"
//notice :
//in case of \r\n, insert \r only, abort \n
extern osMessageQId datarecv_queueHandle;
extern osMessageQId wifirecv_queueHandle;

#endif
