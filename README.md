## How to use

You will need python3.6, virtualenv and pip

### Install

```bash
git clone https://github.com/Jean-Baptiste-Camps/willhelmus.git
cd willhelmus
virtualenv -p python3.6 env
source env/bin/activate
pip install -r requirements.txt
# And get the model for language prediction
mkdir jagen_will/preproc/models
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -P ./jagen_will/preproc/models/
```

## Workflow

FIXME: look inside the scripts, or do

```bash
python main.py --help
```

for full documentation on the CLI.

### Get feats

With or without preexisting feature list:

```bash
python main.py -t chars -n 3 -c debug_authors.csv [-p 1] -k 5000 -s path/to/docs/*
# with it
python main.py -f feature_list.json -t chars -n 3 -c debug_authors.csv -k 5000 -s meertens-song-collection-DH2019/train/*
```


### Do the split

If you want to do initial random split,
```bash
python split.py feats_tests.csv -m langcert_revised.csv -e wilhelmus_train.csv
```

If you want to split according to existing json file,
```bash
python split.py feats_tests.csv -s split.json
```

### Train svm

It's quite simple really,
```bash
python train_svm.py path-to-train-data.csv path-to-test-data.csv [--norms] [--dim_reduc None, 'pca', 'som'] [--kernel, 'LinearSVC', 'linear', 'polynomial', 'rbf', 'sigmoid'] [--final]
# e.g.
python train_svm.py data/feats_tests_train.csv data/feats_tests_valid.csv --norms --dim_reduc som
```


## Sources

### FastText models

## FastText

If you use these models, please cite the following papers:

[1] A. Joulin, E. Grave, P. Bojanowski, T. Mikolov, Bag of Tricks for Efficient Text Classification

@article{joulin2016bag,
  title={Bag of Tricks for Efficient Text Classification},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1607.01759},
  year={2016}
}

[2] A. Joulin, E. Grave, P. Bojanowski, M. Douze, H. Jégou, T. Mikolov, FastText.zip: Compressing text classification models

@article{joulin2016fasttext,
  title={FastText.zip: Compressing text classification models},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Douze, Matthijs and J{\'e}gou, H{\'e}rve and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1612.03651},
  year={2016}
}




