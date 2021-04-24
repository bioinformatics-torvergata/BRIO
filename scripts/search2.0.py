#!/usr/bin/env python
# coding: utf-8

# libraries
import re
import argparse
import json

from exceptions import *

filtered_motifs_set = {
    'ENCFF121XLA_HNRNPA1_hg19_UTR_m1_run1.txt', 'ENCFF456SOS_UTP18_hg19_CDS_m2_run1.txt',
    'ENCFF756RYJ_AARS_hg19_UTR_m1_run1.txt', 'ENCFF545FMX_NPM1_hg19_UTR_m3_run1.txt',
    'ENCFF302FFF_LARP7_hg19_CDS_m1_run2.txt', 'ENCFF929AVT_ABCF1_hg19_UTR_m3_run1.txt',
    'ENCFF355WVE_HNRNPUL1_hg19_CDS_m1_run2.txt', 'ENCFF756RYJ_AARS_hg19_UTR_m3_run1.txt',
    'ENCFF656IDO_XRCC6_hg19_UTR_m2_run1.txt', 'ENCFF456SOS_UTP18_hg19_CDS_m1_run1.txt',
    'ENCFF124YKO_KHDRBS1_hg19_CDS_m3_run1.txt', 'ENCFF367VYJ_DDX42_hg19_CDS_m3_run1.txt',
    'ENCFF901ABJ_SUPV3L1_hg19_UTR_m1_run2.txt', 'ENCFF545FMX_NPM1_hg19_CDS_m3_run2.txt',
    'ENCFF842EFT_BCCIP_hg19_CDS_m2_run2.txt', 'ENCFF305BNZ_LARP7_hg19_UTR_m3_run2.txt',
    'ENCFF105PMR_SBDS_hg19_transcript_m3_run2.txt', 'ENCFF036IYW_NSUN2_hg19_UTR_m2_run2.txt',
    'ENCFF322GPD_SF3B1_hg19_UTR_m2_run2.txt', 'ENCFF322GPD_SF3B1_hg19_CDS_m1_run1.txt',
    'ENCFF955PCQ_HNRNPA1_hg19_CDS_m3_run2.txt', 'ENCFF565RQI_SSB_hg19_CDS_m1_run2.txt',
    'ENCFF545FMX_NPM1_hg19_CDS_m1_run1.txt', 'ENCFF469SRC_SAFB_hg19_CDS_m2_run2.txt',
    'ENCFF800GPC_DDX21_hg19_CDS_m1_run2.txt', 'ENCFF565RQI_SSB_hg19_UTR_m1_run2.txt',
    'ENCFF513PTZ_TAF15_hg19_CDS_m3_run2.txt', 'ENCFF854NXI_HNRNPU_hg19_UTR_m2_run1.txt',
    'ENCFF901ABJ_SUPV3L1_hg19_UTR_m3_run1.txt', 'ENCFF756RYJ_AARS_hg19_UTR_m2_run2.txt',
    'ENCFF153CMF_CPEB4_hg19_CDS_m2_run1.txt', 'ENCFF513PTZ_TAF15_hg19_CDS_m1_run1.txt',
    'ENCFF929AVT_ABCF1_hg19_UTR_m2_run1.txt', 'ENCFF929AVT_ABCF1_hg19_UTR_m1_run2.txt',
    'ENCFF656IDO_XRCC6_hg19_UTR_m3_run1.txt', 'ENCFF322GPD_SF3B1_hg19_UTR_m3_run1.txt',
    'ENCFF159HMF_HNRNPC_hg19_CDS_m1_run2.txt', 'ENCFF800GPC_DDX21_hg19_CDS_m2_run2.txt',
    'ENCFF469SRC_SAFB_hg19_CDS_m1_run2.txt', 'ENCFF324PNB_SSB_hg19_UTR_m1_run2.txt',
    'ENCFF513PTZ_TAF15_hg19_CDS_m2_run2.txt', 'ENCFF926QBW_UTP18_hg19_UTR_m3_run1.txt',
    'ENCFF305BNZ_LARP7_hg19_UTR_m2_run2.txt', 'ENCFF901ABJ_SUPV3L1_hg19_UTR_m2_run2.txt',
    'ENCFF955PCQ_HNRNPA1_hg19_CDS_m2_run1.txt', 'ENCFF159HMF_HNRNPC_hg19_CDS_m3_run2.txt',
    'ENCFF105PMR_SBDS_hg19_transcript_m2_run2.txt', 'ENCFF456SOS_UTP18_hg19_CDS_m3_run2.txt',
    'ENCFF803GSP_RPS11_hg19_CDS_m3_run2.txt', 'ENCFF153CMF_CPEB4_hg19_CDS_m3_run2.txt',
    'ENCFF565RQI_SSB_hg19_UTR_m2_run2.txt', 'ENCFF803GSP_RPS11_hg19_CDS_m1_run2.txt',
    'ENCFF324PNB_SSB_hg19_UTR_m2_run2.txt', 'ENCFF926QBW_UTP18_hg19_UTR_m2_run1.txt',
    'ENCFF121XLA_HNRNPA1_hg19_UTR_m2_run2.txt', 'ENCFF322GPD_SF3B1_hg19_UTR_m1_run1.txt',
    'ENCFF926QBW_UTP18_hg19_CDS_m2_run2.txt', 'ENCFF302FFF_LARP7_hg19_CDS_m2_run1.txt',
    'ENCFF153CMF_CPEB4_hg19_CDS_m1_run1.txt', 'ENCFF545FMX_NPM1_hg19_UTR_m2_run1.txt',
    'ENCFF355WVE_HNRNPUL1_hg19_CDS_m2_run2.txt', 'ENCFF803GSP_RPS11_hg19_CDS_m2_run1.txt',
    'ENCFF955PCQ_HNRNPA1_hg19_CDS_m1_run1.txt', 'ENCFF257KKQ_DDX52_hg19_CDS_m2_run2.txt',
    'ENCFF324PNB_SSB_hg19_UTR_m3_run2.txt', 'ENCFF565RQI_SSB_hg19_CDS_m3_run2.txt',
    'ENCFF036IYW_NSUN2_hg19_UTR_m3_run1.txt', 'ENCFF036IYW_NSUN2_hg19_CDS_m2_run2.txt',
    'ENCFF565RQI_SSB_hg19_CDS_m2_run1.txt', 'ENCFF469SRC_SAFB_hg19_CDS_m3_run1.txt',
    'ENCFF241KPE_SDAD1_hg19_CDS_m2_run1.txt', 'ENCFF124YKO_KHDRBS1_hg19_CDS_m1_run2.txt',
    'ENCFF121XLA_HNRNPA1_hg19_UTR_m3_run2.txt', 'ENCFF545FMX_NPM1_hg19_UTR_m1_run1.txt',
    'ENCFF036IYW_NSUN2_hg19_CDS_m3_run2.txt', 'PARCLIP_FMR1_Ascano2012c_hg19_UTR_m3_run1.nuc.txt',
    'PARCLIP_ELAVL1MNASE_hg19_UTR_m3_run1.nuc.txt',
    'PARCLIP_Ago2MNase_Kishore2011c_hg19_CDS_m3_run2.nuc.txt',
    'PARCLIP_AGO2_Gottwein2011a_hg19_CDS_m3_run2.nuc.txt',
    'PARCLIP_QKI_Hafner2010c_hg19_CDS_m3_run2.nuc.txt',
    'PARCLIP_ELAVL1_Lebedeva2011_hg19_UTR_m3_run2.nuc.txt',
    'PARCLIP_HuRMNase_Kishore2011f_hg19_UTR_m3_run1.nuc.txt',
    'PARCLIP_ELAVL1_stringent_Lebedeva2011_hg19_CDS_m2_run1.nuc.txt',
    'PARCLIP_AGO2_Gottwein2011b_hg19_CDS_m1_run1.nuc.txt',
    'PARCLIP_ZC3H7B_Baltz2012e_hg19_CDS_m2_run2.nuc.txt',
    'PARCLIP_EWSR1_Hoell2011b_hg19_CDS_m3_run2.nuc.txt',
    'PARCLIP_FXR1_Ascano2012e_hg19_CDS_m3_run2.nuc.txt',
    'PARCLIP_PUM2_Hafner2010b_hg19_UTR_m2_run1.nuc.txt',
    'PARCLIP_HuRMNase_Kishore2011f_hg19_CDS_m2_run2.nuc.txt',
    'PARCLIP_METTL3_Ping2014_hg19_CDS_m3_run2.nuc.txt',
    'PARCLIP_AGO2_Skalsky2012d_hg19_UTR_m3_run2.nuc.txt',
    'PARCLIP_FMR1_Ascano2012a_hg19_CDS_m3_run1.nuc.txt',
    'PARCLIP_LIN28B_Graf2013_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF956PEQ_PABPC4_hg19_UTR_m3_run2.nuc.txt', 'ENCFF075XTM_SDAD1_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF456SOS_UTP18_hg19_CDS_m3_run2.nuc.txt', 'ENCFF727XDH_DDX55_hg19_CDS_m1_run2.nuc.txt',
    'ENCFF302FFF_LARP7_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF934PXE_SAFB_hg19_transcript_m2_run1.nuc.txt', 'ENCFF565RQI_SSB_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF242FDW_UPF1_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF105AKX_HNRNPC_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF207UUG_ZC3H8_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF842EFT_BCCIP_hg19_CDS_m3_run2.nuc.txt', 'ENCFF265RIO_FASTKD2_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF470JIH_PUS1_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF514NWO_TROVE2_hg19_transcript_m1_run2.nuc.txt',
    'ENCFF363IJZ_FXR2_hg19_CDS_m2_run1.nuc.txt', 'ENCFF875QBF_GEMIN5_hg19_CDS_m1_run2.nuc.txt',
    'ENCFF756RYJ_AARS_hg19_UTR_m2_run2.nuc.txt', 'ENCFF075TIW_YBX3_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF470JIH_PUS1_hg19_transcript_m3_run2.nuc.txt', 'ENCFF400KYS_AQR_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF901ABJ_SUPV3L1_hg19_UTR_m1_run2.nuc.txt', 'ENCFF370GDB_ILF3_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF648LCX_EIF4G2_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF075TIW_YBX3_hg19_CDS_m3_run1.nuc.txt', 'ENCFF565BTR_METAP2_hg19_CDS_m2_run1.nuc.txt',
    'ENCFF540UOQ_LIN28B_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF241KPE_SDAD1_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF358QSY_WDR43_hg19_transcript_m3_run1.nuc.txt', 'ENCFF456CGG_SLBP_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF151HRC_NOLC1_hg19_CDS_m2_run1.nuc.txt', 'ENCFF331VCF_SND1_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF302FFF_LARP7_hg19_CDS_m3_run2.nuc.txt', 'ENCFF955PCQ_HNRNPA1_hg19_CDS_m2_run2.nuc.txt',
    'ENCFF546ZFM_MTPAP_hg19_CDS_m2_run1.nuc.txt', 'ENCFF233ZXV_DHX30_hg19_UTR_m3_run1.nuc.txt',
    'ENCFF440FET_XPO5_hg19_UTR_m3_run1.nuc.txt', 'ENCFF310NDD_FXR1_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF851FUY_XRN2_hg19_transcript_m3_run1.nuc.txt', 'ENCFF805LKH_SFPQ_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF241KPE_SDAD1_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF565RQI_SSB_hg19_transcript_m2_run2.nuc.txt', 'ENCFF530MIN_SRSF1_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF877QKG_TROVE2_hg19_transcript_m1_run2.nuc.txt',
    'ENCFF075XTM_SDAD1_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF485DDA_ILF3_hg19_transcript_m1_run2.nuc.txt',
    'ENCFF431FMQ_PCBP1_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF648LCX_EIF4G2_hg19_UTR_m1_run1.nuc.txt',
    'ENCFF159HMF_HNRNPC_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF736YDH_APOBEC3C_hg19_CDS_m1_run2.nuc.txt', 'ENCFF130JJX_EIF3D_hg19_CDS_m1_run1.nuc.txt',
    'ENCFF888SME_DDX52_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF878JOG_HNRNPM_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF105AKX_HNRNPC_hg19_UTR_m2_run1.nuc.txt', 'ENCFF357ABQ_FASTKD2_hg19_CDS_m2_run2.nuc.txt',
    'ENCFF928OEC_EIF3H_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF170SCU_PTBP1_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF579NNP_ZNF800_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF481RZR_NCBP2_hg19_transcript_m1_run1.nuc.txt', 'ENCFF969AOQ_PUM1_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF456CGG_SLBP_hg19_UTR_m1_run1.nuc.txt', 'ENCFF485KCC_PRPF4_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF075XTM_SDAD1_hg19_CDS_m2_run1.nuc.txt', 'ENCFF767LWE_PUM2_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF296JHG_HNRNPL_hg19_CDS_m2_run1.nuc.txt', 'ENCFF101EKG_SND1_hg19_CDS_m2_run1.nuc.txt',
    'ENCFF717EQF_XRN2_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF154DRN_RBFOX2_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF322GPD_SF3B1_hg19_CDS_m3_run1.nuc.txt', 'ENCFF934PXE_SAFB_hg19_UTR_m3_run1.nuc.txt',
    'ENCFF637JMJ_LSM11_hg19_UTR_m2_run2.nuc.txt', 'ENCFF305BNZ_LARP7_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF101EKG_SND1_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF159HMF_HNRNPC_hg19_UTR_m2_run1.nuc.txt', 'ENCFF713QGM_GRWD1_hg19_CDS_m2_run2.nuc.txt',
    'ENCFF456CGG_SLBP_hg19_UTR_m2_run1.nuc.txt', 'ENCFF617LAH_AGGF1_hg19_UTR_m1_run2.nuc.txt',
    'ENCFF302FFF_LARP7_hg19_UTR_m1_run1.nuc.txt', 'ENCFF400KYS_AQR_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF296JHG_HNRNPL_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF121XLA_HNRNPA1_hg19_UTR_m2_run1.nuc.txt', 'ENCFF889CCS_GPKOW_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF322GPD_SF3B1_hg19_UTR_m3_run2.nuc.txt', 'ENCFF890KEE_HNRNPL_hg19_UTR_m2_run2.nuc.txt',
    'ENCFF955PCQ_HNRNPA1_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF926QBW_UTP18_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF854NXI_HNRNPU_hg19_UTR_m2_run1.nuc.txt', 'ENCFF700XBC_FMR1_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF485DDA_ILF3_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF955PCQ_HNRNPA1_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF565BTR_METAP2_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF565RQI_SSB_hg19_transcript_m3_run2.nuc.txt', 'ENCFF656IDO_XRCC6_hg19_UTR_m3_run1.nuc.txt',
    'ENCFF039FGP_RBM22_hg19_CDS_m2_run2.nuc.txt', 'ENCFF105AKX_HNRNPC_hg19_CDS_m1_run2.nuc.txt',
    'ENCFF151ZTH_AKAP1_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF310NDD_FXR1_hg19_transcript_m2_run1.nuc.txt', 'ENCFF149CJJ_FXR2_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF890NIT_EWSR1_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF929AVT_ABCF1_hg19_CDS_m3_run2.nuc.txt', 'ENCFF792WPY_DDX24_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF311TOZ_IGF2BP3_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF832JDM_UTP3_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF105PMR_SBDS_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF400KYS_AQR_hg19_transcript_m2_run2.nuc.txt', 'ENCFF146YPF_DDX51_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF693EMF_SMNDC1_hg19_CDS_m3_run2.nuc.txt', 'ENCFF101EKG_SND1_hg19_UTR_m2_run2.nuc.txt',
    'ENCFF969AOQ_PUM1_hg19_UTR_m3_run2.nuc.txt', 'ENCFF004IIT_TRA2A_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF963CVD_G3BP1_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF305BNZ_LARP7_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF311TOZ_IGF2BP3_hg19_CDS_m2_run2.nuc.txt', 'ENCFF713QGM_GRWD1_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF822NMS_DDX55_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF956PEQ_PABPC4_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF510KUY_SUB1_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF322GPD_SF3B1_hg19_transcript_m2_run2.nuc.txt', 'ENCFF756RYJ_AARS_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF241KPE_SDAD1_hg19_CDS_m1_run2.nuc.txt',
    'ENCFF651CNX_BUD13_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF257KKQ_DDX52_hg19_CDS_m1_run2.nuc.txt',
    'ENCFF792WPY_DDX24_hg19_transcript_m1_run1.nuc.txt', 'ENCFF002FLD_DKC1_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF298YFY_MATR3_hg19_CDS_m2_run1.nuc.txt', 'ENCFF284MRX_PPIG_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF877QKG_TROVE2_hg19_CDS_m3_run2.nuc.txt', 'ENCFF527BMM_RBM15_hg19_CDS_m2_run2.nuc.txt',
    'ENCFF222ULF_CSTF2_hg19_UTR_m3_run1.nuc.txt', 'ENCFF693EMF_SMNDC1_hg19_UTR_m2_run2.nuc.txt',
    'ENCFF151ZTH_AKAP1_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF546EKR_PPIL4_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF800GPC_DDX21_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF305BNZ_LARP7_hg19_transcript_m1_run1.nuc.txt', 'ENCFF514KIW_AATF_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF047PZR_NOL12_hg19_CDS_m2_run1.nuc.txt',
    'ENCFF302FFF_LARP7_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF014MZO_POLR2G_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF575BCP_AKAP1_hg19_UTR_m3_run2.nuc.txt', 'ENCFF741FRL_FAM120A_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF131ZWK_TAF15_hg19_CDS_m3_run2.nuc.txt', 'ENCFF805LKH_SFPQ_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF169SMQ_AGGF1_hg19_transcript_m1_run2.nuc.txt',
    'ENCFF207UUG_ZC3H8_hg19_CDS_m3_run2.nuc.txt', 'ENCFF777FHS_FUS_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF530MIN_SRSF1_hg19_transcript_m3_run1.nuc.txt', 'ENCFF623DVN_HLTF_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF949RPR_PRPF8_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF930HHV_BCLAF1_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF598NYT_FUBP3_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF257KKQ_DDX52_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF924CZR_PTBP1_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF553APP_KHSRP_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF871BYW_KHSRP_hg19_CDS_m2_run1.nuc.txt', 'ENCFF955VYD_NIP7_hg19_CDS_m3_run2.nuc.txt',
    'ENCFF456PLF_NCBP2_hg19_CDS_m1_run2.nuc.txt',
    'ENCFF449ZHX_SRSF7_hg19_transcript_m2_run2.nuc.txt', 'ENCFF410XHF_HLTF_hg19_UTR_m3_run2.nuc.txt',
    'ENCFF926QBW_UTP18_hg19_UTR_m2_run1.nuc.txt', 'ENCFF832JDM_UTP3_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF159HMF_HNRNPC_hg19_transcript_m1_run1.nuc.txt',
    'ENCFF546EKR_PPIL4_hg19_CDS_m3_run2.nuc.txt', 'ENCFF075TIW_YBX3_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF565RQI_SSB_hg19_transcript_m1_run2.nuc.txt', 'ENCFF146YIO_GRWD1_hg19_UTR_m2_run2.nuc.txt',
    'ENCFF146YPF_DDX51_hg19_CDS_m1_run2.nuc.txt', 'ENCFF854NXI_HNRNPU_hg19_UTR_m1_run1.nuc.txt',
    'ENCFF567MGK_YBX3_hg19_transcript_m3_run1.nuc.txt',
    'ENCFF368MXJ_FAM120A_hg19_UTR_m2_run2.nuc.txt', 'ENCFF938JQE_WRN_hg19_UTR_m3_run1.nuc.txt',
    'ENCFF793EJK_ZNF800_hg19_UTR_m3_run2.nuc.txt', 'ENCFF103XLC_GRSF1_hg19_UTR_m2_run2.nuc.txt',
    'ENCFF445CGF_QKI_hg19_CDS_m3_run2.nuc.txt', 'ENCFF865SCT_PRPF8_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF923ZLX_AKAP8L_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF080PGT_BUD13_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF103XLC_GRSF1_hg19_transcript_m2_run1.nuc.txt',
    'ENCFF945YRD_CSTF2T_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF215XPR_WDR3_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF391KVJ_UCHL5_hg19_transcript_m3_run2.nuc.txt',
    'ENCFF977MKB_IGF2BP2_hg19_CDS_m3_run1.nuc.txt',
    'ENCFF565BTR_METAP2_hg19_transcript_m2_run2.nuc.txt',
    'ENCFF263BIJ_LARP4_hg19_CDS_m2_run2.nuc.txt', 'ENCFF355WVE_HNRNPUL1_hg19_UTR_m2_run1.nuc.txt',
    'ENCFF215XPR_WDR3_hg19_transcript_m1_run1.nuc.txt', 'ENCFF865SCT_PRPF8_hg19_CDS_m2_run1.nuc.txt',
    'ENCFF530MIN_SRSF1_hg19_transcript_m1_run2.nuc.txt',
    'ENCFF788LMZ_STAU2_hg19_CDS_m3_run2.nuc.txt',
    'HITSCLIP_EWSR1_Paronetto2014_hg19_UTR_m1_run2.nuc.txt',
    'HITSCLIP_FOX2_Yeo2009_hg19_UTR_m3_run1.nuc.txt',
    'HITSCLIP_FUS_Nakaya2013e_hg19_UTR_m2_run2.nuc.txt',
    'HITSCLIP_AGO2_Karginov2013b_hg19_CDS_m3_run1.nuc.txt',
    'HITSCLIP_FOX2_Yeo2009_hg19_CDS_m3_run1.nuc.txt',
    'HITSCLIP_HNRNPL_Shankarling2014c_hg19_UTR_m3_run1.nuc.txt',
    'HITSCLIP_EIF4A3_Sauliere2012a_hg19_CDS_m3_run1.nuc.txt',
    'HITSCLIP_LIN28A_Wilbert2012b_hg19_CDS_m2_run1.nuc.txt',
    'CLIPSeq_HuR_Kishore2011d_hg19_CDS_m3_run1.nuc.txt',
    'HITSCLIP_HNRNPL_Shankarling2014a_hg19_CDS_m2_run1.nuc.txt',
    'HITSCLIP_HNRNPL_Shankarling2014b_hg19_transcript_m3_run2.nuc.txt',
    'HITSCLIP_AGO2_Karginov2013b_hg19_CDS_m1_run2.nuc.txt',
    'HITSCLIP_AGO2_Karginov2013c_hg19_UTR_m3_run1.nuc.txt',
    'CLIPSeq_Ago2_Kishore2011a_hg19_CDS_m3_run2.nuc.txt',
    'HITSCLIP_AGO2_Haecker2012b_hg19_CDS_m3_run2.nuc.txt',
    'HITSCLIP_AGO2_Haecker2012a_hg19_CDS_m2_run1.nuc.txt',
    'HITSCLIP_HNRNPL_Shankarling2014a_hg19_transcript_m1_run1.nuc.txt',
    'HITSCLIP_HNRNPL_Shankarling2014d_hg19_UTR_m3_run2.nuc.txt',
    'HITSCLIP_DGCR8_Macias2012c_hg19_CDS_m1_run1.nuc.txt',
    'CLIPSeq_Ago2_Leung2011b_mm9_UTR_m2_run2.nuc.txt',
    'HITSCLIP_Mbnl1_Wang2012d_mm9_CDS_m3_run2.nuc.txt',
    'HITSCLIP_TDP-43_Polymenidou2011_mm9_UTR_m1_run2.nuc.txt',
    'CLIPSeq_LIN28_Cho2012b_mm9_UTR_m3_run2.nuc.txt',
    'HITSCLIP_Nova_Zhang2011b_mm9_CDS_m3_run2.nuc.txt'}

