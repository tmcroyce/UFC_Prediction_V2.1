# UFC_Prediction_V2.1

# The UFC Prediction Capstone
![Martial Arts](images/spaceufc.jpg)

# Files
- [PDF Presentation (Note: Not updated since Version 1)](https://github.com/tmcroyce/UFC_Prediction/blob/master/presentation.pdf)
- [Video Presentation of Streamlit Application](https://www.youtube.com/watch?v=dl-JhDgQbRA) **TODO: ADD NEW!**
- [Scraping Notebook](UFC_Scraping_Notebook.pdf)
- [Final Notebook](Final_Notebook.pdf)

# Data
- The data was too large to upload normally, so the final test file is provided zipped in the 'compressed_data' folder
   
# Project Overview

The purpose of this project is to create a model to predict the outcome of UFC (Ultimate Fighting Championship) events. The UFC was created in 1993 with the expressed purpose of identifying the most effective martial art(s). This project is an extension of my curiosity into the original purpose of the UFC; what makes a more effective martial artist?

Stakeholders: UFC Bookkeepers, bettors and speculators

This project's end result will be an application which can help identify descrepancies between the "Vegas" odds of a fight and the model-predicted (i.e., theoretically more accurate) odds of that same fight. This could be used by bookmakers to increase revenues by offering slightly "better" odds than competitor bookmakers, given the model indicates it is appropriate. Alternatively, it could simply be used by bookmakers to create more accurate odds than previously, as the favorite only wins around 60% of the time in UFC history.

# Data Overview

## Sources:
 - [UFC.com](https://www.ufc.com/events)
 - [UFCStats.com](https://www.ufcstats.com)
 - [BestFightOdds.com](https://www.bestfightodds.com)


### Data Description

The majority of the data I used for this project I scraped from UFCStats.com. This website contains more statistics than any other website, but does not have some key metrics such as fighter sizes, bios, and odds. 

Thus, the odds were scraped from bestfightodds.com, while the fighter sizes and bios were scraped from ufc.com. 

Further, individual events and fights, and much from the final streamlit application, are scraped from ufc.com.

The data itself is fight-by-fight based data, originally from over 8,000 fights (which, after dropping for lack of data, decreased to around 5,000 by the final testing dataframe).

There are around 400 features in this dataset, after all are added.


### Define Target Variable

The target variable in this project is if a fighter won an individual fight or not. 

### Define Scoring Metric

Because our data is evenly split between wins and losses, and there is no relative advantage between false negatives and false positives, accuracy is my chosen scoring metric.

## Project Structure

As there was no up-to-date database available, a good portion of this notebook is scraping and saving data using various methods with beautiful soup and selenium. 

The following features were created, either by the scrape itself or calculations done after:

- Fighters A & B 
- Fighter Odds
- Event Date, Name, Urls, Fighter URLs
- Descriptive statistics (mean, median, minimum, maximum, standard deviation) for metrics for each fighter, such as:
    - Knockdowns (attempts, successes, average success rate)
    - Significant Strikes (attempts, successes, average success rate)
    - Total Strikes (attempts, successes, average success rate)
    - Takedowns (attempts, successes, average success rate)
    - Submissions (attempts, successes, average success rate)
    - Control time (attempts, successes, average success rate)
    - Head Strikes (attempts, successes, average success rate)
    - Body Strikes (attempts, successes, average success rate)
    - Leg Strikes (attempts, successes, average success rate)
    - Distance Strikes (attempts, successes, average success rate)
    - Clinch Strikes (attempts, successes, average success rate)
    - Ground Stikes (attempts, successes, average success rate)
- Height, Weight, Reach, Leg Reach, and fighter differences in these metrics.

All in all, there were aproximately 350 features in the final test set.



## Testing

The initial model (decision tree) achieved an accuracy of 60%. 

After iterating on a variety of models, including decision tree, logistic regression, bagged trees, extrra trees, KNN, and random forest, I found the best performing model to be an extra trees model which tested at 70% accuracy. 

## Project Conclusion

The final model achieved a 73% (rounded) accuracy. 

The model's most important features included:
    - Difference in Average Ground Strikes
    - Ground Strikes (Standard Deviation)
    - Takedown Percentage (Standard Deviation)
    - Head Strikes 
    - Significant Strikes Percentage

Upon looking into these features, we find that leg reach, while being the most important feature in the algorithm, is not necessarily a consistant advantage or disadvantage, so its importance must be coupled with other features. 

The betting favorite wins approximately 62 percent of the time, indicating the lack of "market" (as in, the betting market) knowledge about what makes a winning fighter. That being said, it is our most accurate single statistical metric for predicting a fight. 

Ground strikes are strikes thrown from a ground position, meaning the martial artists are likely utilizing wrestling, sambo, or jujitsu. The ability to utilize these is indoubtedly important. 

Takedown percentage is the percentage of successful takedowns a martial artist has divided by the number attempted. A takedown typically involves utilizing wrestling skills, although variations with sambo, jujitsu, and judo also occur. It may be important to note that utilizing ground strikes is typically only possible after a successful takedown. 

The number of head strikes is also important, albeit less so than the factors above. Head strikes - or the number of strikes to an opponents head, using boxing, muay thai, kickboxing, etc. - is often thought of as the most valuable technique for success, but we find it just to be among them. 

Finally, significant strikes percentage. This can be thought of as the accuracy of the striker, but does not reflect total output. 
