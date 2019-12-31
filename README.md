# Arabidopsis.tf.pred
## Get started
### Requires
- [python](http://www.python.org/downloads/)>=3.5
- python modules: reference requirements.txt file

### Install
```
git clone git@github.com:liulifenyf/Arabidopsis.tf.pred.git

```

### How to use
```
python ./py/predict.py <InputFile>
```
your can also use 'python ./py/predict.py test.fa' command to view example.
### Input File
The input file must be DNA sequences which have a length of 210bp and a format in FASTA.
A FASTA sequence seems like below:
```
>chr2L:12715-12916
CAAAAATAGAAATACCCACCACAGGAGCACGATGTTTTAATTGTATTTCTTTAGCAAGCTGCGCAGAAATTCGGCGGGGCATGTGTGGTGGTGCATTGCCACTTGCCGACGGGACGGCAGTTGCCGCGGTCTGCGCTGGTGGCAAATGCAGAAGGAAAACCGAGACTGTACTGGCATTTGTTGCTGACCACAAAGTTGGCG
```
### Output File
According to the number of DNA sequences in your input file, our process will generate same number .csv files under "output" folder.the name of each file is the order of your DNA sequences.
Each file contains two columns, the first column is the name of the transposable factor, and the second column is the probability that the sequence is predicted to be the transposable factor, arranged in descending order.
It seems like below:
```
ERF7,0.9990957
AT1G71450,0.9990287
RAP2.11,0.99881834
RAP2.6,0.9987594000000001
CBF1,0.99839324
...

```
*** Attention: Because each prediction will cover last predicted result. In case of confusing, you'd better delete the "output" folder after you restoring the prediction result.

