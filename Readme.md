# flie-PSL

flie-PSL is a tool that learns a [PSL formula](https://en.wikipedia.org/wiki/Property_Specification_Language) consistent a given sample S = (P, N) consisting of positive and negative traces.
The method used for solving the learning problem can be found in [this](https://arxiv.org/abs/2002.03668) paper.

## Setup

- For installing and activating virtual environment venv, run 

```
vitualenv -p python3 venv
source venv/bin/activate
```

- For installing necessary python packages, run 
``
pip install -r requirements.txt
`` 


## Running

For running flie-PSL, run `python run_tests.py`. By default, this runs flie-PSL on a trace `allSamples/dummy.trace`
This command can, also, take the arguments listed in the table below.


|Argument        |Meaning
|----------------|------------------------------
|-t \<filename>| For specifying the path of the trace file on which the PSL learner is applied.
|-tf \<foldername>|For specifying the folder containing  the trace files on which the PSL learner is applied.
|-d\<maxdepth> | For specifying the maximum depth of the output formulas
|-rd<maxregexdepth>| For specifying the maximum depth of the regular expressions in the output formulas
|-o<outputfilename>| For specifying the name of the output csv file
|-f| Specify this option if the traces are of finite length 
|-h| Outputs the help.


### Experiment Trace File Format
Experiment traces file consists of accepted traces and rejected traces, separated by `---`


An example infinite trace looks like this
`1,1;1,0;0,1::1` and means that there are two variables (`x0` and `x1`) whose values in different timesteps are
 - x0 : 1,(1,0)*  
 - x1: 1,(0,1)*

 The value after separator `::` denotes the start of lasso that is being repeated forever. If it is missing, it assumes that the whole sequence is repeated indefinitely.
 
 A finite trace also looks the same (eg. `1,1;1,0;0,1`), but without the separator and the lasso.
