#include <cstdio>
#include <TH1.h>
#include <TRandom3.h>
#include <TCanvas.h>
#include <TStyle.h>

// 5. Write a computer program which makes a histogram with 10k entries, where each en-
//try is the average of n random numbers on the range (0,1). Do it for n=1, 2, 5, 10, 50.
//Make nice plots, labeling your axes properly.

void problem_5(int n_points = 10000) {
    auto *r = new TRandom3(0);

    TH1F *hist1 = new TH1F("Histogram_1", "Average of 1 random number", 100, 0, 1);

    // hist1->SetLineWith(2);  // For some reason this wasn't working
    hist1->SetFillColor(kAzure-1);
    hist1->GetXaxis()->SetTitle("Average random number value");

    auto *hist2 = (TH1F*)hist1->Clone();
    hist2->SetName("Histogram_2");
    hist2->SetTitle("Average of 2 random numbers");

    auto *hist5 = (TH1F*)hist1->Clone();
    hist5->SetName("Histogram_5");
    hist5->SetTitle("Average of 5 random numbers");

    auto *hist10 = (TH1F*)hist1->Clone();
    hist10->SetName("Histogram_10");
    hist10->SetTitle("Average of 10 random numbers");

    auto *hist50 = (TH1F*)hist1->Clone();
    hist50->SetName("Histogram_50");
    hist50->SetTitle("Average of 50 random numbers");

    auto *c1 = new TCanvas("c1", "Average of 1 random number", 800, 800);
    auto *c2 = new TCanvas("c2", "Average of 2 random numbers", 800, 800);
    auto *c5 = new TCanvas("c5", "Average of 5 random numbers", 800, 800);
    auto *c10 = new TCanvas("c10", "Average of 10 random numbers", 800, 800);
    auto *c50 = new TCanvas("c50", "Average of 50 random numbers", 800, 800);

    Double_t histo_values[5] = {1., 2., 5., 10., 50.};
    TH1F* histo_list[5] = {hist1, hist2, hist5, hist10, hist50};
    TCanvas* canvas_list[5] = {c1, c2, c5, c10, c50};
    Double_t random_total, average;

    for (int histo = 0; histo < 5; histo++) {  // loop over each of five histograms
        // printf("1) %d\n", histo);
        // printf("2) %f\n", histo_values[histo]);
        for (int i = 0; i < n_points; i++) {  // 10000 points
            random_total = 0;
            for (int j = 0.; j < histo_values[histo]; j++) {  // Averaged over 1, 2, 5, 10, 50 points for each sample
                random_total += r -> Rndm();
                // printf("3) (%d) %f\n", j, random_total);
            }
            average = random_total / histo_values[histo];
            // printf("4) %f points - (point # %d) - Average: %f\n", histo_values[histo], i, average);
            // fflush(stdout);
            histo_list[histo] -> Fill(average);

            canvas_list[histo] -> cd();
            histo_list[histo] -> Draw();
        }
    }
}
