
## Analysis pipeline and example data for ExM, EM and STED
Here the analysis pipeline of for all dendrites reconstructed using ExM, EM and STED are provided as well as example reconstuctions for each microscopy method.
Analysis of diameters extracted from imaging files is performed in python analysis code is provided on GitHub and extracted diamter data on Zenodo repository 

### Setup Instructions
Download the data repository from [Zenodo](https://zenodo.org/records/14037025?preview=1&token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6ImY4NDE2YWU2LTlmMmEtNGY4NS04M2EwLTg4NzhhMTY1NGRhYSIsImRhdGEiOnt9LCJyYW5kb20iOiJiMGI0YmUwYTg3MjI3MThiNjU5MmY4YjVkOGE3MDE5MiJ9.3r6XoHH6eZQwoqN2nKAh0WgprCR1NjNeP7sbtyx3r9XMjD7o_HtmfZ2qxccQYmhidxqBO5on_0IdoWTX1FDYQg) and the analysis code from [GitHub](https://github.com/tonykelly00/DSC_morphology_pipeline.git).
In ipynb set root folder to location of repo_data/ 

### Organisation
Analysis pipeline for each microscopy method run using the respective jupyter notebook. Which loads reconstruction of branch or branch segment from the provided .csv files found in respective data /table folder.
Reconstructions are compared to raw and binary images and errors are manually corrected, with false positives removes and false negatives added. Changes are noted.

The default code shows the reconstuction and idetified DSCs for the example dendrite in the Figs. Diamters of other dendritic reconstructions can be explored.

![example diameter plot](<figs/Diam_branch_C1_03_cell2_d3.png>)


The full example dendritic morphology using expansion microcsopy is provided with raw data, binarised data and local thickness (diameter) analysis

![example dendrite](<figs/20210201_dg-t1_af488-03_decon-Resolution Level 1_8bit_100-20000_Zproj.png>)

Raw imaging files are provided in /raw and /decon folders for example dendrites with the accompaning <br>
    >> /binary folder - contains binarisation of the raw image using Fiji plugin MaxEntropy <br>
    >> /analysis folder - contains local thickness (_LD file) which is the diameter along the dendrite and skeletistaion of dendrites (SK file) to extract the diameter at each point along the dendrite that generated the .csv file in the /table folder


 


