# time-series

## Projeto Overleaf 
Link para o documento overleaf [aqui](https://www.overleaf.com/project/64e78ba37aa9b5fdc1d32924)

### Perguntas iniciais
Link para as perguntas que definimos [aqui](https://docs.google.com/document/d/1v93sjYmrPYgMzPrnQ7Q3mDkyt3Dhk47OS50PK2EPxwc/edit)

## Instruções para rodar o MVP do projeto 

Siga as instruções abaixo para rodar o MVP de dashboard na sua máquina 

## Setup 
--- 

### 1. **Install Python** 
  [Install](https://www.python.org/downloads/) python3 
  
### 2. **Clone this repo with**
`git clone https://github.com/heitortanoue/time-series`
  
### 3. **Setup a virtual environment with venv** 
   Go to the folder python: `cd .\python`
   
   Create the venv: `python -m venv env` 
   
   Go to the venv folder `cd .\env\` 
   
   Activate the environment `.\Scripts\activate` 
   
### 3. **Install requirements** 

Run the following command to install the project's required libraries 

`cd ..`

`python -m pip install -r requirements.txt`

### 4. **Start the app** 

Go to the project folder `cd .\streamlit`

Run `streamlit run .\0_👋_Introdução.py` to run the app locally 