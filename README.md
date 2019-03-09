# Deep Tweet

## Developement

```
pipenv install

pipenv run jupyter notebook
```

## Open Deepbird

Try to run the notebook `notebooks/DeepBird.ipynb`

Note the directory and edit `project_root` to your local path.

## Build splits

These splits will be used for training.

```
pipenv shell
mkdir data/samples/splits
. ./bin/split.py
```
