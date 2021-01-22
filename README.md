# YouTube Recommendation Engine 


***
The purpose of this project is to build a youtube recommendation system based on a users previously watched videos. We have all found that the youtube system isn't the greatest and we want to hopefully improve it. We will be doing this by using technologies such as Airflow and Spark to gather, clean and analyze data. Then we want to create a GUI to display our results.

We plan to accommodate a 3 week timeline:   
Week 1 - Data Collection and Storage  
Week 2 - Data Cleaning and Modeling  
Week 3 - Data Visualization
 
***
### Overview of Project
Using a Docker container to host our Airflow allowed us to run the standard build on each machine. Airflow was scheduled to run daily to pull YouTube's API to grab the top trending videos. The data was then cleaned and exported to MySQL Database hosted on AWS Lightsail. Which was then exported to be used as data for visualization and machine learning models.


<p align="center">
<img width="700" src = "https://github.com/agonzalez1216/Youtube-Recommendation-System/blob/dev/images/Youtube_Overview.png">
</p>

### Summary of Data Analysis
* NFL produced the most trending videos in January
* Most disliked video was by Mini Ladd with a 71% dislike ratio
* Most popular category videos in order Entertainment, Spirts, Music
* Most popular video is The Weeknd - Save Your Tears
* Video that was on top trending the longest,  MrBeastGaming - If You Build a House, I'll Pay For It! 	for 7 days
<p align="center">
<img width="700" src = "https://github.com/agonzalez1216/Youtube-Recommendation-System/blob/dev/images/youtube_channels.png">
</p>
<p align="center">
<img width="700" src = "https://github.com/agonzalez1216/Youtube-Recommendation-System/blob/dev/images/youtube_categories.png">
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
