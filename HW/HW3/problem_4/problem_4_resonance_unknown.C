                  
// fit data to Gaussian

#include <iostream>
#include <iomanip>
#include <fstream>
#include <TCanvas.h>

#include "TF1.h"
#include "TH1F.h"
#include "TFile.h"
#include "TMinuit.h"
#include "TLatex.h"
#include "TLegend.h"

#define PI      3.14159265 
#define ROOT2PI 2.50663
double hist_lo = 200.;
double hist_hi = 1000.;
int nbinsx = 32;
double bin_width = (hist_hi - hist_lo) / nbinsx;

using namespace std;

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

        double xlo = 200 + static_cast<float>(i-1) * bin_width;
        double xhi = xlo + bin_width;

        /*
        printf("(%d) binlow=%f, binhigh=%f, xlo=%f, xhi=%f\n",
               i,
               h1f->GetBinLowEdge(i),
               h1f->GetBinLowEdge(i) + h1f->GetBinWidth(i),
               xlo,
               xhi);
        */

        double mu  = xval[1]*bin_width + xval[0]*gint(xlo, xhi,xval[2],50);

        double y = h1f->GetBinContent(i);

        fsum = fsum - (y*log(mu)-mu);
    }

    fcnval = 2.0 * fsum ;

}

void minres()
{

    // initialize histogram with data

    auto h1f = new TH1F("Resonance Histogram","Resonance data", nbinsx,hist_lo,hist_hi);

    ifstream res_data;
    // res_data.open("../../Data/resonance.dat");
    res_data.open("../../Data/resonance-unknown.dat");

    string line;

    while(getline(res_data,line)){
        double mass = strtod(line.c_str(), (char**)nullptr); //  atof(line.c_str())
        // printf("%f\n", mass);
        h1f->Fill(mass);
    }

    double bin_content;
    for (int i=0; i<=nbinsx; i++) {
        bin_content = h1f -> GetBinContent(i);
        printf("%d) %f\n", i, bin_content);
    };

    auto *c = new TCanvas("Canvas", "Unknown resonance data", 800, 800);
    c->cd();
    h1f->Draw();

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

    gMinuit->mnparm(0,  "s",1000.,10.,f_null,f_null,error_flag);
    gMinuit->mnparm(1,  "b",  10., 1.,f_null,f_null,error_flag);
    gMinuit->mnparm(2,  "mu",  500., 5.,f_null,f_null,error_flag);

    // minimize

    gMinuit->mnexcm("SIMPLEX",0,0,error_flag);
    gMinuit->mnexcm( "MIGRAD",0,0,error_flag);
    gMinuit->mnexcm(  "MINOS",0,0,error_flag);

    // get parameters

    double pval[3],perr[3],plo[3],phi[3];

    TString para0,para1,para2;

    int istat;

    gMinuit->mnpout(0,para0,pval[0],perr[0],plo[0],phi[0],istat);
    gMinuit->mnpout(1,para1,pval[1],perr[1],plo[1],phi[1],istat);
    gMinuit->mnpout(2,para2,pval[2],perr[2],plo[2],phi[2],istat);

    // display results

    cout << setw(8) << pval[0] << setw(8) << perr[0] << endl;
    cout << setw(8) << pval[1] << setw(8) << perr[1] << endl;
    cout << setw(8) << pval[2] << setw(8) << perr[2] << endl;

    TF1 *gauss_fit = new TF1("gauss_fit",
                             "[0]*[1] + [1]*[4]*exp(-((x-[2])*(x-[2]))/(2*50*50))/(50*[3])",
                             200,
                             1000);
    gauss_fit->SetParameter(0, pval[1]);  // background
    gauss_fit->SetParameter(1, bin_width);  // bin width
    gauss_fit->SetParameter(2, pval[2]);  // mu
    gauss_fit->SetParameter(3, ROOT2PI);  // sqrt(2pi)
    gauss_fit->SetParameter(4, pval[0]);  // s
    gauss_fit->Draw("Same");

    auto leg = new TLegend(.65, .675, .98, .76);
    leg ->AddEntry(h1f, "Unknown resonance data");
    leg ->AddEntry(gauss_fit, "Gaussian fit");
    leg ->Draw("Same");

    TLatex Tl;
    Tl.SetTextSize(0.03);
    Tl.DrawLatex(230, 280, Form("#sigma=%f", pval[0]));
    Tl.DrawLatex(230, 268, Form("b=%f", pval[1]));
    Tl.DrawLatex(230, 256, Form("#mu=%f", pval[2]));

    h1f->GetXaxis()->SetTitle("Signal Cross Section: #sigma (fb)");
    h1f->GetYaxis()->SetTitle("Events");
}



