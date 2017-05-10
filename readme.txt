Welcome to Multi-Reference Population Genome Compression!

The source code is split into four subdirectories: GenomeData, Compression, Visualization and Results. In the main directory, there also exists main.py and params.py. These form the main driver for the code.

GenomeData: Contains a variety of files used for querying, processing and reading the data. A subfolder called Queries stores the BigQuery queries needed to generate 1000 Genomes data. Because these queries can be expensive and require Google Genomics access, I have provided a sample of this data (about half of the samples and each sample cut off at 5000 bases) in the chr17 subfolder. Running Genomes.sh will call all the queries given a specific chromosome (this parameter is alterable at the top of the script). It is currently set to be a "dry-run" and will print all the queries without execution: uncommenting all commented lines will remove this behavior. 

Compression: These files will be called by main.py to run the compression algorithm on the dataset. Compress.py handles the full dataset compression, while Sequence.py considers the single sequence subproblem. 

Visualization: These files will be called by main.py to produce graphs from the pickled results.pkl file. There are two separate files: one to produce line graphs for the simulated data (across multiple levels), and one to produce bar graphs from the human genome data. 

Results: This directory contains an example of some of the graphs obtained when running this code on live human genome data, detailing the compression and running time statistics for both chromosome 3 and chromosome 17.  


Useful commands: 
1. ./Genomes.sh
If all lines are uncommented, this will pull genome data from the 1000 Genomes project. This requires a Google Cloud account and valid access. 

2. python processData.py file_of_data output_file
This processes the raw 1000 Genomes data and concatenates all the outputs into one gzipped data file for later use. This has already been done on the sample data.

3. python main.py
This will run the entire compression pipeline given some parameters specified in params.py. Please be patient - even on relatively small datasets, this may take some time. 

4. vim params.py
This file stores the parameters for the compression. The file itself gives further detail about what each parameters does and how they should be specified. 


Quick Start: Simply running "python main.py" will run the compression algorithm on a simulated dataset, and produce the output results and graph. Changing the "datatype" parameter in params.py will change the behavior of running "python main.py" to instead use the sample dataset as the underlying data for compression. 


Usage requirements: The source code only requires a Python 3 installalation (tested on Python 3.6) to be run. Packages Numpy, Matplotlib, and Pandas will need to installed. For small genome datasets, a simple computer will suffice (note that by default the Compress.py file will run on all available cores). For larger datasets, we recommend using large-scale computing options (Google Cloud was utilized in testing), and well as making use of the Python optimizer PyPy (see https://pypy.org/). A Google Genomics account as well as Google Cloud credit will be required to have access to the human genome data. 

Thanks! Please direct any questions or concerns to hn2261@columbia.edu. 
