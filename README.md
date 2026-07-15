# Password Strength Classifier and Generator

Simple flask proj with ML technique to classify password strength, generate secure passwords like google engine, provide password improvement suggestions, calculate password entropy(not shown) & display live password metrics using chart

## Requirements

To run need these:

- **scikit-learn**
- **pandas**
- **numpy**
- **matplotlib**
- **seaborn**
- **flask**

**Note**: This app although is lightweight and runs completely on the CPU. This app may be slow on low-end computers, cause it used actual passwords large dataset and hence is computationally intensive. It does perform better on machine with GPU and more ram (8,16gb) instead of APU pc/laptop with 4gb ram. It trains a DT classifier when the application starts

### Installation

Just download, go inside the folder and run `python app.py`, but first run `pip install` for all above req packages install.





