This notebook is an adaptation of  **[*An Annotated Corpus for Sexism Detection in French Tweets*](https://hal.science/hal-02889035/)**, by Patricia Chiril, Véronique Moriceau, Farah Benamara, Alda Mari, Gloria Origgi and Marlène Coulomb-Gully. The authors of the article have a git in which there is the id of each tweet that was selected in order to implement and test different methods to detect sexism in french tweets. Hence, implementing the paper and testing a few methods required a bit of craftmanship.

In a nuthsell, the paper described how the authors annnotated different tweets in order to classify them as having sexist content or not. Once the annotation were done, they tested different methods in order to detect sexism in tweets. As for us, we tried bag of words, t-SNE and a neural-network approach. The neural network was slighlty modified from what was presented in the article in order to see how well we could perform given a different architecture.  

# The scraping
As we had only access to a tweet's id, we needed to scrap Twitter (now X). As the rules changed a bit from the moment when it was called twitter, we had to use a package called `twikit`. Moreover, as the policy concerning bots has changed, we had a few difficulties scraping Twitter (we got five accounts that were banned). However, we managed to find a solution to these issues by imposing a random time between two requests. Nevertheless, our procedure was probably detected as being a bot as the response time of Twitter increased at 'fixed' intervals making the whole scraping last about fifteen hours. Our code to retrieve the tweets is in `twitter_scraping.py`. 

For this code to run, one needs to give its Twitter account credentials. We created one for the project but left it 'blank' as the repository will stay in public. The output is a csv file containing the tweet's id, its label (provided by the authors) of the article and the texte of the tweet, untreated. Hence, we had to take care of urls and emojis as they are quite frequent in Tweets. 

# Text preprocessing

With the `data_preprocessing.ipynb` we clean up a corpus of French tweets before implementing the model.
The processing steps are as follows:
- **Data loading**
The `tweets.csv` file is automatically downloaded from Google Drive and loaded into a pandas DataFrame. Empty tweets (missing values in the text column) are removed.
- **Raw text cleaning**
We apply several pre-processing operations to the text:
    - Lower-casing to standardize data.
    - Deletion of URLs.
    - Conversion of emojis to explicit French text descriptions (for example, :smile: becomes __visage_souriant__), using the emoji library.
    - Replacement of emoticons (such as :), :(, XD, etc.) with their French meanings (e.g. sourire, tristesse, rire) via a custom dictionary.

# Supervised classification with SVM 

In the notebook `bow_svm.ipynb`, we want to reproduce the approach described in the reference article, using a simple supervised classification method based on an SVM model and a Bag-of-Words (BoW) representation. The aim was to establish an initial baseline from which we could compare the results obtained with more recent CamemBERT transformers model
Steps taken :
- Vectorization: conversion of texts into numerical vectors using CountVectorizer (n-grams up to 3 words, 1000 features max).
- Training: training of a linear SVM classifier (LinearSVC) on vectors.
- Evaluation: performance measured via a classification ratio and a confusion matrix.

The SVM model trained on the TF-IDF representations achieves an accuracy of 73%, with an f1-score of 0.78 for non-sexist tweets and 0.65 for sexist tweets.

The t-SNE projection of the vectors shows a strong overlap between the two classes, suggesting a difficult separation in the lexical space.

# Neural Network
As the annotated corpus contained French tweets, we used the BERT variant adapted to French text that is CamemBERT. This model was used for two purposes. First, to retrieve the embeddings of the tweets and also to serve as a 'base' for our 'new' model. Concerning the embeddings, we decided to keep the whole sentence embedded and not average it in order to try to capture more 'subtle' differences. 

For the model itself, two main approaches were developped in the article. First, train a model from scratch using convolutional layers and bi-directional LSTM layers. The other idea was first to use BERT and adding on top of the pre existing architecture a layer in order to do transfer learning. We decided to mix up a bit both. Our implementation of the neural newrok for the classification is done in the notebook `true_retrain.ipynb`.

We kept the pre-existing CamemBERT layers and added convolutional and bi-directional LSTM layers (with ReLU non-linearities). However, we decided to retrain the last layer of CamemBERT. This is because after a first training cycle, the precision and F1 score didn't change at all. Moreover, if we had kept the 'classical' BCE loss, as we were dealing with binary classification, it seemed logical that the model would only predict positive (i.e. sexist) labels./ Hence, we used a penalized loss in order to try to have better performances. At the end of the training, that was longer than the one in the article since we decided to train for 25 epochs whereas the authors ran 3 epochs, we had quite satisfying results. On our training set, we had : 

```
precision : 0.7918
F1 : 0.6989
AUC : 0.8580
```

We were quite happy with our results as the best precision attained by the authors was 0.790 (because their 'accuracy' is our 'precision'). Moreover, we think that with a bit more training or minor changes in the architecture, our F1 score could match what was presented in the paper. 




# Conclusion

The authors proposed a very interesting corpus for the detection of sexism in tweets. As we were more 'data-centered' our main concern couldn't be how a tweet was sexist *a priori* but after looking at the cited references the methodology was very interesting. Concerning our results, we are quite happy with them. Nevertheless, our model has a few flaws. First, we had to train our model more than the authors to get such resutls. This could come from the fact that, since the article was published, a certain quantity of identified tweets had been either deleted or removed. Which caused us to work with approximately 7k annotated tweets whereas they had more or less 12k. Hence, they managed to obtain very good results with limited computations whereas we had to use GPUs for a longer time. 

Concerning the results themselves, even if they were quite satisfying, we still have some problems with false positive. This might be due to our samples that might have been biased. Indeed, as the selected tweets, even if not containing sexits content were selected because they at least mention it. So, for more general sentences such as 'la discrimination contre les femmes est un problème', our model will predict it as positive. This could be because as we haven't retrained the last layers on 'general' texts, the model might grasp a few particular words and occurences and once they appear in a tweet consider them as sexist. Something that could be seen as positive, but that is probably due more to the training sample than our procedure, is that there would be more false positives than false negatives, which is the best type of error we could get in our context. 









    



