/******************************************************************************/
/* Corscience GmbH & Co KG                                                    */
/* Henkestr. 91, 91054 Erlangen		                                      */
/*----------------------------------------------------------------------------*/
/* Projekt: BlueECG	                                                      */
/*                                                                            */
/* Datei:   Filterdesign.h                                                    */
/*                                                                            */
/* Aufgabe: Header file for "medianfir.c" and "mwindow.c"		      */
/*                                                                            */
/* System:  PC				                                      */
/*----------------------------------------------------------------------------*/
/* Funktionen: keine                                                          */
/*----------------------------------------------------------------------------*/
/* Er   | 13.05.05 | erstellt          LP                                     */
/******************************************************************************/


#ifndef _FILTERDESIGN_H_
#define _FILTERDESIGN_H_


/*-------------------------------------------------------------------*/

void mdefir1(int l,int iband,float fl,float fh,float fs,int iwindow,
             float b[],float w[],int ierror);

void mwindow(float w[],int n,int iwindow,int ierror);


/*-------------------------------------------------------------------*/
#endif