# paths
mbr_path = "resources/MBR.tsv"

# argparse
parser = argparse.ArgumentParser(description='Look for motifs in database of motif PFMs')

parser.add_argument('--input', '-i', dest='inputFile', action='store',
                    help='input multiFasta with BEAR notation')
parser.add_argument('--motifs', '-m', dest='motifsFile', action='store',
                    help='target motifs file')
parser.add_argument('--sequence', dest='seqFlag', action='store_true',
                    help='for running the search on sequences instead of structures')
parser.add_argument('--min-seq-len', dest='minSeqLen', action='store', default=3,
                    help='minimum sequence length to consider')
parser.add_argument('--output', '-o', dest='output', action='store', default="stdout",
                    help='output file. Default: stdout')
args = parser.parse_args()


def parse_input(inputpath, min_seq_len):
    seqs = {}
    seq_regex = re.compile("^[ACGTUacgtu]+$")
    db_regex = re.compile("^[\(\)\.]+$")
    counter = 0
    with open(inputpath) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                # new sequence

                if counter > 0 and len(seq) >= min_seq_len:
                    # Save the previous sequence
                    seqs[name] = {'seq': seq, 'db': db, 'bear': bear, 'counter': counter}

                name = line.strip().lstrip('>')
                seq = ""
                db = ""
                bear = ""

                counter += 1
            elif seq_regex.match(line):
                seq += line
            elif db_regex.match(line):
                db += line
            else:
                # let's avoid a bear string regex
                bear += line

        # Last sequence
        if counter > 0 and len(seq) >= min_seq_len:
            seqs[name] = {'seq': seq, 'db': db, 'bear': bear, 'counter': counter}

    return seqs


