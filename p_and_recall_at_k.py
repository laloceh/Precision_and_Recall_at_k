#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 14:17:02 2018

@author: edgar ceh

This program calculates the precision at k (Precision@k), and recall at k (Recall@k)
This metrics are used in recommender systems to see if the the predicted
ratings for a given user are inside its top-k items

"""

from collections import defaultdict
import pandas as pd


'''
    Function to build a helper dictionary
    simulating a matrix with the predicted
    ratings and the actual ratings"
'''
def df_for_precision_and_recall(missing_ids, all_ratings, k=3):
        
    item_est_true = {}    
    col1 = []
    col2 = []
    col3 = []

    for i,est in enumerate(all_ratings):
        item = i+1
        if item in missing_ids:
            true = 0
            col1.append(item)
            col2.append(true)
            col3.append(est)            
        else:
            true = est           
            col1.append(item)
            col2.append(true)
            col3.append(est)
            
    item_est_true['ids'] = col1
    item_est_true['true'] = col2 # The actual ratings
    item_est_true['estimated'] = col3 # The predicted ratings

    return item_est_true

    
'''
    Function to calculate the precision and recall at k
    This will calculate if k ratings are inside the 
    top rated items for a given user
'''
def precision_recall_at_k(df, k=3, threshold=3.5):
    # Sort by estimated value
    df.sort_values(by=['estimated'], inplace=True, ascending=False)
    print df
    
    # number of relevan items
    n_rel = df[df['true']>= threshold].count()['true']
    print 'n_relevant=',n_rel
    
    # Number of recommended items in top k
    n_rec_k = df[df['estimated']>= threshold][:k].count()['estimated']
    print 'n_recommended_at_k=',n_rec_k
    
    # Number of relevant and recommended items in top k
    df_k = df[:k]
    #print df_k
    n_rel_and_rec_k = df_k[(df_k['true']>= threshold) & (df_k['estimated']>= threshold)].count()['ids']
    print 'n_relevant_and_recommended_k=',n_rel_and_rec_k
    
     # Precision@K: Proportion of recommended items that are relevant
    if n_rec_k != 0:
        precision = float(n_rel_and_rec_k) / n_rec_k 
    else:
        precision = 1
        
    # Recall@K: Proportion of relevant items that are recommended
    if n_rel != 0:
        recall = float(n_rel_and_rec_k) / n_rel
    else:
        recall = 1
    
    return precision, recall
    
    
######################
if __name__ == "__main__":
    missing_ids = [4,6,8,9] 
    all_ratings = [4, 2, 3, 4.3, 5, 2.3, 2, 4.3, 3.3, 4]
    rating_data = df_for_precision_and_recall(missing_ids, all_ratings)
    df = pd.DataFrame.from_dict(rating_data)
    
    precision, recall = precision_recall_at_k(df, k=5)
    print 'precision = ', precision
    print 'recall = ', recall
