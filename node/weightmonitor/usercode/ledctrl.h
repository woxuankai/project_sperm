#ifndef LEDCTRL_H
#define LEDCTRL_H

#include <stdint.h>

enum leddevices
{
    devLED0,
};


int32_t ledflash(int dev, int time);


#define LED_GPIO_ON GPIO_PIN_RESET
#define LED_GPIO_OFF GPIO_PIN_SET

#define LED_ON(devLED) HAL_GPIO_WritePin(devLED##_GPIO_Port,devLED##_Pin,LED_GPIO_ON)
#define LED_OFF(devLED) HAL_GPIO_WritePin(devLED##_GPIO_Port,devLED##_Pin,LED_GPIO_OFF)
#define LED_TOGGLE(devLED) HAL_GPIO_TogglePin(devLED##_GPIO_Port,devLED##_Pin)

#endif
