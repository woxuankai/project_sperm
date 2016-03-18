#ifndef CONSOLE_H
#define CONSOLE_H

enum console_level{CONSOLE_ERROR,CONSOLE_WARNING};

//#define console_runtimereport(level,s) {__nop();}
#define console_runtimereport(level,s) {while(1);}
#endif
