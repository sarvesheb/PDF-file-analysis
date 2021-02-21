# Textual Analysis of Annual Reports PDFs

This is a Python program that helps perform textual analysis on a large volume of PDF files organized by company name and collects relevant data and presents the results in a compelling CSV format useful for statistical analysis or as training data. 

The application is designed to count the occurrences of certain words/phrases as well as of large groups of words/phrases.

##### The sample lists provided as an example use case for sentiment analysis has been obtained from [Loughran-McDonald Sentiment Wordlists](https://sraf.nd.edu/textual-analysis/resources/)

> *XPDF reader(open-source) application in the form of a x64 executable file is used for quick conversion of PDF to text* 

 > `Important note: The process of reading multiple PDF files utilizes parallel processing using Python threads which merely spawn the executable as individual ungrouped processes for the sake of efficiency and make use of multiple cores in the system`

## Requirements
```
filelock==3.0.12
```

## How to Use
<block>
  
*Organize the annual reports in PDFs in a folder structure such as `<Company name>/<year or any valid identifier>.pdf`*

For example, a company folder named "Microsoft" would contain the company's annual reports in PDF form and each PDF would be named by the year of publication, e.g. 2019.pdf.

Create files with the naming format `group_<name>.txt` and add necessary words inside it for getting a grouped output of the word count in the file.
Have a master word file with the name `words.txt` to determine the word count of the words in this file followed by the data specific to each individual filing type

Run the `run.py` file for starting the scraping the PDF content and gather relevant data according to the inputs provided in the aforementioned files
</block>

## Output
2 files are generated while running the `run.py` file

`data.csv`:
<block>
This file contains data in the format
  
`'Company', 'Year', 'Search Word', 'Occurrences','Total Words'`

`grouped_data.csv` contains data in this format

`'Company', 'Year', 'File Size(MB)', <names>(as mentioned in group_<name>.txt) , 'Total Words'`

## Program Author
### Sarvesh E B

## Project Conceptualization and Co-Authoring :

<block> 
 
### George Kladakis (Management School, University of Sheffield)
</block>




