Contents
--------

- input.txt: the input sequences file with dot-bracket notation and BEAR alphabet representation for the secondary
             structure calculated using RNAfold tool from the ViennaRNA package(Lorenz et al., 2011).

- logo/:     this folder contains all the Weblogos of the motifs that BRIO has found in the input sequences. The structure
             motifs are in qBEAR alphabet, the sequence motifs in IUPAC nucleic acid notation. The Weblogos have been
             generated using WebLogo (Crooks et al., 2004).

- motifs/:   this foolder contains a text file for each motif found in the input sequences.
             In each file, every row represents the occurrence of the motif in one of the input sequence/s. In particular,
             each column represents:
             - the name of the input sequence where that particular motif was found;
             - the representation of the motif in BEAR alphabet for structural motifs, or in IUPAC alphabet for sequence motifs;
             - the BEAM (Pietrosanto et al., 2016) score obtained for the motif in the sequence (see http://beam.uniroma2.it for more details);
             - the start and end position of the motif in that sequence;
             - the BEAM score threshold used to select the motif.


References
* Lorenz R, Bernhart S.H., Hoener zu Siederdissen C., Tafer H., Flamm C., Stadler P.F. and Hofacker I.L. (2011), "ViennaRNA Package 2.0", Algorithms for Molecular Biology: 6:26
* Crooks, Gavin E., et al. "WebLogo: a sequence logo generator." Genome research 14.6 (2004): 1188-1190
* Pietrosanto,M., Mattei,E., Helmer-Citterich,M. and Ferrè,F. (2016) A novel method for the identification of conserved structural patterns in RNA: From small scale to high-throughput applications. Nucleic Acids Res., 44, 8600–8609.
