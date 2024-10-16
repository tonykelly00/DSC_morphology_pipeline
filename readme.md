
## Analysis pipeline and example data for ExM, EM and STED
Here the analysis pipeline of for all dendrites reconstructed using ExM, EM and STED are provided as well as example reconstuctions for each microscopy method.

### Setup Instructions
should just work of course

### organisation
Analysis pipeline for each microscopy method run using the respective jupyter notebook. Which loads reconstruction of branch or branch segment from .csv files in respective data /table folder.
Reconstructions are compared to raw and binary images and errors are manually corrected, with false positives removes and false negatives added. Changes are noted.

Raw imaging files are provided in decon folder for example dendrites with the accompaning 
    /binary folder - contains binarisation of the raw image using Fiji plugin MaxEntropy 
    /analysis folder - contains local thickness (_LD file) which is the diameter along the dendrite and skeletistaion of dendrites (SK file) to extract the diameter at each point along the dendrite that generated the .csv file in the /table folder


