# CpPy

A simple command line encounter difficulty calculator written in python.

```bash
Usage: main.py [OPTIONS]

Options:
  --party TEXT     The level of each party member, comma-separated.
  --monsters TEXT  The count and CR values for each monster, as n@CR.
  --help           Show this message and exit.

```

For example, running:

```bash
> python main.py --party 1,2,1,2 --monsters 2@1/2
```

would result in: 

```bash
MEDIUM
```

Denoting that for a 4-PC party of levels 1 & 2, against two CR-1/2 monsters, the encounter would be of 
MEDIUM difficulty.