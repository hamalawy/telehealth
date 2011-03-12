/******************************************************************************/
/* Corscience GmbH & Co KG                                                    */
/* Henkestr. 91, 91054 Erlangen                                               */
/*----------------------------------------------------------------------------*/
/* Project: Blue ECG                                                                   */
/*                                                                            */
/* File:   setting.h                                                         */
/*                                                                            */
/* Globel macros and definition	                              */
/*                                                                            */
/* System:  Controller?     KEIL-C51 V3.20                                    */
/*----------------------------------------------------------------------------*/
/* Er   | 20.10.04 | erstellt           		                              */
/*      |          |                                                          */
/******************************************************************************/
#ifndef __SETTING_H_
#define __SETTING_H_




#define WRAPINC(v,w) ((v==w-1) ? 0:v+1)  /* maximal w-1 */
#define WRAPDEC(v,w) ((v==0) ? w-1:v-1)  /* minimal 0 */

#define WRAPADD(v,w,s) ((((v)+(w))>((s)-1)) ? ((v)+(w))-(s):(v)+(w)) /* maximal s-1 */
#define WRAPSUB(v,w,s) ((((v)-(w))<0) ?  (s)+((v)-(w)):(v)-(w))  /* minimal 0   */

#define SAMPLE_RATE_FS500 500
#define SAMPLE_RATE_FS100 100
#define SAMPLE_RATE_FS1000 1000


/* Parameters for high-pass filter*/
//Fs = 500
#define HP_LENGTH 500

#define HP_LENGTH_FS500 500
#define HP_BUFFER_LENGTH_FS500  HP_LENGTH*2+2
//Fs = 100
#define HP_LENGTH_FS100 100
#define HP_BUFFER_LENGTH_FS100  HP_LENGTH*2+2

//Fs = 1000
#define HP_LENGTH_FS1000 1000
#define HP_BUFFER_LENGTH_FS1000  HP_LENGTH*2+2



/* Parameters for low-pass filter */
#define FILTER_TYPE2  1    /* lowpass filter */
#define WINDOW_TYPE2  6    /* window type*/
#define FC2  25           /* cutoff frequency of highpass filter  */
//Fs = 500
#define LP_LENGTH  1500
#define LP_LENGTH_FS500  51
#define LP_BUFFER_LENGTH_FS500  (LP_LENGTH)*2
//Fs = 100
#define LP_LENGTH_FS100  11
#define LP_BUFFER_LENGTH_FS100  (LP_LENGTH)*2
//Fs = 1000
#define LP_LENGTH_FS1000  1001
#define LP_BUFFER_LENGTH_FS1000  (LP_LENGTH)*2


///* Parameters for Notch 50Hz filter */
//#define MK1 1.61803398874989
//#define MK2 0.99980001
//#define NOTCH_GAIN 0.0027
//#define NOTCH_LIM  0.5
//#define NOTCH_EPS  0.005

#define NOTCH_LENGTH_AVERAGE_FS500 500/50
#define NOTCH_LENGTH_AVERAGE_FS100 100/50
#define NOTCH_LENGTH_AVERAGE_FS1000 1000/50



#endif /* __SETTING_H_ */
