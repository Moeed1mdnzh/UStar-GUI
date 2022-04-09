# Getting-Started
The point of this simple application is to represent the usage of the [UStar](https://github.com/Moeed1mdnzh/UStar) model which generates unreal stars from only your simple paintings.This GUI provides you a basic paint-like environment wanting you to draw a simple painting to be transformed to a imaginary star.

## Installation
Clone this repository using <br />
`git clone https://github.com/Moeed1mdnzh/UStar-GUI`<br />
And next install the required libraries using
```python
pip install -r requirements.txt 
``` 
The tensorflow framework isn't mentioned in the requirements file since CUDA and cuDNN installation is required along it as well which you should consider installing
separately.
## Running
The process of running the program is as simple as a piece of cake.As you're already in the project directory, simply run the main file using the following command
```python
python run.py
```
# Note
Here are a couple of things you need to keep in mind when using this app
## Multi-Attributes
The model has the capability to generate stars with various colors together and sizes.
## Lighting
The model is sensitive to darker colors as dark stars don't make much sense in real life so you had better consider using bright colors(Not pure white).
