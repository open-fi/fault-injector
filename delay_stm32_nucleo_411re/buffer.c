#include <libopencm3/stm32/usart.h>
#include <libopencm3/stm32/f4/nvic.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "buffer.h"

//configure the frequencies inside the test system
#define FREQUENCY_STOPCLOCK	84e6
#define FREQUENCY_TARGET	2e6

//approach command code followed by payload
//like  | 0x0A | DELAY |

//global rxBuffer for Uart
buffer rxBuffer;

void resetBuffer(buffer* input){
	for(uint8_t i=0;i<RXBUFFERLEN;i++){
		input->text[i]=0;
	}
	input->len=0;
}

void copyBuffer(buffer* from, buffer* to){
	for(uint8_t i=0;i<RXBUFFERLEN;i++){
			to->text[i]=from->text[i];
		}
	to->len=from->len;
}

void copyBufferWithoutPrefix(buffer* from, buffer* to){

	for(uint8_t i=0;i<from->len-2;i++){
			to->text[i]=from->text[i+2];
		}
	to->len=from->len-2;

}

void sendByte(uint8_t input){
	usart_send_blocking(USART2, (char)input);

}

void sendBuffer(buffer input){
	for(uint8_t i=0; i<input.len;i++){
		sendByte(input.text[i]);
	}
}

uint8_t checkPacketComplete(buffer input){
	if((input.text[1]==input.len-2) && input.len>2){
		return 1;
	}
	else{
		return 0;
	}
}

uint8_t getTaskFromBuffer(buffer input){

	//get first byte from buffer and switch case
	return input.text[0];
}

void usart2_isr(void){
	rxBuffer.text[rxBuffer.len++] = usart_recv(USART2);
}
