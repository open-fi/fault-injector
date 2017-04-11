#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>
#include <libopencm3/stm32/f4/nvic.h>
#include <libopencm3/stm32/exti.h>
#include <libopencm3/cm3/scs.h>
#include <libopencm3/cm3/dwt.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "buffer.h"

//GPIO PA0 A0 input exti
//GPIO PA1 A1 output trigger
//GPIO PA4 A2 output reset dut

//configure the frequencies inside the test system
#define FREQUENCY_STOPCLOCK	84e6
#define FREQUENCY_TARGET	2e6
volatile uint16_t delay = 0;

int main(void){

	clock_scale_t clkcfg_84mhz = {
		.pllm = 8,
		.plln = 336,
		.pllp = 4,
		.pllq = 4,
		.flash_config = (1<<9) | (1<<10) | 0x03,
		.hpre = 1,
		.ppre1 = 2,
		.ppre2 = 1,
		.power_save = 1,
		//apb1 should be 42e6 there is a bug in the lib uart2 is clocked by apb2 not apb1 !!!!!
		//.apb1_frequency = 42e6,
		.apb1_frequency = 84e6,
		.apb2_frequency = 84e6
	};
	
	rcc_osc_bypass_enable(HSE);
	rcc_clock_setup_hse_3v3(&clkcfg_84mhz);
	rcc_periph_clock_enable(RCC_GPIOA);
	rcc_periph_clock_enable(RCC_USART2);
	
	gpio_mode_setup(GPIOA, GPIO_MODE_INPUT , GPIO_PUPD_PULLDOWN, GPIO0);
	gpio_mode_setup(GPIOA, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLDOWN, GPIO1);
	gpio_mode_setup(GPIOA, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLDOWN, GPIO4);
	gpio_mode_setup(GPIOA, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE	, GPIO5);
	gpio_mode_setup(GPIOA, GPIO_MODE_AF	, GPIO_PUPD_NONE	, GPIO2);
	gpio_mode_setup(GPIOA, GPIO_MODE_AF	, GPIO_PUPD_NONE	, GPIO3);
	gpio_set_af(GPIOA, GPIO_AF7, GPIO2);
	gpio_set_af(GPIOA, GPIO_AF7, GPIO3);
	
	gpio_set_output_options(GPIOA,GPIO_PUPD_PULLDOWN,GPIO_OSPEED_100MHZ,GPIO1);
	
	nvic_enable_irq(NVIC_EXTI0_IRQ);
	exti_select_source(NVIC_EXTI0_IRQ,GPIOA);
	exti_set_trigger(EXTI0,EXTI_TRIGGER_RISING);
	exti_enable_request(EXTI0);
	
	usart_set_baudrate(USART2, 115200);
	usart_set_databits(USART2, 8);
	usart_set_stopbits(USART2, USART_STOPBITS_1);
	usart_set_mode(USART2, USART_MODE_TX_RX);
	usart_set_parity(USART2, USART_PARITY_NONE);
	usart_set_flow_control(USART2, USART_FLOWCONTROL_NONE);
	nvic_enable_irq(NVIC_USART2_IRQ);
	usart_enable_rx_interrupt(USART2);
	usart_enable(USART2);
	
	dwt_enable_cycle_counter();
	resetBuffer(&rxBuffer);
	
	//infinite loop
	for(;;){
		if(checkPacketComplete(rxBuffer)){
			switch(getTaskFromBuffer(rxBuffer)){
				case COMMAND_SEND_DELAY :
					delay = rxBuffer.text[2] << 8 | rxBuffer.text[3];
					sendBuffer(rxBuffer);
					resetBuffer(&rxBuffer);
					break;
				case COMMAND_SEND_TRIGGER :
					GPIO_BSRR(GPIOA) = GPIO1;
					gpio_set(GPIOA, GPIO5);
					for (volatile uint32_t loop = 0; loop < 1e3; loop++);
					gpio_clear(GPIOA, GPIO1);
					gpio_clear(GPIOA, GPIO5);
					sendBuffer(rxBuffer);
					resetBuffer(&rxBuffer);
					break;
				case COMMAND_SEND_RESET :
					gpio_set(GPIOA, GPIO4);
					for (volatile uint32_t loop = 0; loop < 10e3; loop++);
					gpio_clear(GPIOA, GPIO4);
					sendBuffer(rxBuffer);
					resetBuffer(&rxBuffer);
					break;
				default:
					break;
			}
		}
	}
	return 0;
}

void exti0_isr(void){
	DWT_CYCCNT = 0;
	while(DWT_CYCCNT <= delay);
	GPIO_BSRR(GPIOA) = GPIO1;
	gpio_set(GPIOA, GPIO5);
	for (volatile uint32_t loop = 0; loop < 100e3; loop++);
	gpio_clear(GPIOA, GPIO1);
	gpio_clear(GPIOA, GPIO5);
	exti_reset_request(EXTI0);

}
