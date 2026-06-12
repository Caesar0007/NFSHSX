/* host behavioral test for trnsmult.cpp + matrix.cpp reorthogonalize. 64-bit, libm oracle. */
#include <cstdio>
#include <cmath>
#include <cstring>

extern "C" int fixedmult(int a, int b){ return (int)(((long long)a*(long long)b) >> 16); }
extern "C" void blockmove(void *s,void *d,int n){ memmove(d,s,n); }
extern "C" void transpose(int *s,int *d){
    int i,j; for(i=0;i<3;i++) for(j=0;j<3;j++) d[j*3+i]=s[i*3+j];
}
extern "C" const int identitymatrix[9]={65536,0,0, 0,65536,0, 0,0,65536};

extern "C" int *transmult(int *a,int *b,int *out);          /* trnsmult.cpp */
extern "C" int  reorthogonalize(int *M);                    /* matrix.cpp   */
extern "C" int *addmatrix(int*,int*,int*);
extern "C" int *submatrix(int*,int*,int*);
extern "C" int *scalematrix(int*,int,int*);

static int FX(double v){ return (int)lround(v*65536.0); }
static double DB(int v){ return (double)v/65536.0; }

int main(){
    /* --- 1. trnsmult correctness vs double matmul --- */
    int A[9],B[9],C[9]; double a[9],b[9];
    double seed[18]={0.3,-0.7,1.1, 0.5,0.2,-0.9, -0.4,0.8,0.6,
                     1.0,0.1,-0.2, -0.3,0.7,0.4,  0.9,-0.5,0.25};
    for(int i=0;i<9;i++){a[i]=seed[i];   A[i]=FX(a[i]);}
    for(int i=0;i<9;i++){b[i]=seed[9+i]; B[i]=FX(b[i]);}
    transmult(A,B,C);
    int mulbad=0; double mulmax=0;
    for(int i=0;i<3;i++)for(int k=0;k<3;k++){
        double ref=0; for(int j=0;j<3;j++) ref+=a[i*3+j]*b[j*3+k];
        double err=fabs(DB(C[i*3+k])-ref); if(err>mulmax)mulmax=err;
        if(err>1e-3) mulbad++;
    }
    printf("trnsmult: maxerr=%.6f  %s\n", mulmax, mulbad?"FAIL":"PASS");

    /* alias safety: C=A*A into A itself */
    int Acopy[9]; memcpy(Acopy,A,sizeof A);
    transmult(A,A,A);
    int Ref[9]; transmult(Acopy,Acopy,Ref);
    printf("trnsmult alias-safe: %s\n", memcmp(A,Ref,sizeof A)?"FAIL":"PASS");

    /* --- 2. reorthogonalize: perturb a real rotation, expect M^T M -> I --- */
    double ang=0.6;                     /* a rotation about Z with realistic per-frame drift */
    double R[9]={ cos(ang),-sin(ang),0,  sin(ang),cos(ang),0,  0,0,1 };
    double dent[9]={0.004,-0.003,0.002, 0.0,0.005,-0.004, 0.003,-0.002,0.006};
    int M[9]; for(int i=0;i<9;i++) M[i]=FX(R[i]+dent[i]);

    /* orthonormality error before */
    int MT[9],G[9]; transpose(M,MT); transmult(MT,M,G);
    double before=0; for(int i=0;i<9;i++){double e=DB(G[i])-DB(identitymatrix[i]); before+=e*e;}
    before=sqrt(before);

    reorthogonalize(M);

    transpose(M,MT); transmult(MT,M,G);
    double after=0; for(int i=0;i<9;i++){double e=DB(G[i])-DB(identitymatrix[i]); after+=e*e;}
    after=sqrt(after);
    /* contract: a weak (1/4-weight) per-frame drift cleaner -- error must shrink markedly */
    printf("reorthogonalize: ||M^TM-I|| before=%.5f after=%.5f (%.1fx)  %s\n",
           before, after, before/after, (after<before*0.5)?"PASS":"FAIL");

    /* det should be ~1 (proper rotation) */
    double m[9]; for(int i=0;i<9;i++)m[i]=DB(M[i]);
    double det=m[0]*(m[4]*m[8]-m[5]*m[7]) - m[1]*(m[3]*m[8]-m[5]*m[6]) + m[2]*(m[3]*m[7]-m[4]*m[6]);
    printf("reorthogonalize: det=%.5f  %s\n", det, (fabs(det-1.0)<0.01)?"PASS":"FAIL");
    return 0;
}
