# gbn-vansjo

Data and code for developing, evaluating and benchmarking a Gaussian Bayesian Network (GBN) to forecast summer seasonally-aggregated water quality, applied to Lake Vansjø in southeast Norway.

Data sources:
* Precipitation and air temperature were derived from the seNorge 1 km2 gridded data (Lussana et al., 2019), averaged over the whole catchment area of Lake Vansjø
* Wind speed data were from the met.no monitoring location at Rygge airport, by the southern edge of Lake Vansjø
* Hobøl River discharge is measured hourly by NVE at Høgfoss, and was aggregated to a daily sum
* TP concentration data from the Hobøl River at Kure are collected by NIBIO. Lake water quality data are collected by NIVA. Both datasets were downloaded from Vannmiljø (https://vannmiljo.miljodirektoratet.no/, last accessed 01/11/2021), aside from cyanobacteria data, which was provided by NIVA directy.
* TP, chl-a and colour data were downloaded from Vannmiljø whilst cyanobacteria biovolume was provided by NIVA (pers. comm). NIVA colour data were patchy over the period 1998-2007. 


# References
Lussana, C., Tveito, O. E., Dobler, A., & Tunheim, K. (2019). seNorge_2018, daily precipitation, and temperature datasets over Norway. Earth Syst. Sci. Data, 11(4), 1531-1551. https://doi.org/10.5194/essd-11-1531-2019
