# gbn-vansjo

Data and code for developing, evaluating and benchmarking a Gaussian Bayesian Network (GBN) to forecast summer seasonally-aggregated water quality, applied to Lake Vansjø in southeast Norway.

## Code

Code is in the folder 'Notebooks', and is written in Jupyter notebooks. Python kernels are used for all but two notebooks,  NB05 (BN development and cross validation) and NB09 (fitting the final BN), which both make use of the bnlearn R package and therefore use R kernels. Each notebook contains an introduction, which briefly describes the purpose of the notebook. 

In summary, the notebooks include the following:

* 01_generate_features: generate potential explanatory variables for use in the exploratory statistical analyses, including aggregating daily data to seasonal (6-monthly).
* 02_exploratory stats: exploratory statistical analyses, including plotting time series, scatterplot matrices and calculating correlation coefficients
* FeatureImportance: folder containing feature importance analysis, with one notebook per dependent variable of interest
* 02b_prepeak_aggregation_stats: similar to 02, but replacing the 6-month growing season temporal aggregation with a shorter aggregation (see notebook for more details)
* 02c_monthly_exploratory_stats: similar to 02, but using monthly temporal aggregation of the data
* 03_select_features_xval_setup: make data matrices for development of continuous Bayesian Network, including a variety of cross-slices of the data for use in cross validation of different network structures.
* 04_discretization: discretization of the continuous data for use when developing a discrete network
* 05_BN_development_xval_R: R code for developing continuous and discrete Bayesian Networks and cross validation of a variety of BN structures
* 06_BN_xval_postprocess_python: python code to post-process the results of cross validation runs from the previous notebook, including calculating a variety of model performance statistics.
* 07_make_training_evaluation_data: Set up for generating hindcast predictions using the whole continuous BN (rather than small parts of the network, as in the cross validation)
* 08_Fit_BN: R code to re-fit a Gaussian Bayesian Network using training data from notebook 07 (without NaN-filling, which was carried out before NB05)
* 09_Generate_hindcasts: Predict with GBNs (fit in notebook 08) for the hindcast period, with and without weather nodes. Also generate a seasonal naive hindcast.
* 10_Hindcast_model_comparison: Compare models for the hindcast period (time series and stats)

Files bayes_net_utils.py and .R contain some convenience functions.

The code was written to obtain results, sometimes in a rush, and is therefore messy in places! Tidying is needed. E.g. boundaries_dict (or boundaries_list in R) should be removed from the functions in bayes_net_utils and be user input. Lots of other areas where boiler plate code could be factored into functions.


## Data sources

Data sources in the "Data/raw_input_data" folder are as follows:

* Precipitation and air temperature were derived from the seNorge 1 km2 gridded data (Lussana et al., 2019), averaged over the whole catchment area of Lake Vansjø
* Wind speed data were from the met.no monitoring location at Rygge airport, by the southern edge of Lake Vansjø.
* Hobøl River discharge is measured hourly by NVE at Høgfoss, and was aggregated to a daily sum.
* TP concentration data from the Hobøl River at Kure are collected by NIBIO. Lake water quality data are collected by NIVA. Both datasets were downloaded from Vannmiljø (https://vannmiljo.miljodirektoratet.no/, last accessed 01/11/2021), aside from cyanobacteria data, which was provided by NIVA directy (personal communication).
* TP, chl-a and colour data were downloaded from Vannmiljø whilst cyanobacteria biovolume was provided by NIVA (pers. comm). NIVA colour data were patchy over the period 1998-2007, and were supplemented with data provided by Morsa (pers. comm.).


## References
Lussana, C., Tveito, O. E., Dobler, A., & Tunheim, K. (2019). seNorge_2018, daily precipitation, and temperature datasets over Norway. Earth Syst. Sci. Data, 11(4), 1531-1551. https://doi.org/10.5194/essd-11-1531-2019


## Acknowledgements
Funding: This work was carried out as part of the WATExR project, part of ERA4CS, an ERA-NET initiated by JPI Climate. The work was funded by the Research Council of Norway (Project 274208), with co-funding by the European Union (Grant 690462). Thanks to James Sample for help with Python/R integration.