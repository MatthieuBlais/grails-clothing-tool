# Meow

## 1. Why Meow?

Because I lack of inspiration and that's the only thing that came to my mind.

## 2. What is this?

This Grails application is just an internal tool to better organize and synchronize our work related to a clothing project. We also have a few independent pieces of code and it allows us to keep everything in one place. Feel free to add your own stuff.

Currently it includes:
- Database SQL query interface
- Image labelling for computer vision
- Data cleaning (images) for computer vision
- API development documentation

## 3. What do I need to get started? 

- Linux is better, but you can it "should" work on windows. If you have any bugs on Windows, contact Bill Gates though. 
- Grails 3.2.8
- Java 8. Java 9 and 10 are not supported by Grails yet. Grails 4 should come by the end of the year and they should support Java 10, but for now, we must deal with that
- PostgreSQL 9.X or 10.X 
- Python2.7

Installation: 
1. Clone this repository
2. Open grails-app/conf/application.yml
3. Replace lines 110, 111 and 112 the database credentials by yours (or request the shared database credentials)
4. If you use your local database (DON'T DO THAT ON THE SHARED DATABASE), open grails-app/init/db/Bootstrap.groovy. Uncomment line 14, initUser. Set email and password in initUser function, save.
4. "grails run-app" to start the application. The first run will take a while as the system must download all the libraries
5. If you have done step 4, stop the application, comment back line 14, initUser. 

DONE!

About git, do not push any credentials in application.yml and boostrap.groovy. 
Ignore all changes with git update-index --assume-unchanged <file>

## 3. More details?

Check the documentation included directly in the app.

Few tools:

- SQL query: Used to analyze the data in AWS RDS. 

![alt text](https://raw.githubusercontent.com/MatthieuBlais/grails-clothing-tool/master/doc/sql_query.png)


- Image Labelling: To identify clothes on the picture

![alt text](https://raw.githubusercontent.com/MatthieuBlais/grails-clothing-tool/master/doc/label_image.png)

- Data Cleaning: Clean existing labelled image. Some labelling is done automatically with an existing model. The interface allows the user to clean misclassified images and/or adjust the coordinates of detected clothes.

![alt text](https://raw.githubusercontent.com/MatthieuBlais/grails-clothing-tool/master/doc/cleaning.png)

- API Documentation: To synchronize work

![alt text](https://raw.githubusercontent.com/MatthieuBlais/grails-clothing-tool/master/doc/api.png)


And more:
- Similarity algoi

