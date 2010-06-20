/************************************************************/
/* Corscience GmbH & Co KG			                        */
/* Henkestraﬂe 91, 91052 Erlangen					        */
/*----------------------------------------------------------*/
/* Project: BlueEKG             			                */
/*										                    */
/* File: compiler.h							                */
/*										                    */
/* Compilerspecific preferences                             */
/* Type definitions				                            */
/* 										                    */
/* System: gcc 4.0.0							            */
/*----------------------------------------------------------*/
/* Funktionen: keine							            */
/*----------------------------------------------------------*/
/* Heggen  | 24.05.2005  | erstellt					        */
/************************************************************/
#ifndef __COMPILER_H_
#define __COMPILER_H_

/*----------------------------------------------------------*/
/* Pr‰prozessoranweisungen						*/
/*----------------------------------------------------------*/
#pragma CODE
#pragma DEBUG

/*----------------------------------------------------------*/
/* allgemeine Definitionen						*/
/*----------------------------------------------------------*/
#define FALSE 0
#define TRUE 1
#define LOW 0
#define HIGH 1

#define MAX_LAENGE 1000
#define MAX_ARRAY 100
#define MIN_PAKET_LAENGE 33

#define TEMP_NAME "temporaere_Daten.txt"
#define DEBUG_NAME "debug_log.txt"

/*----------------------------------------------------------*/
/* Datentypendefinitionen						*/
/*----------------------------------------------------------*/
typedef unsigned int	u32		;
typedef signed int		s32		;
typedef unsigned short	u16		;
typedef signed short	s16		;
typedef unsigned char	u8		;
typedef signed char		s8		;
typedef float			f32     ;
typedef double			d64     ;


/*----------------------------------------------------------*/
/* Funktionsmakros							*/
/*----------------------------------------------------------*/
#define HI_BYTE(VAL)	(*((byte *)(&(VAL))  ))
#define LO_BYTE(VAL)	(*((byte *)(&(VAL))+1))
#define X_BYTE(X)	(*(((byte volatile *) 0x20000L+X))

#define min(A,B)	(((A)<(B))?(A):(B))
#define max(A,B)	(((A)>(B))?(A):(B))


#endif /*__UMWANDELN_H_*/
/************************************************************/
/************************************************************/