// 0) 0.000000
//1) 92.000000
//2) 91.000000
//3) 70.000000
//4) 73.000000
//5) 101.000000
//6) 75.000000
//7) 90.000000
//8) 78.000000
//9) 81.000000
//10) 91.000000
//11) 99.000000
//12) 84.000000
//13) 106.000000
//14) 108.000000
//15) 192.000000
//16) 201.000000
//17) 278.000000
//18) 268.000000
//19) 236.000000
//20) 194.000000
//21) 142.000000
//22) 115.000000
//23) 96.000000
//24) 89.000000
//25) 96.000000
//26) 82.000000
//27) 109.000000
//28) 83.000000
//29) 85.000000
//30) 94.000000
//31) 93.000000
//32) 86.000000
// **********
// **    1 **SET ERR           1
// **********
// PARAMETER DEFINITIONS:
//    NO.   NAME         VALUE      STEP SIZE      LIMITS
//     1 s            1.00000e+03  1.00000e+01     no limits
//     2 b            1.00000e+01  1.00000e+00     no limits
//     3 mu           5.00000e+02  5.00000e+00     no limits
// **********
// **    1 **SIMPLEX
// **********
// FIRST CALL TO USER FUNCTION AT NEW START POINT, WITH IFLAG=4.
// START SIMPLEX MINIMIZATION.    CONVERGENCE WHEN EDM .LT. 0.1
// FCN=-26156 FROM SIMPLEX   STATUS=PROGRESS       11 CALLS          12 TOTAL
//                     EDM=1693.92    STRATEGY= 1      NO ERROR MATRIX
//  EXT PARAMETER               CURRENT GUESS      PHYSICAL LIMITS
//  NO.   NAME      VALUE            ERROR       NEGATIVE      POSITIVE
//   1  s           -4.56000e+02   1.00000e+01
//   2  b            1.00000e+01   1.00000e+00
//   3  mu           5.00000e+02   5.00000e+00
//  FUNCTION VALUE DOES NOT SEEM TO DEPEND ON ANY OF THE 3 VARIABLE PARAMETERS.
//          VERIFY THAT STEP SIZES ARE BIG ENOUGH AND CHECK FCN LOGIC.
// *******************************************************************************
// *******************************************************************************
// SIMPLEX TERMINATES WITHOUT CONVERGENCE.
// FCN=-26156 FROM SIMPLEX   STATUS=CALL LIMIT    549 CALLS         550 TOTAL
//                     EDM=-nan    STRATEGY= 1      NO ERROR MATRIX
//  EXT PARAMETER               CURRENT GUESS      PHYSICAL LIMITS
//  NO.   NAME      VALUE            ERROR       NEGATIVE      POSITIVE
//   1  s           -4.56000e+02   1.00000e+01
//   2  b            1.00000e+01   1.00000e+00
//   3  mu           5.00000e+02   5.00000e+00
// **********
// **    2 **MIGRAD
// **********
// START MIGRAD MINIMIZATION.  STRATEGY  1.  CONVERGENCE WHEN EDM .LT. 1.00e-04
// FCN=-26156 FROM MIGRAD    STATUS=INITIATE       10 CALLS         560 TOTAL
//                     EDM= unknown      STRATEGY= 1      NO ERROR MATRIX
//  EXT PARAMETER               CURRENT GUESS       STEP         FIRST
//  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//   1  s           -4.56000e+02   1.00000e+01          -nan   7.87410e-01
//   2  b            1.00000e+01   1.00000e+00          -nan   7.89106e+02
//   3  mu           5.00000e+02   5.00000e+00          -nan   2.69735e+00
// MIGRAD FAILS TO FIND IMPROVEMENT
// EIGENVALUES OF SECOND-DERIVATIVE MATRIX:
//        -6.3411e-02  8.7501e-01  2.1884e+00
// MINUIT WARNING IN HESSE
// ============== MATRIX FORCED POS-DEF BY ADDING 0.065600 TO DIAGONAL.
// FCN=-26156 FROM HESSE     STATUS=NOT POSDEF     16 CALLS         587 TOTAL
//                     EDM=3654.29    STRATEGY= 1      ERR MATRIX NOT POS-DEF
//  EXT PARAMETER                APPROXIMATE        STEP         FIRST
//  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//   1  s           -4.56000e+02   7.13961e+02   3.63732e+00   7.87413e-01
//   2  b            1.00000e+01   9.79059e-01   1.18660e-02   7.89106e+02
//   3  mu           5.00000e+02   8.23554e+01   3.94851e-01   2.69734e+00
// MIGRAD FAILS TO FIND IMPROVEMENT
// MIGRAD TERMINATED WITHOUT CONVERGENCE.
// FCN=-26156 FROM MIGRAD    STATUS=FAILED         48 CALLS         598 TOTAL
//                     EDM=3654.29    STRATEGY= 1      ERR MATRIX NOT POS-DEF
//  EXT PARAMETER                APPROXIMATE        STEP         FIRST
//  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//   1  s           -4.56000e+02   7.13961e+02  -0.00000e+00   7.87413e-01
//   2  b            1.00000e+01   9.79059e-01   0.00000e+00   7.89106e+02
//   3  mu           5.00000e+02   8.23554e+01  -0.00000e+00   2.69734e+00
// EXTERNAL ERROR MATRIX.    NDIM=  25    NPAR=  3    ERR DEF=1
//  5.097e+05 -6.911e+02  5.864e+04
// -6.911e+02  9.586e-01 -7.938e+01
//  5.864e+04 -7.938e+01  6.782e+03
//ERR MATRIX NOT POS-DEF
// PARAMETER  CORRELATION COEFFICIENTS
//       NO.  GLOBAL      1      2      3
//        1  0.99805   1.000 -0.989  0.997
//        2  0.98889  -0.989  1.000 -0.984
//        3  0.99733   0.997 -0.984  1.000
// ERR MATRIX NOT POS-DEF
// **********
// **    3 **MINOS
// **********
// FUNCTION MUST BE MINIMIZED BEFORE CALLING MINOs
// START MIGRAD MINIMIZATION.  STRATEGY  1.  CONVERGENCE WHEN EDM .LT. 1.00e-04
// FCN=-26156 FROM MIGRAD    STATUS=INITIATE        6 CALLS         604 TOTAL
//                     EDM=3654.28    STRATEGY= 1      ERR MATRIX NOT POS-DEF
//  EXT PARAMETER                APPROXIMATE        STEP         FIRST
//  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//   1  s           -4.56000e+02   7.13961e+02  -0.00000e+00   7.87410e-01
//   2  b            1.00000e+01   9.79059e-01   0.00000e+00   7.89106e+02
//   3  mu           5.00000e+02   8.23554e+01  -0.00000e+00   2.69735e+00
// MIGRAD FAILS TO FIND IMPROVEMENT
// EIGENVALUES OF SECOND-DERIVATIVE MATRIX:
//        -6.4237e-02  8.7495e-01  2.1893e+00
// MINUIT WARNING IN HESSE
// ============== MATRIX FORCED POS-DEF BY ADDING 0.066426 TO DIAGONAL.
// FCN=-26156 FROM HESSE     STATUS=NOT POSDEF     16 CALLS         631 TOTAL
//                     EDM=3661.13    STRATEGY= 1      ERR MATRIX NOT POS-DEF
//  EXT PARAMETER                APPROXIMATE        STEP         FIRST
//  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//   1  s           -4.56000e+02   7.13805e+02   3.63724e+00   7.87413e-01
//   2  b            1.00000e+01   9.77749e-01   1.18662e-02   7.89106e+02
//   3  mu           5.00000e+02   8.23630e+01   4.90582e-01   2.69734e+00
// MIGRAD FAILS TO FIND IMPROVEMENT
// MIGRAD TERMINATED WITHOUT CONVERGENCE.
// FCN=-26156 FROM MIGRAD    STATUS=FAILED         44 CALLS         642 TOTAL
//                     EDM=3661.13    STRATEGY= 1      ERR MATRIX NOT POS-DEF
//  EXT PARAMETER                APPROXIMATE        STEP         FIRST
//  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//   1  s           -4.56000e+02   7.13805e+02  -0.00000e+00   7.87413e-01
//   2  b            1.00000e+01   9.77749e-01   0.00000e+00   7.89106e+02
//   3  mu           5.00000e+02   8.23630e+01  -0.00000e+00   2.69734e+00
// EXTERNAL ERROR MATRIX.    NDIM=  25    NPAR=  3    ERR DEF=1
//  5.095e+05 -6.900e+02  5.863e+04
// -6.900e+02  9.560e-01 -7.928e+01
//  5.863e+04 -7.928e+01  6.784e+03
//ERR MATRIX NOT POS-DEF
// PARAMETER  CORRELATION COEFFICIENTS
//       NO.  GLOBAL      1      2      3
//        1  0.99805   1.000 -0.989  0.997
//        2  0.98886  -0.989  1.000 -0.984
//        3  0.99733   0.997 -0.984  1.000
// ERR MATRIX NOT POS-DEF
// EIGENVALUES OF SECOND-DERIVATIVE MATRIX:
//        -6.2578e-02  8.7490e-01  2.1877e+00
// MINUIT WARNING IN HESSE
// ============== MATRIX FORCED POS-DEF BY ADDING 0.064766 TO DIAGONAL.
// MINUIT WARNING IN MIGRAD
// ============== Negative diagonal element 1 in Error Matrix
// MINUIT WARNING IN MIGRAD
// ============== Negative diagonal element 2 in Error Matrix
// MINUIT WARNING IN MIGRAD
// ============== 7.94285 added to diagonal of error matrix
// CALL LIMIT EXCEEDED IN MIGRAD.
//                         NEGATIVE MINOS ERROR NOT CALCULATED FOR PARAMETER 1
// MIGRAD FAILS WITH STRATEGY=0.   WILL TRY WITH STRATEGY=1.
// EIGENVALUES OF SECOND-DERIVATIVE MATRIX:
//        -6.8915e+00  8.8915e+00
// MINUIT WARNING IN MIGRAD
// ============== MATRIX FORCED POS-DEF BY ADDING 6.900345 TO DIAGONAL.
// FCN=-26164.1 FROM MINOS     STATUS=NEW MINIMU   1401 CALLS        2059 TOTAL
//                     EDM= unknown      STRATEGY= 1      NO ERROR MATRIX
//  EXT PARAMETER                  PARABOLIC         MINOS ERRORS
//  NO.   NAME      VALUE            ERROR      NEGATIVE      POSITIVE
//   1  s            1.67683e+03   4.43338e+01                 4.94361e+03
//   2  b            7.43922e-01   9.85618e-01                 7.80449e-01
//   3  mu           6.31323e+02   1.87318e+00
// NEW MINIMUM FOUND.  GO BACK TO MINIMIZATION STEP.
// =================================================
//                                                  V
//                                                  V
//                                                  V
//                                               VVVVVVV
//                                                VVVVV
//                                                 VVV
//                                                  V
//
// START MIGRAD MINIMIZATION.  STRATEGY  1.  CONVERGENCE WHEN EDM .LT. 5.00e-05
// FCN=-26164.1 FROM MIGRAD    STATUS=INITIATE        6 CALLS        2065 TOTAL
//                     EDM= unknown      STRATEGY= 1      NO ERROR MATRIX
//  EXT PARAMETER               CURRENT GUESS       STEP         FIRST
//  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//   1  s            1.67683e+03   4.43338e+01  -3.31298e+00   2.53359e-05
//   2  b            7.43922e-01   9.85618e-01   9.85618e-01  -4.04897e+03
//   3  mu           6.31323e+02   1.87318e+00  -4.02300e-03  -7.40800e-05
// MIGRAD MINIMIZATION HAS CONVERGED.
// MIGRAD WILL VERIFY CONVERGENCE AND ERROR MATRIX.
// COVARIANCE MATRIX CALCULATED SUCCESSFULLY
// FCN=-29191 FROM MIGRAD    STATUS=CONVERGED      86 CALLS        2145 TOTAL
//                     EDM=1.20933e-08    STRATEGY= 1      ERROR MATRIX ACCURATE
//  EXT PARAMETER                                   STEP         FIRST
//  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
//   1  s            9.63309e+02   4.40547e+01   3.43036e+00  -1.58398e-06
//   2  b            3.51836e+00   7.69611e-02   5.99170e-03   4.18416e-04
//   3  mu           6.30655e+02   2.69574e+00   2.24870e-01   4.80282e-05
// EXTERNAL ERROR MATRIX.    NDIM=  25    NPAR=  3    ERR DEF=1
//  1.941e+03 -1.220e+00  4.909e-01
// -1.220e+00  5.923e-03 -6.121e-04
//  4.909e-01 -6.121e-04  7.267e+00
// PARAMETER  CORRELATION COEFFICIENTS
//       NO.  GLOBAL      1      2      3
//        1  0.35972   1.000 -0.360  0.004
//        2  0.35971  -0.360  1.000 -0.003
//        3  0.00442   0.004 -0.003  1.000
// FCN=-29191 FROM MINOS     STATUS=SUCCESSFUL    100 CALLS        2245 TOTAL
//                     EDM=1.20933e-08    STRATEGY= 1      ERROR MATRIX ACCURATE
//  EXT PARAMETER                  PARABOLIC         MINOS ERRORS
//  NO.   NAME      VALUE            ERROR      NEGATIVE      POSITIVE
//   1  s            9.63309e+02   4.40547e+01  -4.37518e+01   4.43954e+01
//   2  b            3.51836e+00   7.69611e-02  -7.64622e-02   7.75232e-02
//   3  mu           6.30655e+02   2.69574e+00  -2.69641e+00   2.69649e+00
// 963.309 44.0547
// 3.51836 0.0769611
// 630.655 2.69574
