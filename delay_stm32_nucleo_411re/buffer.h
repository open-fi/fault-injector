/*
 * uart.h
 *
 *  Created on: 23.05.2015
 */

#ifndef BUFFER_H_
#define BUFFER_H_

#include <stdint.h>

#define RXBUFFERLEN 128
#define COMMAND_SEND_DELAY		0xAA
#define COMMAND_SEND_TRIGGER		0xBB
#define COMMAND_SEND_RESET		0xCC

//buffer data structure containing length informations
typedef struct buffer {
	volatile uint8_t text[RXBUFFERLEN];
	volatile uint8_t len;
} buffer;

extern buffer rxBuffer;

void resetBuffer(buffer *input);
void copyBuffer(buffer *from, buffer *to);
void copyBufferWithoutPrefix(buffer *from, buffer *to);
void sendByte(uint8_t input);
void sendBuffer(buffer input);
uint8_t checkPacketComplete(buffer input);
uint8_t getTaskFromBuffer(buffer input);



#endif /* UART_H_ */
