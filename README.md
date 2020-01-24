# Google Hashcode 2019

this repo contains my improvements on the solution we submitted for the extended round of google hashcode 2019.

|extended round score|top score|
|-:|-:|
| 796.086 | 1.271.117

|file|score|my score |
|-:|:-|:-|
|input1|21081|109359|
|input2|1416|1749|
|input3|412436|387601|
|input4|361153|495386|

## Usage

`cd` to project root and run:

```bash
pipenv install --dev # to install dependencies

python -m solver /in/file.ext WINDOW_SIZE
```

where WINDOW_SIZE is the sliding window size. If it's bigger than the dataset, it runs the full O(N^2) algorithm
