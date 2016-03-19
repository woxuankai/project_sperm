/**
  ******************************************************************************
  * File Name          : freertos.c
  * Description        : Code for freertos applications
  ******************************************************************************
  *
  * COPYRIGHT(c) 2016 STMicroelectronics
  *
  * Redistribution and use in source and binary forms, with or without modification,
  * are permitted provided that the following conditions are met:
  *   1. Redistributions of source code must retain the above copyright notice,
  *      this list of conditions and the following disclaimer.
  *   2. Redistributions in binary form must reproduce the above copyright notice,
  *      this list of conditions and the following disclaimer in the documentation
  *      and/or other materials provided with the distribution.
  *   3. Neither the name of STMicroelectronics nor the names of its contributors
  *      may be used to endorse or promote products derived from this software
  *      without specific prior written permission.
  *
  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "FreeRTOS.h"
#include "task.h"
#include "cmsis_os.h"

/* USER CODE BEGIN Includes */     
#include "uart_driver.h"
/* USER CODE END Includes */

/* Variables -----------------------------------------------------------------*/
osThreadId defaultTaskHandle;
osThreadId recv_dataHandle;
osThreadId recv_ctrlHandle;
osThreadId recv_wifiHandle;
osThreadId handle_dataHandle;
osThreadId handle_ctrlHandle;
osThreadId handle_wifiHandle;
osThreadId send_dataHandle;
osThreadId send_ctrlHandle;
osThreadId send_wifiHandle;
osThreadId mainthreadHandle;
osMessageQId data_r_queueHandle;
osMessageQId data_t_queueHandle;
osMessageQId wifi_r_queueHandle;
osMessageQId wifi_t_queueHandle;
osMessageQId ctrl_r_queueHandle;
osMessageQId ctrl_t_queueHandle;
osMessageQId datarecv_queueHandle;
osMessageQId wifirecv_queueHandle;
osTimerId led0Handle;
osSemaphoreId data_t_cpltHandle;
osSemaphoreId wifi_t_cpltHandle;
osSemaphoreId ctrl_t_cpltHandle;

/* USER CODE BEGIN Variables */

/* USER CODE END Variables */

/* Function prototypes -------------------------------------------------------*/
void StartDefaultTask(void const * argument);
extern void func_recv_data(void const * argument);
extern void func_recv_ctrl(void const * argument);
extern void func_recv_wifi(void const * argument);
extern void func_handle_data(void const * argument);
extern void func_handle_ctrl(void const * argument);
extern void func_handle_wifi(void const * argument);
extern void func_send_data(void const * argument);
extern void func_send_ctrl(void const * argument);
extern void func_send_wifi(void const * argument);
extern void func_mainthread(void const * argument);
extern void Callback_led0(void const * argument);

void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */

/* USER CODE BEGIN FunctionPrototypes */

/* USER CODE END FunctionPrototypes */

/* Hook prototypes */

/* Init FreeRTOS */

