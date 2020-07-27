# Arabidopsis.tf.pred
## Python program for predicting TFBS for 265 TFs
This program allows for:
  1.Repeat Traning process of 265 TFs
  2.Predciting TFBS for given fasta file
### Dependencies
The program requires:
  * python 3.6
  * tensorflow2.0.0 module
  * keras2.3.1 module
  * pandas module
  * numpy module
  * scikit-learn module
  * TAIR10 reference genome
  * the [bedtools](https://bedtools.readthedocs.io/en/latest/) software
### Install
```
git clone git@github.com:liulifenyf/Arabidopsis.tf.pred.git

```

### Tutorial
## Training
By running the train.py process directly, ABF2 will be used as an example to run the training program and generate a folder for saving the newly trained model and training results.Modify the file path of TFBS in the training program to realize the training of another TF.
*** before training, remember to generate the fa file of TFs with bedtools.
## Predicting
```
cd Arabidopsis.tf.pred
python Predict.py <input fasta file>
```
After the program runs, a result.csv file will be generated in the current folder to record the prediction results of the models.
we provide a test.fa file for testing.
### input File
The uplode file must be DNA sequences which have a length of 201bp and a format in FASTA.
A FASTA sequence seems like below:
```
>chr2L:12715-12916
CAAAAATAGAAATACCCACCACAGGAGCACGATGTTTTAATTGTATTTCTTTAGCAAGCTGCGCAGAAATTCGGCGGGGCATGTGTGGTGGTGCATTGCCACTTGCCGACGGGACGGCAGTTGCCGCGGTCTGCGCTGGTGGCAAATGCAGAAGGAAAACCGAGACTGTACTGGCATTTGTTGCTGACCACAAAGTTGGCG
>chr2L:59143-59344
TAGACCGCCTGACAAGTTCGGGTGACCATCGAGCGTCTCTGCTTACCGTGCGCTTAAGCGAACCACACGTCCTAATCGAAACAACTATACAGCGCGACTGTGCGGACGAGTGTCTTGAGACTCTGGGCAAGCGCAGCCAGCCAACCAAGTTTCGAAGTCTGGCTTTTGGGCCAAGCTTGGTCTGCGCCACGCTTGGCCCCG

```
### Output File
The output file will seems like below, first column represents the name of TFs, follow columns are the probabilities of DNA sequence to be predicted as a TF binding site:
```
Factor Name	chr2L:12715-12916	chr2L:59143-59344
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
