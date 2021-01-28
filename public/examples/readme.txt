Contents
--------

*input

*results

#######################INPUT#########################

In the input download you will find a multiFASTA file with dot-bracket notation and BEAR alphabet representation for the secondary structure calculated using RNAfold tool from the ViennaRNA package(Lorenz et al., 2011).


#######################RESULTS#######################

In the results download you will find two folders: Logos and Motifs.

Logos:
------

-The logos folder contains al the Weblogos of the motifs that BRIO has found in the user input, structure motifs are in qBEAR alphabet, sequence motifs in IUPAC nucleic acid notation(logos have been generated using WebLogo (Crooks et al., 2004).


Motifs:
-------

-The motifs folder contains a text file for each motif found in the user's input by BRIO. Inside these files every row represent an occurrence of the motif in one of the input sequence/s.

Each column represent:
	
-the name of the input sequence where that particular motif was found; 	
-the representation of the motif in BEAR alphabet for structural motifs, or in IUPAC alphabet for sequence motifs;
-the BEAM (Pietrosanto et al., 2016) score obtained for the motif in the sequence (see http://beam.uniroma2.it or the BEAM article for more details);
-start and end position of the motif in that sequence;
-the BEAM score threshold used to select the motif.



--------------------------------------------------------------------------------------------------------------------------------

*Lorenz R, Bernhart S.H., Hoener zu Siederdissen C., Tafer H., Flamm C., Stadler P.F. and Hofacker I.L. (2011), "ViennaRNA Package 2.0", Algorithms for Molecular Biology: 6:26 
*Crooks, Gavin E., et al. "WebLogo: a sequence logo generator." Genome research 14.6 (2004): 1188-1190
*Pietrosanto,M., Mattei,E., Helmer-Citterich,M. and Ferrè,F. (2016) A novel method for the identification of conserved structural patterns in RNA: From small scale to high-throughput applications. Nucleic Acids Res., 44, 8600–8609.
