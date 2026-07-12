# Hands on Machine Learning with Scikit-Learn and PyTorch

## Sources
- [handson-mlp github](https://github.com/ageron/handson-mlp/tree/main)

## Cards

### Chapter 1 — The Machine Learning Landscape

### What Is Machine Learning?

**Front:**
How would you define Machine Learning?

**Back:**
Machine Learning is about building systems that can **learn from data**. Learning means getting better at some task, given some performance measure.

Key distinction from traditional programming: instead of explicitly coding rules, the system discovers patterns from data.

---

### When to Use Machine Learning

**Front:**
What are four scenarios where Machine Learning is a better approach than traditional programming?

**Back:**
- **Complex problems with no known algorithmic solution** — e.g., speech recognition, image classification
- **Replacing long lists of hand-tuned rules** — e.g., spam filters with hundreds of manually maintained rules
- **Fluctuating environments** — systems that need to adapt to changing data (e.g., new types of spam)
- **Helping humans learn** — data mining to discover patterns that aren't obvious (e.g., finding correlations in large datasets)

---

### Labeled Training Set

**Front:**
What is a labeled training set?

**Back:**
A training set that contains the **desired solution** (called a **label**) for each instance.

Example: an email dataset where each email is tagged as "spam" or "not spam."

Used in **supervised learning** — the algorithm learns to map inputs to known outputs.

---

### Four Learning Paradigms by Label Availability

**Front:**
What are the four main learning paradigms based on how labels are used in training data?

**Back:**
- **Supervised** — all training data has labels. Model learns to map inputs to known outputs. (e.g., classifying emails as spam/not spam using a labeled dataset)
- **Unsupervised** — no labels at all. Model finds hidden structure in the data on its own. (e.g., clustering customers into segments without predefined groups)
- **Semi-supervised** — a small amount of labeled data combined with a large amount of unlabeled data. Model uses the labeled examples to guide learning from the unlabeled ones. (e.g., Google Photos: you label a few faces, then it clusters and labels the rest automatically)
- **Self-supervised** — the model generates its own labels from the structure of the data, then learns in a supervised fashion from those generated labels. (e.g., GPT-style language models predict the next word — the "label" is just the next word in existing text, so no human labeling is needed)

Semi-supervised and self-supervised both bridge the gap between supervised and unsupervised — they avoid the cost of fully labeling data while still giving the model a training signal.

---

### Supervised Learning Tasks

**Front:**
What are the two most common supervised learning tasks, and how do they differ?

**Back:**
- **Regression** — predict a continuous numerical value (e.g., predicting house prices given features like size, location)
- **Classification** — predict a discrete category/class (e.g., classifying emails as spam or not spam)

Key difference: regression outputs a number on a continuous scale; classification outputs a class label from a finite set.

Note: many classifiers output a **probability** (e.g., 80% chance of spam) that is then mapped to a category via a decision threshold. This is still classification — the model is trained to predict a class, not a continuous value.

---

### Common Unsupervised Learning Tasks

**Front:**
What are four common unsupervised learning tasks?

**Back:**
- **Clustering** — grouping similar instances together (e.g., customer segmentation)
- **Visualization** — plotting high-dimensional data in 2D or 3D while preserving structure
- **Dimensionality reduction** — simplifying data by reducing the number of features while retaining as much information as possible
- **Association rule learning** — discovering relationships between attributes (e.g., people who buy X also tend to buy Y)

---

### Reinforcement Learning

**Front:**
When would you choose Reinforcement Learning over supervised or unsupervised learning? Give an example.

**Back:**
In RL, an **agent** observes an environment, takes **actions**, and receives **rewards or penalties**. It learns a **policy** — a strategy that maximizes cumulative reward over time.

Choose RL when an agent must learn a **sequence of actions** by interacting with an environment.

Example: a robot learning to walk in various unknown terrains. The robot tries different movements, gets feedback (falling = penalty, moving forward = reward), and gradually improves its policy.

RL is the natural fit when:
- The problem involves sequential decision-making
- There's no labeled "correct action" dataset
- The environment may be unknown or changing

---

### Clustering vs Classification for Customer Segmentation

**Front:**
You want to segment customers into groups. When would you use clustering vs classification?

**Back:**
- **Don't know what the groups should be** → use **clustering** (unsupervised). The algorithm discovers natural groupings based on similarity.
- **Already know what groups you want** → use **classification** (supervised). Provide labeled examples of each group, and the algorithm learns to assign new customers to the predefined groups.

---

### Online vs Batch Learning

**Front:**
What is the key difference between online learning and batch learning?

**Back:**
- **Batch learning** — the system is trained on the entire dataset at once. To learn about new data, you must retrain from scratch on the full dataset (old + new).
- **Online learning** — the system learns **incrementally**, one instance or mini-batch at a time. There is only one model — each mini-batch updates the **same parameters** (e.g., via gradient descent), so the model is refined progressively rather than rebuilt.

Online learning is better when:
- Data arrives continuously (e.g., stock prices)
- The system must adapt rapidly to changing data
- The dataset is too large to fit in memory (out-of-core learning)

---

### Out-of-Core Learning

**Front:**
What is out-of-core learning, and how does it work?

**Back:**
Out-of-core learning handles datasets **too large to fit in a computer's main memory**.

How it works: the algorithm chops the data into **mini-batches** and uses **online learning techniques** to learn from each mini-batch sequentially. Each mini-batch is loaded, learned from, then discarded before loading the next.

It's essentially online learning applied to the problem of limited memory rather than streaming data.

---

### Instance-Based vs Model-Based Learning

**Front:**
How does an instance-based learning system make predictions, compared to a model-based system?

**Back:**
**Instance-based learning:**
- Learns the training data **by heart**
- For a new instance, uses a **similarity measure** to find the most similar learned instances
- Predicts based on those similar instances (e.g., k-nearest neighbors)

**Model-based learning:**
- Searches for **optimal parameter values** so the model generalizes to new instances
- Trained by minimizing a **cost function** (+ regularization penalty if applicable)
- Predicts by feeding new instance features into the model's prediction function with learned parameters

---

### Model Parameters vs Hyperparameters

**Front:**
What is the difference between a model parameter and a hyperparameter?

**Back:**
- **Model parameter** — determines what the model predicts given a new instance. Learned during training. (e.g., the slope and intercept of a linear model)
- **Hyperparameter** — a parameter of the **learning algorithm itself**, not the model. Set before training and controls how training proceeds. (e.g., the amount of regularization, learning rate, number of neighbors in k-NN)

The learning algorithm optimizes model parameters; the practitioner tunes hyperparameters.

---

### Main Challenges in Machine Learning

**Front:**
What are the main challenges in Machine Learning (4 data, 2 model)?

**Back:**
Data problems:
- **Insufficient quantity** of training data
- **Poor data quality** (errors, noise, missing values)
- **Nonrepresentative data** (sampling bias)
- **Uninformative features** (irrelevant or redundant)

Model problems:
- **Underfitting** — model is too simple to capture the underlying pattern
- **Overfitting** — model is too complex and fits noise in the training data

---

### Diagnosing and Fixing Overfitting

**Front:**
A model performs great on training data but generalizes poorly to new instances. What is likely wrong, and what are possible solutions?

**Back:**
The model is likely **overfitting** the training data — it has learned noise and details specific to the training set rather than the underlying pattern.

Possible solutions:
- **Get more training data** — more data makes it harder to overfit
- **Simplify the model** — use a simpler algorithm, reduce the number of parameters or features
- **Regularize the model** — constrain the model to reduce its degrees of freedom (add a penalty to the cost function that discourages large parameter values, limiting how much the model can bend to fit noise)
- **Reduce noise** in the training data (fix errors, remove outliers)

---

### Test Set vs Validation Set

**Front:**
What is the difference between a test set and a validation set?

**Back:**
Data is split into three parts:
- **Training set** (~60-80%) — the model learns from this
- **Validation set** (~10-20%) — carved from training data, used to **compare models** and **tune hyperparameters** during development. Can be evaluated on repeatedly.
- **Test set** (~10-20%) — used **once at the very end** to estimate **generalization error** before going to production

The validation set is separate from the test set — it is not a subset of it. If you tune hyperparameters using the test set, you risk overfitting to it, and your generalization error estimate will be **optimistically biased**.

---

### Train-Dev Set

**Front:**
What is a train-dev set, and when would you use one?

**Back:**
Used when there's a risk of **mismatch between training data and validation/test data** (which should always resemble production data).

The train-dev set is a portion of the training data **held out** (not trained on). After training, evaluate on both the train-dev set and validation set:

- Good on training set, **bad on train-dev set** → the model is **overfitting** the training data
- Good on training set and train-dev set, **bad on validation set** → there's a **data mismatch** between training data and validation/test data — improve training data to better resemble production data

---