# Getting-Started
The point of this simple application is to represent the usage of the [UStar](https://github.com/Moeed1mdnzh/UStar) model which generates unreal stars from only your simple paintings.This GUI provides you a basic paint-like environment wanting you to draw a simple painting to be transformed to an imaginary star.
|Input|Output|
|-------------|-------------|
![](https://github.com/Moeed1mdnzh/UStar-GUI/blob/master/images/input_1.jpg)|![](https://github.com/Moeed1mdnzh/UStar-GUI/blob/master/images/result_1.jpg)
![](https://github.com/Moeed1mdnzh/UStar-GUI/blob/master/images/input_2.jpg)|![](https://github.com/Moeed1mdnzh/UStar-GUI/blob/master/images/result_2.jpg)
![](https://github.com/Moeed1mdnzh/UStar-GUI/blob/master/images/input_3.jpg)|![](https://github.com/Moeed1mdnzh/UStar-GUI/blob/master/images/result_3.jpg)

*Examples of the performance of the model*<br /><br />
The quality of the results aren't the best but they'll be improved in the upcoming updates to the model.

## Installation
Clone this repository using <br />
`git clone https://github.com/Moeed1mdnzh/UStar-GUI.git`<br />
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
# Guideline
Once you've completed the previous steps, you should then be able to face such screen
![](https://github.com/Moeed1mdnzh/UStar-GUI/blob/master/images/screen.PNG)
<br />
You are provided with both a color picker and sliders for accurate rgb values to paint with but you'd get warned if you use dark colors as 
it is said why in the **Notes** section(Next section).The pen size slider, brush and eraser options are obvious and the **C** option is used to reset
everything.Once you are done with your painting, press generate to be navigated to the next screen(It may take some time to generate your image depending
on your GPU and CPU).

![](https://github.com/Moeed1mdnzh/UStar-GUI/blob/master/images/result_screen.PNG)
<br />
Now you are given your unreal star.You can save the result and painting using the save button as it will be saved in a new directory in the project directory
named as **result** or you can simply press return to draw another star.

# Notes
Here are a couple of things you need to keep in mind when using this app
## Multi-Attributes
The model has the capability to generate stars with various colors together and sizes.
## Lighting
The model is sensitive to darker colors as dark stars don't make much sense in real life so you had better consider using bright colors(Not pure white).
