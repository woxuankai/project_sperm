#ifndef CONSOLE_H
#define CONSOLE_H

#define __INT2STR(I) #I
#define INT2STR(I) __INT2STR(I)

typedef enum 
{
    CONSOLE_MESSAGE,
    CONSOLE_ERROR,
    CONSOLE_WARNING
} CONSOLE_LEVEL;

int console_problemhandle(CONSOLE_LEVEL level, char * file, char* line, char* msg);

//#define console_runtimereport(level,msg) \
            {\
                console_send(msg#__LINE__);\
            }

#define console_runtimereport(LEVEL,MSG) \
            {\
                console_problemhandle(LEVEL,__FILE__,INT2STR(__LINE__), MSG);\
            }
            
#endif