def parse_motif(motifpath, seq_flag=False):
    if seq_flag:
        token = "#NT"
        antitoken = "#BEAR"
    else:
        token = "#BEAR"
        antitoken = "#NT"

    motif_info = {}
    with open(motifpath) as f:
        line = f.readline()
        while line:
            if line.startswith("#NAME"):
                name = f.readline().strip()

                if name in filtered_motifs_set:
                    continue

                motif_info[name] = {}
            if line.startswith(antitoken):
                raise MotifGroupError("The parameters and the motif file specified do not match!")
            if line.startswith(token):
                """get threshold score"""
                line = f.readline()
                thr = 9999
                while line and line != "\n":
                    current_score = float(line.split()[5])
                    if current_score < thr:
                        thr = current_score
                    line = f.readline()

                if name in filtered_motifs_set:
                    continue
                motif_info[name]['thr'] = thr

            if line.startswith("#PSSM"):
                line = f.readline()
                vals = []
                while line and line != "\n":
                    row = line.strip().split("\t")
                    vals.append({
                        pair[0]: float(pair[1:].split(":")[1].strip()) for pair in row
                    })
                    line = f.readline()

                if name in filtered_motifs_set:
                    continue
                motif_info[name]['PSSM'] = vals

            line = f.readline()

    return motif_info


