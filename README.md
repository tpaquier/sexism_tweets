This notebook is an adaptation of  **[*An Annotated Corpus for Sexism Detection in French Tweets*](https://hal.science/hal-02889035/)**, by Patricia Chiril, Véronique Moriceau, Farah Benamara, Alda Mari, Gloria Origgi and Marlène Coulomb-Gully. The authors of the article have a git in which there is the id of each tweet that was selected in order to implement and test different methods to detect sexism in french tweets. Hence, implementing the paper and testing a few methods required a bit of craftmanship.

In a nuthsell, the paper described how the authors annnotated different tweets in order to classify them as having sexist content or not. Once the annotation were done, they tested different methods in order to detect sexism in tweets. As for us, we tried bag of words, t-SNE and a neural-network approach. The neural network was slighlty modified from what was presented in the article in order to see how well we could perform given a different architecture.  

# The scraping
As we had only access to a tweet's id, we needed to scrap Twitter (now X). As the rules changed a bit from the moment when it was called twitter, we had to use a package called `twikit`. Moreover, as the policy concerning bots has changed, we had a few difficulties scraping Twitter (we got five accounts that were banned). However, we managed to find a solution to these issues by imposing a random time between two requests. Nevertheless, our procedure was probably detected as being a bot as the response time of Twitter increased at 'fixed' intervals making the whole scraping last about fifteen hours. Our code to retrieve the tweets is in `twitter_scraping.py`. 

For this code to run, one needs to give its Twitter account credentials. We created one for the project but left it 'blank' as the repository will stay in public. The output is a csv file containing the tweet's id, its label (provided by the authors) of the article and the texte of the tweet, untreated. Hence, we had to take care of urls and emojis as they are quite frequent in Tweets. 

# Fabz do your magic here


# Neural Network
As the annotated corpus contained French tweets, we used the BERT variant adapted to French text that is CamemBERT. This model was used for two purposes. First, to retrieve the embeddings of the tweets and also to serve as a 'base' for our 'new' model. Concerning the embeddings, we decided to keep the whole sentence embedded and not average it in order to try to capture more 'subtle' differences. 

For the model itself, two main approaches were developped in the article. First, train a model from scratch using convolutional layers and bi-directional LSTM layers. The other idea was first to use BERT and adding on top of the pre existing architecture a layer in order to do transfer learning. We decided to mix up a bit both. 

We kept the pre-existing CamemBERT layers and added convolutional and bi-directional LSTM layers (with ReLU non-linearities). However, we decided to retrain the last layer of CamemBERT. This is because after a first training cycle, the precision and F1 score didn't change at all. Moreover, if we had kept the 'classical' BCE loss, as we were dealing with binary classification, it seemed logical that the model would only predict positive (i.e. sexist) labels./ Hence, we used a penalized loss in order to try to have better performances. At the end of the training, that was longer than the one in the article since we decided to train for 25 epochs whereas the authors ran 3 epochs, we had quite satisfying results. On our training set, we had : 

```
precision : 0.7918
F1 : 0.6989
AUC : 0.8580
```

We were quite happy with our results as the best precision attained by the authors was 0.790 (because their 'accuracy' is our 'precision'). Moreover, we think that with a bit more training or minor changes in the architecture, our F1 score could match what was presented in the paper. 




# Conclusion



