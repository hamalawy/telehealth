
/******************************************************************************/
/* Corscience GmbH & Co KG                                                    */
/* Henkestr. 91, 91054 Erlangen                                               */
/*----------------------------------------------------------------------------*/
/* Project: BlueECG                                              		      */
/*                                                                            */
/* File:   BPfilter.c                                                         */                                                        
/*                                                                            */
/* System:  PC                                              			      */
/*----------------------------------------------------------------------------*/
/* Functions:                                                                 */
/* s16 oBPfilter(s16 oData, u8 lead)                      		      	      */
/*----------------------------------------------------------------------------*/
/*Use Function to filter frequencies outside 0.12Hz and 25Hz                  */ 
/*                                                                            */
/*Input:  signed short oData -> Datastream from ECG                           */
/*        char lead          -> Number of the active ECG lead                 */
/*                              3/6 Channel ECG - max 6 leads                 */
/*                                                                            */
/*                              12 Channel ECG - max 12 leads                 */
/*                                                                            */
/*                                                                            */
/*                                                                            */
/*                                                                            */
/*Output: Function returns signed short value of filtered data                */
/*----------------------------------------------------------------------------*/
/*Pang Luping   | 13.05.05 |                	                              */
/*Felix Kupsch  | 13.10.05 |                                                  */
/******************************************************************************/


#ifndef __BPFILTER_C_
#define __BPFILTER_C_

#include "BPfilter.h"
#include "Filterdesign.h"
#include "compiler.h"
#include "setting.h"



//Bandpass Filter: Sampling rate 500Hz
s16 oBPfilterFS500(s16 oData, u8 lead)
{
    s16	 i;        
    s16  error=0;
    f32  ylp=0;
    u16  FH=(SAMPLE_RATE_FS500/2-1);
    
    s32  static y1[12];
    s32  y0=0;
    
    
    /*--- Calculation of the lowpass filter coefficients on the first sample(init==0).
          These filter coefficients are stored in  fLPCoeff[].
          then filters are performed on the following signal (init!=0) -----*/
    
    if (init==0)
    {
       	// Fs = 500 Hz
    	mdefir1(LP_LENGTH_FS500,FILTER_TYPE2,FC2,FH,SAMPLE_RATE_FS500,WINDOW_TYPE2, fLPCoeff_FS500, fLPWindow_FS500, error);
    	for(i=0; i<8; i++)
           nhp_FS500[i]=HP_LENGTH_FS500;
        for(i=0; i<8; i++)
           nlp_FS500[i]=LP_LENGTH_FS500-1;
        init=1;
    }
    else
    {
    	// Fs = 500 Hz
      	xhp_FS500[lead][nhp_FS500[lead]]= xhp_FS500[lead][nhp_FS500[lead] + HP_LENGTH_FS500 + 1] = oData;
       	y0 = y1[lead] + xhp_FS500[lead][nhp_FS500[lead]] - xhp_FS500[lead][nhp_FS500[lead] + HP_LENGTH_FS500];
       	y1[lead] = y0;
       	oHPfilterOut=xhp_FS500[lead][nhp_FS500[lead]] - (y0 /HP_LENGTH_FS500);
   	
       	if (--nhp_FS500[lead] < 0) nhp_FS500[lead] = HP_LENGTH_FS500;
   	
    	xlp_FS500[lead][nlp_FS500[lead]]=oHPfilterOut;
    	xlp_FS500[lead][nlp_FS500[lead] + LP_LENGTH_FS500]=oHPfilterOut;
    	for(i=0;i<LP_LENGTH_FS500;i++)
    	{
    		ylp=xlp_FS500[lead][nlp_FS500[lead]+i]*fLPCoeff_FS500[i]+ylp;
    	}
    	if (--nlp_FS500[lead] < 0) nlp_FS500[lead]=LP_LENGTH_FS500-1;
    	oLPfilterOut=(s16)ylp;    	
    }
   /*------------------------------------------------------------------------#*/
   return(oLPfilterOut);
}


