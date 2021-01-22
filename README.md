***
### Overview of Project
Using a Docker container to host our Airflow allowed us to run the standard build on each machine. Airflow was scheduled to run daily to pull YouTube's API to grab the top trending videos. The data was then cleaned and exported to MySQL Database hosted on AWS Lightsail. Which was then exported to be used as data for visualization and machine learning models.


<p align="center">
<img width="700" src = "https://github.com/agonzalez1216/Youtube-Recommendation-System/blob/dev/images/Youtube_Overview_update.png">
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
