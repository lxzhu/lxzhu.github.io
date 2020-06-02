---
title: k-nearest neighbors algorithm
subtitle: with introduction to mnist dataset
tags: [knn, mnist, machine learning]
---

This is a part of learning Python and Machine Learning.

[kNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm){:target="blank"} might be the simplest machine learning algorithm. In this post, i will implementthe algorithm and test with mnist dataset.

**The primary principle of kNN** is thinking all the data records are points in space, and the nearest k points vote, according to their own label, to elect a label for the test point.  There are two points that might change the error rate of this algorithm:

1. the measurement of distance. In this post, [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance){:target="blank"} is used.
1. the weight of each points.

The algorithm in this post will be generic to mnist dataset. To be applied with other dataset, you may need to change it a little.

[Minist dataset](http://yann.lecun.com/exdb/mnist){:target="blank"} is a large handwriting digitals which is commonly used for training various image processing systems. The database is widely used in training and testing in the field of machine learning.

Minist datasets used in this post are a little different with the original one. Lable file is merged into training and testing data respectively. In [mnist_train.csv.gz](/dataset-mnist/mnist_train.csv.gz){:target="blank"} and [mnist_test.csv.gz](/dataset-mnist/mnist_test.csv.gz){:target="blank"}, the first field of each line is the lable. mnist_train.csv contains 60 000 lines and mnist_test.csv.gz contains 10 000 lines. Each line is a handwritting image.

I copied the first 1000 lines from mnist_train.csv and mnist_test.csv.gz, then I get [mnist_train_1000.csv.gz](/dataset-mnist/mnist_train_1000.csv.gz) and [mnist_test_1000.csv.gz](/dataset-mnist/mnist_test_1000.csv.gz). I find smaller datasets are more practicle when you're learning the algorithm.


Here is an example code to show the data as image

```python
%matplotlib inline

```