//Bandpass Filter: Sampling rate 100Hz
s16 oBPfilterFS100(s16 oData, u8 lead)
{
    s16	 i;        
    s16  error=0;
    f32  ylp=0;
    u16  FH=(SAMPLE_RATE_FS100/2-1);
    
    s32  static y1[12];
    s32  y0=0;
    
    
    /*--- Calculation of the lowpass filter coefficients on the first sample(init==0).
          These filter coefficients are stored in  fLPCoeff[].
          then filters are performed on the following signal (init!=0) -----*/
    
    if (init==0)
    {
   	// Fs = 100 Hz
    	mdefir1(LP_LENGTH_FS100,FILTER_TYPE2,FC2,FH,SAMPLE_RATE_FS100,WINDOW_TYPE2, fLPCoeff_FS100, fLPWindow_FS100, error);
    	
    	for(i=0; i<8; i++)
           nhp_FS100[i]=HP_LENGTH_FS100;
           
        for(i=0; i<8; i++)
           nlp_FS100[i]=LP_LENGTH_FS100-1;
        init=1;
        
    }
    else
    {

	    // Fs = 100 Hz
      	xhp_FS100[lead][nhp_FS100[lead]]= xhp_FS100[lead][nhp_FS100[lead] + HP_LENGTH_FS100 + 1] = oData;
       	y0 = y1[lead] + xhp_FS100[lead][nhp_FS100[lead]] - xhp_FS100[lead][nhp_FS100[lead] + HP_LENGTH_FS100];
       	y1[lead] = y0;
       	oHPfilterOut=xhp_FS100[lead][nhp_FS100[lead]] - (y0 /HP_LENGTH_FS100);
   	
       	if (--nhp_FS100[lead] < 0) nhp_FS100[lead] = HP_LENGTH_FS100;
   	     	
   	
    	xlp_FS100[lead][nlp_FS100[lead]]=oHPfilterOut;
    	xlp_FS100[lead][nlp_FS100[lead] + LP_LENGTH_FS100]=oHPfilterOut;
    	for(i=0;i<LP_LENGTH_FS100;i++)
    	{
    		ylp=xlp_FS100[lead][nlp_FS100[lead]+i]*fLPCoeff_FS100[i]+ylp;
    	}
    	if (--nlp_FS100[lead] < 0) nlp_FS100[lead]=LP_LENGTH_FS100-1;
    	oLPfilterOut=(s16)ylp;    	
    }
   /*------------------------------------------------------------------------#*/
   return(oLPfilterOut);
}


//Bandpass Filter: Sampling rate 1000Hz
s16 oBPfilterFS1000(s16 oData, u8 lead)
{
    s16	 i;        
    s16  error=0;
    f32  ylp=0;
    u16  FH=(SAMPLE_RATE_FS1000/2-1);
    
    s32  static y1[12];
    s32  y0=0;
    
    
    /*--- Calculation of the lowpass filter coefficients on the first sample(init==0).
          These filter coefficients are stored in  fLPCoeff[].
          then filters are performed on the following signal (init!=0) -----*/
    
    if (init==0)
    {
   	// Fs = 1000 Hz
    	mdefir1(LP_LENGTH_FS1000,FILTER_TYPE2,FC2,FH,SAMPLE_RATE_FS1000,WINDOW_TYPE2, fLPCoeff_FS1000, fLPWindow_FS1000, error);
    	
    	for(i=0; i<8; i++)
           nhp_FS1000[i]=HP_LENGTH_FS1000;
           
        for(i=0; i<8; i++)
           nlp_FS1000[i]=LP_LENGTH_FS1000-1;
           
       
        
        
        
        
        init=1;
        
    }
    else
    {

	// Fs = 1000 Hz
  	xhp_FS1000[lead][nhp_FS1000[lead]]= xhp_FS1000[lead][nhp_FS1000[lead] + HP_LENGTH_FS1000 + 1] = oData;
   	y0 = y1[lead] + xhp_FS1000[lead][nhp_FS1000[lead]] - xhp_FS1000[lead][nhp_FS1000[lead] + HP_LENGTH_FS1000];
   	y1[lead] = y0;
   	oHPfilterOut=xhp_FS1000[lead][nhp_FS1000[lead]] - (y0 /HP_LENGTH_FS1000);
   	
   	if (--nhp_FS1000[lead] < 0)
   	 nhp_FS1000[lead] = HP_LENGTH_FS1000;
   	     	
   	
    	xlp_FS1000[lead][nlp_FS1000[lead]]=oHPfilterOut;
    	xlp_FS1000[lead][nlp_FS1000[lead] + LP_LENGTH_FS1000]=oHPfilterOut;
    	for(i=0;i<LP_LENGTH_FS1000;i++)
    	{
    		ylp=xlp_FS1000[lead][nlp_FS1000[lead]+i]*fLPCoeff_FS1000[i]+ylp;
    		
    	}
    	if (--nlp_FS1000[lead] < 0) nlp_FS1000[lead]=LP_LENGTH_FS1000-1;
    	oLPfilterOut=(s16)ylp;    	
    	
 
 
    	
    	
    	
    	
    }
   /*------------------------------------------------------------------------#*/




   return(oLPfilterOut);
   
}
#endif
