# YouTube Recommendation Engine 


***
In our group of 3, we often notice that YouTube doesn't always recommend the best videos for us to watch. We get a range of various different videos or even videos we have already watched. Using YouTube's API and Machine Learning we aim to create a better video recommendation system based on videos you have watched. 
***
### Overview of Project
Using a Docker container to host our Airflow allowed us to run the standard build on each machine. Airflow was scheduled to run daily to pull YouTube's API to grab the top trending videos. The data was then cleaned and exported to MySQL Database hosted on AWS Lightsail. Which was then exported to be used as data for visualization and machine learning models.


<p align="center">
<img width="700" src = "https://github.com/agonzalez1216/Youtube-Recommendation-System/blob/dev/images/Youtube_Overview.png">
</p>

***
### Technologies Involved:
* Python
* AWS Lightsail MySQL Database
* Docker
* Airflow
* Jupyter Notebook
* Pandas
* Natural Language Toolkit(NLTK)
* Seaborn
* Matplotlib
* SKLearn TF-IDF
* Django

## API:
* YouTube Data API v3
