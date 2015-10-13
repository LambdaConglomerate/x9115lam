# Review6: Dr. Dam's Talk

+ What are predictive models?
Predictive models are machine learning algorithms trained on known data made up of a set of input vectors. 

+ What are rule based models?
A model that uses a set of rules to determine a prediction.  A modeling approach that uses a set of rules that indirectly specifices a a model.  Dr. Hoa mentioned that they were difficult to maintain.
+ Define: 
+ 1) **Supervised learning**
Applications of machine learning where the training data compromises input vectors and their corresponging target vectors(labels)
+ 2) **Features**
Input Vectors, attributes of an object used during training, independent variables
+ 3) **Dependent Variables.**
Target variable, label, what we predict
+ In the following figure, label features and independent variables.
+ features/independent variables = outlook, temp, humidity, windy
![image](https://cloud.githubusercontent.com/assets/1433964/10419861/9b895770-7052-11e5-9fed-77c53a922a20.png)

+ In a few lines, differentiate regression and classification.
Regression is used to predict some continuous value that can be expressed as a real number. Classification is used to predict some discrete value that can be expressed as finite or countably infinite. 
A few nice answers to this can be found [here](http://math.stackexchange.com/questions/141381/regression-vs-classification), similar to the above though.
Regression: the output variable takes continuous values.
Classification: the output variable takes class labels.
Regression involves estimating or predicting a response. 
Classification is identifying group membership.

+ What is risk exposure? Give a mathematical expression to calculate it.
Risk exposure is the sum of weighted risk impact probabilities for a given class.
REi = C1P(i, Non) + C2)(i, Min) + C3P(i, Maj)
Risk impact = degree of delay measured in (non,min,maj)

+ Sort the steps taken in predicting delays, as proposed by Dr. Hoa:
  1. Characterize the issues that  constitute delays.
  2. Extract Features, and select the ones that contribute to risk of delay.
  3. Train classifiers.
+ In the following figure label **A** and **B**:

~~Looks like this is answered.~~  I think they want to know terms which describe A and B. I said that A describes precision and B describes recall. (wumpafruit)

![1](https://cloud.githubusercontent.com/assets/1433964/10259938/29db384a-693c-11e5-8163-69f25542da9a.png)

+ Define networked data
+ Data that can represented as graph of vertices and edges. In this specific case directed graphs to represent dependencies.
+ Briefly describe task networks
+ A directed graph where each vertex is a task and where each edge represents relationships between tasks.

+ Define: 
+ 1) Explicit relationship
+ A relationship that is defined in the task record, typically the ordering of the tasks. Ex. Blocking
+ 2) Implicit relationship (give an example)
+ Relationship a task has that can only be derived by using information from other tasks. ex. Resource-based relationship: tasks share the same human resource.  Resource can be the person the task is assigned to or the person who creates and reports the task.
+ 3) Resourse based relationship
+ Above
+ 4) Attribute based relationship
+ A relationship between tasks that shared the same attribute. If tasks are performed on the same component.
+ 5) Content based relationship
+ Similarity of task based on how they are conducted or what the affect.