void MX_FREERTOS_Init(void) {
  /* USER CODE BEGIN Init */
       
  /* USER CODE END Init */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* Create the semaphores(s) */
  /* definition and creation of data_t_cplt */
  osSemaphoreDef(data_t_cplt);
  data_t_cpltHandle = osSemaphoreCreate(osSemaphore(data_t_cplt), 1);

  /* definition and creation of wifi_t_cplt */
  osSemaphoreDef(wifi_t_cplt);
  wifi_t_cpltHandle = osSemaphoreCreate(osSemaphore(wifi_t_cplt), 1);

  /* definition and creation of ctrl_t_cplt */
  osSemaphoreDef(ctrl_t_cplt);
  ctrl_t_cpltHandle = osSemaphoreCreate(osSemaphore(ctrl_t_cplt), 1);

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* Create the timer(s) */
  /* definition and creation of led0 */
  osTimerDef(led0, Callback_led0);
  led0Handle = osTimerCreate(osTimer(led0), osTimerOnce, NULL);

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* Create the thread(s) */
  /* definition and creation of defaultTask */
  osThreadDef(defaultTask, StartDefaultTask, osPriorityIdle, 0, 128);
  defaultTaskHandle = osThreadCreate(osThread(defaultTask), NULL);

  /* definition and creation of recv_data */
  osThreadDef(recv_data, func_recv_data, osPriorityRealtime, 0, 128);
  recv_dataHandle = osThreadCreate(osThread(recv_data), NULL);

  /* definition and creation of recv_ctrl */
  osThreadDef(recv_ctrl, func_recv_ctrl, osPriorityRealtime, 0, 128);
  recv_ctrlHandle = osThreadCreate(osThread(recv_ctrl), NULL);

  /* definition and creation of recv_wifi */
  osThreadDef(recv_wifi, func_recv_wifi, osPriorityRealtime, 0, 128);
  recv_wifiHandle = osThreadCreate(osThread(recv_wifi), NULL);

  /* definition and creation of handle_data */
  osThreadDef(handle_data, func_handle_data, osPriorityAboveNormal, 0, 128);
  handle_dataHandle = osThreadCreate(osThread(handle_data), NULL);

  /* definition and creation of handle_ctrl */
  osThreadDef(handle_ctrl, func_handle_ctrl, osPriorityAboveNormal, 0, 128);
  handle_ctrlHandle = osThreadCreate(osThread(handle_ctrl), NULL);

  /* definition and creation of handle_wifi */
  osThreadDef(handle_wifi, func_handle_wifi, osPriorityAboveNormal, 0, 128);
  handle_wifiHandle = osThreadCreate(osThread(handle_wifi), NULL);

  /* definition and creation of send_data */
  osThreadDef(send_data, func_send_data, osPriorityHigh, 0, 128);
  send_dataHandle = osThreadCreate(osThread(send_data), NULL);

  /* definition and creation of send_ctrl */
  osThreadDef(send_ctrl, func_send_ctrl, osPriorityHigh, 0, 128);
  send_ctrlHandle = osThreadCreate(osThread(send_ctrl), NULL);

  /* definition and creation of send_wifi */
  osThreadDef(send_wifi, func_send_wifi, osPriorityHigh, 0, 128);
  send_wifiHandle = osThreadCreate(osThread(send_wifi), NULL);

  /* definition and creation of mainthread */
  osThreadDef(mainthread, func_mainthread, osPriorityNormal, 0, 128);
  mainthreadHandle = osThreadCreate(osThread(mainthread), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* Create the queue(s) */
  /* definition and creation of data_r_queue */
  osMessageQDef(data_r_queue, 4, uart_memblk_pt);
  data_r_queueHandle = osMessageCreate(osMessageQ(data_r_queue), NULL);

  /* definition and creation of data_t_queue */
  osMessageQDef(data_t_queue, 4, uart_memblk_pt);
  data_t_queueHandle = osMessageCreate(osMessageQ(data_t_queue), NULL);

  /* definition and creation of wifi_r_queue */
  osMessageQDef(wifi_r_queue, 4, uart_memblk_pt );
  wifi_r_queueHandle = osMessageCreate(osMessageQ(wifi_r_queue), NULL);

  /* definition and creation of wifi_t_queue */
  osMessageQDef(wifi_t_queue, 4, uart_memblk_pt);
  wifi_t_queueHandle = osMessageCreate(osMessageQ(wifi_t_queue), NULL);

  /* definition and creation of ctrl_r_queue */
  osMessageQDef(ctrl_r_queue, 4, uart_memblk_pt);
  ctrl_r_queueHandle = osMessageCreate(osMessageQ(ctrl_r_queue), NULL);

  /* definition and creation of ctrl_t_queue */
  osMessageQDef(ctrl_t_queue, 4, uart_memblk_pt );
  ctrl_t_queueHandle = osMessageCreate(osMessageQ(ctrl_t_queue), NULL);

  /* definition and creation of datarecv_queue */
  osMessageQDef(datarecv_queue, 256, char);
  datarecv_queueHandle = osMessageCreate(osMessageQ(datarecv_queue), NULL);

  /* definition and creation of wifirecv_queue */
  osMessageQDef(wifirecv_queue, 256, char);
  wifirecv_queueHandle = osMessageCreate(osMessageQ(wifirecv_queue), NULL);

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */
}

/* StartDefaultTask function */
void StartDefaultTask(void const * argument)
{

  /* USER CODE BEGIN StartDefaultTask */
  /* Infinite loop */
  for(;;)
  {
    osDelay(1);
  }
  /* USER CODE END StartDefaultTask */
}

/* USER CODE BEGIN Application */
     
/* USER CODE END Application */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