def read_MBR(mbr_path):
    mbr_dict = {}
    with open(mbr_path) as f:
        header_list = f.readline().rstrip().split('\t')[1:]

        for line in f:
            splitted = line.strip().split('\t')

            mbr_dict[splitted[0]] = {char: float(score) for char, score in zip(header_list, splitted[1:])}

    return mbr_dict


def compare(rna, motifs, mbr_dict, seq_flag=False):
    """
    Scores one RNA against all motifs
    rna: string (primary sequence or bear string)
    motifs: dictionary -- motifs[name][thr and PSSM]
    """

    results = {}
    for motif_name, info_motif in motifs.items():
        motif_size = len(info_motif['PSSM'])
        best_score, position = score(rna, info_motif['PSSM'], motif_size, mbr_dict, seq_flag)

        if position >= 0:
            results[motif_name] = (best_score, info_motif['thr'], position, motif_size)

    return results


def score(rna, pssm, motif_size, mbr_dict, seq_flag=False, match=3, mismatch=-2):
    """
    tests all possible ungapped alignments
    """

    best_score = -9999
    position = -1
    rna_len = len(rna)
    if rna_len >= motif_size:
        for start in range(0, rna_len - motif_size + 1):
            slice_score = 0.0
            for b_rna, b_dict in zip(rna[start:(start + motif_size)], pssm):
                position_score = 0.0

                # frequency * subs(i,j)
                if not seq_flag:
                    mbr_row_dict = mbr_dict[b_rna]

                    for b_char, sos_score in b_dict.items():
                        position_score += sos_score * mbr_row_dict[b_char]
                else:
                    for b_char, sos_score in b_dict.items():
                        position_score += sos_score * (match if b_char == b_rna else mismatch)

                slice_score += position_score

            if slice_score > best_score:
                best_score = slice_score
                position = start
    # else:
    #    for start in range(0, motif_size - rna_len + 1):
    #        slice_score = 0.0
    #        for b_rna, b_list in zip(rna, pssm[start:(start + rna_len)]):
    #            index_b_rna = bear_dict[b_rna]
    #
    #            position_score = 0.0
    #            for b_char in b_list:
    #                # frequency * subs(i,j)
    #                if not seq_flag:
    #                    position_score += b_list[b_char] * mbr[bear_dict[b_char], index_b_rna]
    #                else:
    #                    position_score += b_list[b_char] * (match if b_char == b_rna else mismatch)
    #
    #            slice_score += position_score
    #
    #        if slice_score > best_score:
    #            best_score = slice_score
    #            position = start

    return best_score, position


seqs = parse_input(args.inputFile, int(args.minSeqLen))
motifs = parse_motif(args.motifsFile, args.seqFlag)
# print(seqs)
# print(motifs)

string_to_align = 'seq' if args.seqFlag else 'bear'

mbr_np = read_MBR(mbr_path)

seq_to_result = {}

for seq_name, info in seqs.items():
    seq_to_result[seq_name] = compare(info[string_to_align], motifs, mbr_np, args.seqFlag)

if args.output == 'stdout':
    json.dump(seq_to_result, sys.stdout)
else:
    with open(args.output, 'w') as f:
        json.dump(seq_to_result, f)
