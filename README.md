# Welcome to CleanMyData!

> All over the world, more and more data is being produced every day.
> However, almost no data has its quality checked immediately as it is
> produced, meaning that a lot of poor-quality data is circulating the
> Internet. Datasets need to be reliable for when data analysis is
> performed, so that the result of the analysis is useful. It is worth
> considering the issues that an analysis based on data of poor quality
> could lead to: The result of such an analysis could be either false or
> misleading, ending up having a negative impact on projects that affect
> the real world, thereby affecting real people. Therefore, data quality
> assurance is an important aspect of database and analysis work.

*How can a simplified data wrangling tool be made to allow accessibility in transforming heterogeneous data to homogeneous data?*


# Setup

1. Download the required files such as Python 3.9.5 and your preferred
    code editor.
    
2. Initiate a new virtual environment with python using the following command in a terminal. You should be positioned in the project directory.
	```
	python -m venv env
	```
	
3. Now, activate the environment you just created.
	```
	env\scripts\activate
	```

4. Next, in the same directory, install the project dependencies with the following command:
    	```
	pip install -r requirements.txt
	```

5. You are now ready to start the server with the command:
	```
	python manage.py runserver
