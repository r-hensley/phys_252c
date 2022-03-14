                  
// fit data to Gaussian

#include <iostream>
#include <iomanip>
#include <fstream>
#include "TH1F.h"
#include "TFile.h"
#include "TMinuit.h"

#define PI      3.14159265 
#define ROOT2PI 2.50663

using namespace std;

int nbinsx = 50;

// routine to integrate gaussian from xlo to hi

double gint(double xlo, double xhi, double mu, double sig)
{
  double dx = (xhi-xlo)/100.0;

  double gsum = 0.;
  for(int i = 0; i<100; i++)
    {
      double x = xlo + dx/2. + dx*(double)(i) ;
      gsum += exp(-(x-mu)*(x-mu)/2.0/sig/sig) ;
    }

  return gsum*dx/sig/ROOT2PI ;
}


// MINUIT objective function

void fcn(int &npar, double *grad, double &fcnval, double *xval, int iflag)
{

    // link to histogram

    TH1F *h1f = (TH1F*)gDirectory->Get("h1f");

    // calculate -lnL

    double fsum = 0.0;

    for(int i=0; i<=nbinsx; i++) {
        if (h1f ->GetBinContent(i) == 0.) {continue;};

        double xlo = static_cast<float>(i-1) * 20.0;
        double xhi = xlo + 20.0;

        double mu  = xval[1]*20. + xval[0]*gint(xlo,xhi,xval[2],50);

        double y = h1f->GetBinContent(i);

        fsum = fsum - (y*log(mu)-mu);
    }

    fcnval = 2.0 * fsum ;

}

void minres_original()
{

    // initialize histogram with data

    auto h1f = new TH1F("Resonance Histogram", "Resonance data", nbinsx, 0, 1000);

    ifstream res_data;
    res_data.open("../../Data/resonance.dat");

    string line;

    while(getline(res_data,line)){
        double mass = strtod(line.c_str(), (char**)nullptr); //  atof(line.c_str())
        h1f->Fill(mass);
    }

    double bin_content;
    for (int i=0; i<=nbinsx; i++) {
        bin_content = h1f -> GetBinContent(i);
        printf("%d) %f\n", i, bin_content);
    };


    // initialize MINUIT

    auto *gMinuit = new TMinuit(5);

    gMinuit->SetFCN(fcn);

    double arglist[10];
    int error_flag = 0;

    arglist[0]=1;
    gMinuit->mnexcm("SET ERR",arglist,1,error_flag);

    gMinuit->mninit(5,6,7);  // 5 = stdin, 6 = stdout, 7 = stderr

    // set up parameters

    double f_null=0.0;
    error_flag = 0;

    gMinuit->mnparm(0,  "s",1000.,10.,f_null,f_null,error_flag);  // 1000 = initial par. guess
    gMinuit->mnparm(1,  "b",  10., 1.,f_null,f_null,error_flag);  // 1 = initial err. guess
    gMinuit->mnparm(2,  "mu",  500., 5.,f_null,f_null,error_flag);

    // minimize

    gMinuit->mnexcm("SIMPLEX",0,0,error_flag);
    gMinuit->mnexcm( "MIGRAD",0,0,error_flag);
    gMinuit->mnexcm(  "MINOS",0,0,error_flag);

    // get parameters

    double pval[3], perr[3], plo[3], phi[3];
    TString para0, para1, para2;
    int istat;

    gMinuit->mnpout(0,para0,pval[0],perr[0],plo[0],phi[0],istat);
    gMinuit->mnpout(1,para1,pval[1],perr[1],plo[1],phi[1],istat);
    gMinuit->mnpout(2,para2,pval[2],perr[2],plo[2],phi[2],istat);


    // display results

    cout << setw(8) << pval[0] << setw(8) << perr[0] << endl;
    cout << setw(8) << pval[1] << setw(8) << perr[1] << endl;
    cout << setw(8) << pval[2] << setw(8) << perr[2] << endl;

}


