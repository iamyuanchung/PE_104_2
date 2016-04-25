#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define EMPTY -6.89

typedef struct{
    double comeIn;
    double startServ;
    double endServ;
}customer;

typedef struct{
    customer *cust;
}server;

typedef struct{
    int custNum;
    double total_wait;
    double total_sys;
    double both_idle;
    double both_busy;
}output;

