# Car database in Python

This program is for a Python submission for school. We have been working with Python for a little more than a month.

To start the program whe sould set up a database through SQLLite and Python. We should use the Create Table call from SQL to make a table in the database. 

The program should include the following:
- Make a class named *Car* that includes the following variables:
	1. Price, with the type Integer
	2. Brand, with the type String
	3. Year, with the type Integer
	4. License Plate, with the type string
	5. isLeasingCar, with the type Boolean
- Add 3 car objects with concrete data and insert them into the database table.

We should also make the 5 following functions:
1. Show all elements in a table from the database in a overwiev in the console
2. Add an element to the table in the database
3. Remove an element from the table in the database
4. Update an element from the table in the database
5. Show a specific elemment, through a search of the database


To run the program i made a simple .bat file to open the python file *main.py* in the console.

***

To display the cars most clear i used the module PrettyTable which prints nice good looking tables in python. You can install this using pip:
```python
pip install PTable
```

I included a simple [web scraper](https://en.wikipedia.org/wiki/Web_scraping) so you can import cars from the website [Bilhandel.dk](https://bilhandel.dk/). For this i used the module BeautifulSoup. You can install this using pip:

```python
pip install beautifulsoup4
```

***

### About me!
Hi i am Magnus. I am on my first year of gymnasium (High scool) here in Denmark. I have chosen the study program Programming and Math. So far we have only been working with JavaScript, Python and a bit of SQL, and this here is my first submission for our class.




*This is my first time uploading to GitHub and writing a README in markdown. Feedback is appreciated*
