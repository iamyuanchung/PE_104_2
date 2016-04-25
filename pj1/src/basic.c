/* =================================== */
/* basic: Two servers and single queue */
/* =================================== */

#include "utils.h"

server S[2];
customer *queue[10000];
int qs, qe;

double get_exp(double lambda){
    int randNum = (rand() % 10000) + 1;
    double x = ((double)randNum) / 10000;
    return ((log(x) * -1)/lambda);
}

int cust_waiting(){
    if(qe >= qs)
        return qe - qs;
    return (qe + 10000 - qs);
}

void push(customer *c){
    if((qe == qs) && (queue[qs] != NULL)){
        fprintf(stderr, "queue full, stop\n");
        exit(0);
    }
    queue[qe] = c;
    qe += 1;
    if(qe == 10000)
        qe = 0;
    return;
}

customer* pop(){
    if(qs == qe){
        fprintf(stderr, "pop from empty queue, stop\n");
        exit(0);
    }
    customer *x;
    if(queue[qs] == NULL)
        fprintf(stderr, "queue[qs] == NULL\n");
    x = queue[qs];
    queue[qs] = NULL;
    qs += 1;
    if(qs == 10000)
        qs = 0;
    return x;
}

void create_customer(double ArrRate){
    static double last_arrival = 0.00;
    customer *newC;
    newC = (customer*)malloc(sizeof(customer));
    newC -> comeIn = last_arrival + get_exp(ArrRate);
    newC -> startServ = EMPTY;
    newC->endServ = EMPTY;
    push(newC);
    last_arrival = newC -> comeIn;
    return;
}

int main(int argc, char* argv[]){
    if(argc < 4){
        fprintf(stderr, "argument not enough:\n ArrivalRate ServiceRate SimTime\n");
        exit(-1);
    }
    double ArrRate = atof(argv[1]);
    double SerRate = atof(argv[2]);
    int SimTime = atoi(argv[3]);
    fprintf(stderr, "%f %f %d\n", ArrRate, SerRate, SimTime);

    // set up the initial condition
    srand(time(NULL));
    S[0].cust = NULL;
    S[1].cust = NULL;
    qs = 0;
    qe = 0;
    double timeNow = 0.00;
    int nS;
    customer* nextC = NULL;
    output OP;
    OP.custNum = 0;
    OP.total_wait = 0.00;
    OP.total_sys = 0.00;
    OP.both_idle = 0.00;
    OP.both_busy = 0.00;

    // start running the simulation
    while(1){
        if(cust_waiting() == 0){
            create_customer(ArrRate);
            continue;
        }
        else if(S[0].cust == NULL){
            OP.custNum += 1;
            S[0].cust = pop();
            S[0].cust -> startServ = S[0].cust -> comeIn;
            S[0].cust -> endServ = S[0].cust -> comeIn + get_exp(SerRate);
            OP.total_sys += S[0].cust -> endServ - S[0].cust -> startServ;
            create_customer(ArrRate);
            continue;
        }
        else if(S[1].cust == NULL){
            OP.custNum += 1;
            S[1].cust = pop();
            S[1].cust -> startServ = S[1].cust -> comeIn;
            S[1].cust -> endServ = S[1].cust -> comeIn + get_exp(SerRate);
            OP.total_sys += S[1].cust -> endServ - S[1].cust -> startServ;
            create_customer(ArrRate);
            continue;
        }

        timeNow = S[0].cust -> endServ;
        nS = 0;
        if(S[0].cust -> endServ > S[1].cust -> endServ){
            timeNow = S[1].cust -> endServ;
            nS = 1;
        }

        if(timeNow > SimTime)
            break;

        if(nS == 0){
            if(S[0].cust -> startServ > S[1].cust -> startServ)
                OP.both_busy += S[0].cust -> endServ - S[0].cust -> startServ;
            else
                if((S[0].cust -> endServ - S[1].cust -> startServ) > 0)
                    OP.both_busy += S[0].cust -> endServ - S[1].cust -> startServ;
        }
        else if(nS == 1){
            if(S[1].cust -> startServ > S[0].cust -> startServ)
                OP.both_busy += S[1].cust -> endServ - S[1].cust -> startServ;
            else
                if((S[1].cust -> endServ - S[0].cust -> startServ) > 0)
                    OP.both_busy += S[1].cust -> endServ - S[0].cust -> startServ;
        }
        nextC = pop();
        if(timeNow > nextC -> comeIn){
            OP.custNum += 1;
            free(S[nS].cust);
            S[nS].cust = nextC;
            S[nS].cust -> startServ = timeNow;
            S[nS].cust -> endServ = timeNow + get_exp(SerRate);
            OP.total_wait += S[nS].cust -> startServ - S[nS].cust -> comeIn;
            OP.total_sys += S[nS].cust -> endServ - S[nS].cust -> comeIn;
            create_customer(ArrRate);
            continue;
        }
        else{
            OP.custNum += 1;
            free(S[nS].cust);
            S[nS].cust = nextC;
            S[nS].cust -> startServ = nextC -> comeIn;
            S[nS].cust -> endServ = nextC -> comeIn + get_exp(SerRate);
            if(nS == 0)
                if(S[0].cust -> startServ > S[1].cust -> endServ)
                    OP.both_idle += (S[0].cust -> startServ - S[1].cust -> endServ);
            if(nS == 1)
                if(S[1].cust -> startServ > S[0].cust -> endServ)
                    OP.both_idle += (S[1].cust -> startServ - S[0].cust -> endServ);
            OP.total_sys += S[nS].cust -> endServ - S[nS].cust -> comeIn;
            create_customer(ArrRate);
            continue;
        }
    }

    // output the final statistics
    // printf("Number of customers: %d\n", OP.custNum);
    printf("Average waiting time: %f\n", OP.total_wait / (double)OP.custNum);
    printf("Average system time: %f\n", OP.total_sys / (double)OP.custNum);
    printf("System utilization ratio: %f\n",(((double)SimTime - OP.both_idle) / (double)SimTime));
    printf("Full utilization ratio: %f\n", (OP.both_busy / (double)SimTime));
    return 0;
}
