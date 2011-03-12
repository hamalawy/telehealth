//http://www.daniweb.com/forums/thread278258.html

#include "SDL.h"
#include "SDL_gfxPrimitives.h"
#include "SDL_image.h"
#include "BPfilter.h"

int WINDOW_WIDTH = 1120;
int WINDOW_HEIGHT = 380;
int XOFFSET = 16;
char BMPIMAGE[50];
const char* WINDOW_TITLE = "SDL Start";
int cont = 1;
int filter = 1;
int CENTER = WINDOW_HEIGHT/2;
int ScaleNum = 1;
int ScaleDen = 1;
int ScalePlot = 1;
int main(int argc, char **argv)
{
   scanf("%d,%d,%d,%d,%d,%d,%d,%d,%d,%s",&WINDOW_WIDTH,&WINDOW_HEIGHT,&XOFFSET,&CENTER,&cont,&filter,&ScaleNum,&ScaleDen,&ScalePlot,BMPIMAGE);
   
   SDL_Init( SDL_INIT_VIDEO );

   SDL_Surface* screen = SDL_SetVideoMode(WINDOW_WIDTH, WINDOW_HEIGHT, 0, SDL_HWSURFACE | SDL_DOUBLEBUF );
   SDL_WM_SetCaption( WINDOW_TITLE, 0 );

   SDL_Surface *grid;
   SDL_Rect gridLocation;
   grid = IMG_Load(BMPIMAGE);
   gridLocation.x=0;
   gridLocation.y=0;

   SDL_Event event;
   bool gameRunning = true;

   int t=0,x1=0, y1=0, x2=0, y2=0, x=0, y=0;
   float tScale = 0.00263*ScaleNum/ScaleDen*ScalePlot/15*CENTER;
   SDL_FillRect(screen, NULL, SDL_MapRGB(screen->format, 0, 0, 0));
   SDL_BlitSurface(grid, NULL, screen, &gridLocation);
   
   scanf("%d,%d",&x,&y);
   if(x==WINDOW_WIDTH) return 0;
   if(filter) y = CENTER-oBPfilterFS500(y, 2)*tScale;
   else y = CENTER-y*tScale;
   x2=x;
   y2=y;
   printf("Plotter Start\n");
      
   while (gameRunning)
   {
      if (SDL_PollEvent(&event))
      {
         if (event.type == SDL_QUIT)
         {
            gameRunning = false;
         }
      }
      
      scanf("%d,%d",&x,&y);
      if(x>=WINDOW_WIDTH) break;
      if(filter) y = CENTER-oBPfilterFS500(y, 2)*tScale;
      else y = CENTER-y*tScale;

      if(x<=XOFFSET || x2 > x){
    	 SDL_FillRect(screen, NULL, SDL_MapRGB(screen->format, 0, 0, 0));
    	 SDL_BlitSurface(grid, NULL, screen, &gridLocation);
    	 x1 = XOFFSET;
    	 y1 = WINDOW_HEIGHT/2;
    	 x2 = XOFFSET;
    	 y2 = WINDOW_HEIGHT/2;
      }

      t++;
      x1=x2;
      y1=y2;
      x2=x;
      y2=y;
      lineRGBA(screen, x1, y1+1, x2, y2+1, 255, 0, 0, 255);
      lineRGBA(screen, x1, y1, x2, y2, 255, 0, 0, 255);

      if(cont && x1%10==0) SDL_Flip(screen);
//      SDL_Delay(0.01);
   }
   if(!cont) {
      SDL_Delay(2500);
      SDL_Flip(screen);
   }
   SDL_Quit();
   printf("Plotter Stop\n");
   return 0;
}
