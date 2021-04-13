Contents
--------

- input.txt: the input RNA sequences, plus their dot-bracket and BEAR (Mattei et al., 2014) representation for the secondary structure.

- tab_enriched_motifs.txt: this file contains the information present in the "Enriched Motifs" table of the output page, where each tab-separated column represents:
    - the logo of the motif in the qBEAR alphabet for structure motifs or in IUPAC nucleic acid notation for sequence motifs;
    - the type of the motif: sequence or structure;
    - the type of mapping regions from GENCODE annotation of the RNAs datasets where the motif was originally found. The annotation includes UTR, CDS, and the entire transcript for those involving RBPs known to act in the nucleus on unspliced RNAs;
    - the coverage, which represents the number of input RNA molecules in which the motif is identified divided by the total number of query molecules;
    - the one-sided Fisher’s Test p-value;
    - the type of the experiment;
    - the protein associated with the RNA sequence or secondary structure motif in the CLIP experiment analyzed in Adinolfi et al.;
    - the protein domain associated with the RNA secondary structure motif (this information is not always available);
    - the cellular line used in the eCLIP experiments;
    - the link to the experiment page (for eCLIP data), or to the corresponding paper for PAR-CLIP and HITS data);
    - the organism in which the experiment was performed (Homo sapiens or Mus musculus).

tab_sequences.txt: this file contains the information present in the "Sequences" table of the output page, where each tab-separated column represents:
    - the start and the end position of the motif in the selected sequence;
    - the representation of the motif in BEAR alphabet for structure motifs or in IUPAC nucleic acid notation for sequence motifs;
    - the type of the motif: sequence or structure;
    - the protein associated with the RNA sequence or secondary structure motif in the experiments analyzed by Adinolfi et al.;
    - the type of the experiment (PAR-CLIP, eCLIP, HITS).

- "logos" folder: this folder contains all the Weblogos of the motifs that BRIO has found in the input RNA sequences. The
    structure motifs are in qBEAR alphabet, the sequence motifs in IUPAC nucleic acid notation. All Weblogos have been generated using WebLogo (Crooks et al., 2004).

- "motifs" folder: this folder contains a text file for each motif found enriched in the input RNA sequences.
    In each file, every row represent an occurrence of the motif in one of the input sequence/s. In particular, each column represents:
    - the name of the input sequence where that particular motif was found;
    - the representation of the motif in BEAR alphabet for structural motifs, or in IUPAC alphabet for sequence motifs;
    - the BEAM (Pietrosanto et al., 2016) score obtained for the motif in the sequence (see http://beam.uniroma2.it or the BEAM paper for more details);
    - start and end position of the motif in that sequence;
    - the BEAM score threshold used to select the motif.


Bibliography
* Mattei,E., Ausiello,G., Ferrè,F. and Helmer-Citterich,M. (2014) A novel approach to represent and compare RNA secondary structures. Nucleic Acids Res., 42, 6146–6157.
* Crooks, Gavin E., et al. "WebLogo: a sequence logo generator." Genome research 14.6 (2004): 1188-1190
* Pietrosanto,M., Mattei,E., Helmer-Citterich,M. and Ferrè,F. (2016) A novel method for the identification of conserved structural patterns in RNA: From small scale to high-throughput applications. Nucleic Acids Res., 44, 8600–8609.
* Adinolfi,M., Pietrosanto,M., Parca,L., Ausiello,G., Ferrè,F. and Helmer-Citterich,M. (2019) Discovering sequence and structure landscapes in RNA interaction motifs. Nucleic Acids Res., 47, 4958–4969.
