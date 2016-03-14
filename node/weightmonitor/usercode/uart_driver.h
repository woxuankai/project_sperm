#ifndef UART_DRIVER_H
#define UART_DRIVER_H

//buff size setting
/////////////////////////////////////////////////////////////////////////////
#define UART_QUIERY_INTERVAL 20 //ms
//115200 bps
//(((uint32_t)(115200/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4) = 460.8
#define UARTCTRL_BUFF_SIZE 464
#define UARTCTRL_PACKAGE_T_SIZE 64
#define UARTCTRL_PACKAGE_R_SIZE 64
//9600 bps
//(((uint32_t)(9600/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4) = 38.4
#define UARTDATA_BUFF_SIZE 128
#define UARTDATA_PACKAGE_T_SIZE 32
#define UARTDATA_PACKAGE_R_SIZE 32
//115200 bps
//(((uint32_t)(115200/10*(UART_QUIERY_INTERVAL/1000.0)*2/4+0.5))*4) = 460.8
#define UARTWIFI_BUFF_SIZE  464
#define UARTWIFI_PACKAGE_T_SIZE 64
#define UARTWIFI_PACKAGE_R_SIZE 64

//uart redifine
////////////////////////////////////////////////////////////////////////////
#define UART1_BUFF_SIZE UARTCTRL_BUFF_SIZE
#define UART2_BUFF_SIZE UARTDATA_BUFF_SIZE
#define UART3_BUFF_SIZE UARTWIFI_BUFF_SIZE

#define UARTCTRL_BUFF UART1_BUFF
#define UARTDATA_BUFF UART2_BUFF
#define UARTWIFI_BUFF UART3_BUFF

//typedef
////////////////////////////////////////////////////////////////////////////
typedef  struct
{
	char null[UARTCTRL_PACKAGE_T_SIZE];
} uartctrl_package_t_t;
typedef  struct
{
	char null[UARTCTRL_PACKAGE_R_SIZE];
} uartctrl_package_r_t;
typedef  struct
{
	char null[UARTDATA_PACKAGE_T_SIZE];
} uartdata_package_t_t;
typedef  struct
{
	char null[UARTDATA_PACKAGE_R_SIZE];
} uartdata_package_r_t;
typedef  struct
{
	char null[UARTWIFI_PACKAGE_T_SIZE];
} uartwifi_package_t_t;
typedef  struct
{
	char null[UARTWIFI_PACKAGE_R_SIZE];
} uartwifi_package_r_t;


#endif 