//0) 0.000000
//1) 0.000000
//2) 0.000000
//3) 0.000000
//4) 0.000000
//5) 0.000000
//6) 203.000000
//7) 171.000000
//8) 225.000000
//9) 183.000000
//10) 178.000000
//11) 200.000000
//12) 187.000000
//13) 241.000000
//14) 196.000000
//15) 199.000000
//16) 214.000000
//17) 210.000000
//18) 210.000000
//19) 200.000000
//20) 233.000000
//21) 211.000000
//22) 172.000000
//23) 195.000000
//24) 190.000000
//25) 201.000000
//26) 206.000000
//27) 205.000000
//28) 198.000000
//29) 200.000000
//30) 249.000000
//31) 214.000000
//32) 251.000000
//33) 283.000000
//34) 316.000000
//35) 364.000000
//36) 315.000000
//37) 330.000000
//38) 283.000000
//39) 279.000000
//40) 263.000000
//41) 223.000000
//42) 209.000000
//43) 223.000000
//44) 177.000000
//45) 208.000000
//46) 193.000000
//47) 186.000000
//48) 210.000000
//49) 203.000000
//50) 192.000000
//51) 1.000000
//52) 1.000000
//53) 1.000000
//54) 1.000000
//55) 1.000000
//**********
//**    1 **SET ERR           1
//**********
//PARAMETER DEFINITIONS:
//   NO.   NAME         VALUE      STEP SIZE      LIMITS
//    1 s            1.00000e+03  1.00000e+01     no limits
//    2 b            1.00000e+01  1.00000e+00     no limits
//    3 mu           5.00000e+02  5.00000e+00     no limits
//**********
//**    1 **SIMPLEX
//**********
//FIRST CALL TO USER FUNCTION AT NEW START POINT, WITH IFLAG=4.
//START SIMPLEX MINIMIZATION.    CONVERGENCE WHEN EDM .LT. 0.1
//FCN=-88290.3 FROM SIMPLEX   STATUS=PROGRESS       14 CALLS          15 TOTAL
//                    EDM=720.687    STRATEGY= 1      NO ERROR MATRIX
// EXT PARAMETER               CURRENT GUESS      PHYSICAL LIMITS
// NO.   NAME      VALUE            ERROR       NEGATIVE      POSITIVE
//  1  s            5.16000e+02   1.00000e+01
//  2  b            1.10000e+01   1.00000e+00
//  3  mu           7.00000e+02   5.00000e+00
//SIMPLEX MINIMIZATION HAS CONVERGED.
//FCN=-88365.6 FROM SIMPLEX   STATUS=PROGRESS       67 CALLS          68 TOTAL
//                    EDM=0.0437065    STRATEGY= 1      NO ERROR MATRIX
// EXT PARAMETER               CURRENT GUESS      PHYSICAL LIMITS
// NO.   NAME      VALUE            ERROR       NEGATIVE      POSITIVE
//  1  s            9.15740e+02   1.00000e+01
//  2  b            1.00940e+01   1.00000e+00
//  3  mu           7.05531e+02   5.00000e+00
//**********
//**    2 **MIGRAD
//**********
//START MIGRAD MINIMIZATION.  STRATEGY  1.  CONVERGENCE WHEN EDM .LT. 1.00e-04
//FCN=-88365.6 FROM MIGRAD    STATUS=INITIATE       10 CALLS          78 TOTAL
//                    EDM= unknown      STRATEGY= 1      NO ERROR MATRIX
// EXT PARAMETER               CURRENT GUESS       STEP         FIRST
// NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//  1  s            9.15740e+02   1.00000e+01   9.29791e+00   4.71189e-04
//  2  b            1.00940e+01   1.00000e+00   2.89471e-02   2.20501e-01
//  3  mu           7.05531e+02   5.00000e+00   1.17141e+00   2.30481e-02
//MIGRAD MINIMIZATION HAS CONVERGED.
//MIGRAD WILL VERIFY CONVERGENCE AND ERROR MATRIX.
//COVARIANCE MATRIX CALCULATED SUCCESSFULLY
//FCN=-88365.6 FROM MIGRAD    STATUS=CONVERGED      45 CALLS         113 TOTAL
//                    EDM=7.20792e-07    STRATEGY= 1      ERROR MATRIX ACCURATE
// EXT PARAMETER                                   STEP         FIRST
// NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//  1  s            9.15232e+02   5.80051e+01   7.74396e+00   4.03346e-06
//  2  b            1.00931e+01   1.19268e-01   1.59243e-02  -5.01499e-03
//  3  mu           7.05336e+02   4.08849e+00   5.93464e-01  -2.35198e-04
//EXTERNAL ERROR MATRIX.    NDIM=  25    NPAR=  3    ERR DEF=1
// 3.365e+03 -2.713e+00  1.187e+00
//-2.713e+00  1.422e-02 -1.312e-03
// 1.187e+00 -1.312e-03  1.672e+01
//PARAMETER  CORRELATION COEFFICIENTS
//      NO.  GLOBAL      1      2      3
//       1  0.39216   1.000 -0.392  0.005
//       2  0.39214  -0.392  1.000 -0.003
//       3  0.00507   0.005 -0.003  1.000
//**********
//**    3 **MINOS
//**********
//FCN=-88365.6 FROM MINOS     STATUS=SUCCESSFUL     70 CALLS         183 TOTAL
//                    EDM=7.20792e-07    STRATEGY= 1      ERROR MATRIX ACCURATE
// EXT PARAMETER                  PARABOLIC         MINOS ERRORS
// NO.   NAME      VALUE            ERROR      NEGATIVE      POSITIVE
//  1  s            9.15232e+02   5.80051e+01  -5.77292e+01   5.83618e+01
//  2  b            1.00931e+01   1.19268e-01  -1.18857e-01   1.19839e-01
//  3  mu           7.05336e+02   4.08849e+00  -4.08959e+00   4.09305e+00
//915.232 58.0051
//10.09310.119268
//705.336 4.08849