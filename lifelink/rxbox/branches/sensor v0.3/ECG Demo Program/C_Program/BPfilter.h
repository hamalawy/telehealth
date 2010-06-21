/******************************************************************************/
/* Corscience GmbH & Co KG                                                    */
/* Henkestr. 91, 91054 Erlangen		                                          */
/*----------------------------------------------------------------------------*/
/* Project: BlueECG	                                                          */
/*                                                                            */
/* File:   BPfilter.h                                                         */
/*                                                                            */
/* Header file for "BPfilter.c"				                                  */
/*                                                                            */
/* System:  PC				                                                  */
/*----------------------------------------------------------------------------*/
/* Pang Luping     | 13.05.05 | generated                                     */
/******************************************************************************/
#ifndef __BPFILTER_H_
#define __BPFILTER_H_

#include "compiler.h"
#include "setting.h"

/*------------------------------------------------------------------------*/
/* global functions and variables                                         */
/*------------------------------------------------------------------------*/


extern s16 oHPfilterOut, oLPfilterOut;
s16 oBPfilterFS500(s16 oData, u8 lead);
s16 oBPfilterFS100(s16 oData, u8 lead);
s16 oBPfilterFS1000(s16 oData, u8 lead);


#ifdef __BPFILTER_C_

/*----------------------------------------------------------------------------*/
/* locale functions and variables                                             */
/*----------------------------------------------------------------------------*/
    s16  init=0;
    s16  oHPfilterOut=0, oLPfilterOut=0;
    
    // Fs = 500
    s16  xhp_FS500[12][HP_BUFFER_LENGTH_FS500]={0};
    f32  fLPCoeff_FS500[LP_LENGTH_FS500]={0};  /* FIR Filter coefficients */
    f32  fLPWindow_FS500[LP_LENGTH_FS500]={0};  /* FIR Filter coefficients */   
    f32  xlp_FS500[12][LP_BUFFER_LENGTH_FS500];
    s16  nlp_FS500[12], nhp_FS500[12];
    // Fs = 100
    s16  xhp_FS100[12][HP_BUFFER_LENGTH_FS100]={0};
    f32  fLPCoeff_FS100[LP_LENGTH_FS100]={0};  /* FIR Filter coefficients */
    f32  fLPWindow_FS100[LP_LENGTH_FS100]={0};  /* FIR Filter coefficients */   
    f32  xlp_FS100[12][LP_BUFFER_LENGTH_FS100];    
    s16  nlp_FS100[12], nhp_FS100[12];
    // Fs = 1000
    s16  xhp_FS1000[12][HP_BUFFER_LENGTH_FS1000]={0};
    f32  fLPCoeff_FS1000[LP_LENGTH_FS1000]={0};  /* FIR Filter coefficients */
    f32  fLPWindow_FS1000[LP_LENGTH_FS1000]={0};  /* FIR Filter coefficients */   
    f32  xlp_FS1000[12][LP_BUFFER_LENGTH_FS1000];   
    s16  nlp_FS1000[12], nhp_FS1000[12];


#endif /*__BPFILTER_C_*/

#endif /*__BPFILTER_H_*/
