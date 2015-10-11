# Review6: Dr. Dam's Talk

+ What are predictive models?
Predictive models are machine learning algorithms trained on known data made up of a set of input vectors. 

+ What are rule based models?
A model that uses a set of rules to determine a prediction.
+ Define: 
1) Supervised learning
Applications of machine learning where the training data compromises input vectors and their corresponging target vectors(labels)
2) Features;
Input Vectors, attributes of an object used during training, independent variables
3) Dependent Variables.
Target variable, label, what we predict
+ In the following figure, label features and independent variables.
?
+ In a few lines, differentiate regression and classification.
Regression is used to predict some continuous value that can be expressed as a real number. Classification is used to predict some discrete value that can be expressed as finite or countably infinite. 
+ What is risk exposure? Give a mathematical expression to calculate it.
Risk exposure is the sum of weighted risk impact probabilities for a given class.
REi = C1P(i, Non) + C2)(i, Min) + C3P(i, Maj)
+ Sort the steps taken in predicting delays, as proposed by Dr. Hoa:
  1. Characterize the issues that  constitute delays.
  2. Extract Features, and select the ones that contribute to risk of delay.
  3. Train classifiers.
+ In the following figure label **A** and **B**:

Looks like this is answered.

![1](https://cloud.githubusercontent.com/assets/1433964/10259938/29db384a-693c-11e5-8163-69f25542da9a.png)

+ Define networked data
Data that can represented as graph of vertices and edges. In this specific case directed graphs to represent dependencies.
+ Briefly describe task networks
A directed graph where each vertex is a task and where each edge represents relationships between tasks.

+ Define: 
1) Explicit relationship
A relationship that is defined in the task record, typically the ordering of the tasks. Ex. Blocking
2) Implicit relationship (give an example)
Relationship a task has that can only be derived by using information from other tasks. ex. Resource-based relationship: tasks share the same human resource
3) Resourse based relationship
Above
4) Attribute based relationship
A relationship between tasks that shared the same attribute. If tasks are performed on the same component
5) Content based relationship
Similarity of task based on how they are conducted or what the affect.