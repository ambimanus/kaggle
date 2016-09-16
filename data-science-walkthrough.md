Data Science Walkthrough
========================

http://brettromero.com/wordpress/data-science-a-kaggle-walkthrough-introduction/


Understand Data
---------------

- get hints for important fractions of the data
    - example: check time-dependeny of training data and date range of test
    data (probably we should emphasize on a certain date range?)
- get hints for subsequent analytic phases
    - example: analyze plausibility (identify outliers and their origin, e.g.
    common misspellings)
- get hints for the required analytic approach
    - example: distribution of response variable determines the needed
    sensititivy of the model


Clean Data
----------

- domain knowledge may help here
- fix formats
- imputation
  - category: introduce 'unknown' category, this will preserve structural
  information
- fix outliers
- standardize categories (convert values that mean the same to a common category)
- in kaggle competitions, we might combine test and train to obtain higher
  accuracy (in general however, this is not good practice)


Data Transformation
-------------------

- bucketing/binning: eliminate noise, e.g. convert age values to age categories
- normalization (required by many algorithms)
- transformation, e.g. logarithm to eliminate exponential data spread (e.g.
many low values, few high values)
- one hot encoding: decode category variable with x possible category values
into x new (numeric) dummy variables (where each new variable represents a
different category value) being each either 0 (original item was not of the
category value corresponding to this dummy variable) or 1 (original item had
this very category value).
    - this transforms categorical to numerical data (without changing the
    structure by e.g. introducing an ordering), which is required by some
    algorithms


Feature Construction
--------------------

- domain knowledge helps a lot here!
- hierarchical: extract different hierarchy levels from a variable
    - bottom-up example: infer new feature "continent" from existing feature
    "country"
    - top-down example: split "datetime" into "year", "month", "day",
    "day of week" and so on
- add external data
    - example: add demographic data inferred from feature "country"
    - example: identify primary/secondary device for each website user by
    counting sessions per user (from external logging data) with respect to
    devices used


Feature Selection
-----------------

- depends on algorithm: some require few features, others don't care


Algorithm Selection
-------------------

- most popular approaches: Random Forest and Gradient Boosting
    - for Gradient Boosting, use XGBoost library
- even more promising: Ensembles with XGBoost and Deep Learning
  - http://www.kdnuggets.com/2016/03/xgboost-implementing-winningest-kaggle-algorithm-spark-flink.html
  - http://blog.kaggle.com/2016/03/07/airbnb-new-user-bookings-winners-interview-3rd-place-sandro-vega-pons/
- before going to complex strategies, gain a deep understanding of the
evaluation measure for the problem at hand, and buld a reliable validation
strategy


Parameter Tuning
----------------

- use grid search combined with k-fold cross-validation (GridSearchCV)


Model Training
--------------

- split training/test data if it was combined during the cleaning phase
- remove random nonsense data such as user-ids
- split into features (X) and response (y)
- choose metric for performance measurement
    - see: http://scikit-learn.org/stable/modules/model_evaluation.html
    - Quote from svpons interview (see URL in Algorithm Selection):
    > I always got the best results when using multi-class log-loss as
    objective function. Specifically, for the the definition of EN_optA and
    EN_optB (second layer), I tried with different objective functions like
    mlogloss, mlogloss@5 (multi-class log-loss after keeping only the 5 classes
    with highest probabilities), ndcg@5 (the competition evaluation metric) and
    mlogloss + 2 - ndcg@5 (a combination of mlogloss and ndcg after converting
    ndcg to a dissimilarity measure). I was expecting the ndcg not to work
    well, since it is a non-smooth function and therefore not suitable for
    gradient based optimization. However, I was not sure whether some
    combination of mlogloss and ndcg could give any improvement.
    [...]
    Directly using an [competition] evaluation metric as objective function is
    not always the optimal solution.
- set defined seeds for RNG


Prediction
----------

- remove same random nonsense data as in the training phase, such as user-ids


Interpretation
--------------

- beware of "counfounding": interpreting correlation for causality
