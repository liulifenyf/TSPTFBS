# TSPTFBS
## Python programs for predicting TFBS for 265 Arabidopsis TFs
## Dependencies
The program requires:
  * python 3.6
  * tensorflow2.0.0 module
  * keras2.3.1 module
  * pandas module
  * numpy module
  * scikit-learn module
  * TAIR10 reference genome
  * the [bedtools](https://bedtools.readthedocs.io/en/latest/) software
## Install
```
git clone git@github.com:liulifenyf/TSPTFBS.git

```

## Tutorial
### Predicting
```
cd TSPTFBS
python Predict.py <input fasta file>
```
After running the program, a file named 'result.csv' will be generated in the current folder which records the prediction results of the models.
We here provide a Test.fa file for an example: 
```
python Predict.py Example/Test.fa
```
## Input File Format
The input file must contain DNA sequences which have a length of 201bp with a FASTA format.
A FASTA file of the example is:
```
>chr2L:12715-12916
CAAAAATAGAAATACCCACCACAGGAGCACGATGTTTTAATTGTATTTCTTTAGCAAGCTGCGCAGAAATTCGGCGGGGCATGTGTGGTGGTGCATTGCCACTTGCCGACGGGACGGCAGTTGCCGCGGTCTGCGCTGGTGGCAAATGCAGAAGGAAAACCGAGACTGTACTGGCATTTGTTGCTGACCACAAAGTTGGCG
>chr2L:59143-59344
TAGACCGCCTGACAAGTTCGGGTGACCATCGAGCGTCTCTGCTTACCGTGCGCTTAAGCGAACCACACGTCCTAATCGAAACAACTATACAGCGCGACTGTGCGGACGAGTGTCTTGAGACTCTGGGCAAGCGCAGCCAGCCAACCAAGTTTCGAAGTCTGGCTTTTGGGCCAAGCTTGGTCTGCGCCACGCTTGGCCCCG

```
## Output File Format
The output file will seem like below: the first column represents the names of 265 Arabidopsis TFs, the remaining columns (The example has two remaining columns because the input file has two enquired DNA sequences) record the probabilities of given DNA sequences to be predicted as a TFBS of one of 265 Arabidopsis TFs.
```
TF Name	chr2L:12715-12916	chr2L:59143-59344
AT3G10113	5.8268368E-05	0.00023753107
AT3G12130	0.0003848466	0.077134416
AT3G52440	0.6031477	0.42776716
AT3G12730	0.0059271543	0.03132692
AT3G60580	0.05004888	0.012927864
AT3G60490	0.86310613	0.8729982
AT4G00250	0.13277796	0.2112361
AT3G24120	0.011899605	0.052325442
AT3G09600	0.0072161327	0.016331125
...

```
