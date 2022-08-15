# ImmunIC
ImmunIC (Immune cell Identifier and Classifier) is a tool for immune cell identification and classificaiton from single cell RNA sequencing data. ImmunIC takes a single input of a gene count matrix to dentify immune cells and classify immune cells into B cells, plasma cells, CD4+ T cells, CD8+ T cells, NK cells, monocytes, dendritic cells, macrophages, neutrophils and other myeloid cells. ImmunIC uses the predetermined leukocyte gene signature matrix [LM22](https://www.nature.com/articles/nmeth.3337) along with [Xgboost](https://dl.acm.org/doi/10.1145/2939672.2939785). More details are provided in our publication.

## Example
An input example, pbmc_test.csv, is a raw gene count matrix of 10 peripheral blood mononuclear cells (PBMCs) ([GSE158055](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE158055)). The output is ImmunIC_pbmc_test.csv.

## Using Docker
The ImmunIC pipeline with all code requirements is provided as a [Docker file](https://github.com/hayounlee-lab/ImmunIC/blob/main/Dockerfile). 
``
docker build -t immunic:latest - < Dockerfile
``

After creating the Docker image, you can run ImmunIC with the following command:
``
docker run -v $(pwd):$(pwd) --rm immunic:latest $(pwd)/pbmc_test.csv
``
