#ifndef WIFICTRL_H
#define WIFICTRL_H

#include <stdint.h>
#include "stm32f1xx_hal.h"

#define WIFI_ON  HAL_GPIO_WritePin(Wifi_En_GPIO_Port, Wifi_En_Pin, GPIO_PIN_SET)

#define WIFI_OFF HAL_GPIO_WritePin(Wifi_En_GPIO_Port, Wifi_En_Pin, GPIO_PIN_RESET)

#endif

