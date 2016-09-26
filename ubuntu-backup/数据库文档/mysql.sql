
# last date
SELECT * FROM jokes WHERE date > DATE_SUB(NOW(), INTERVAL 1 DAY) ORDER BY score DESC;

# last week
SELECT * FROM jokes WHERE date > DATE_SUB(NOW(), INTERVAL 1 WEEK) ORDER BY score DESC;

# last month
SELECT * FROM jokes WHERE date > DATE_SUB(NOW(), INTERVAL 1 MONTH) ORDER BY score DESC;


# Current date
select count(*) from myTable where DATE(myTime) = DATE(NOW());

# Current week
select count(*) from myTable where YEAR(myTime) = YEAR(NOW()) AND WEEKOFYEAR(myTime) = WEEKOFYEAR(NOW());

# Current month
select count(*) from myTable where YEAR(myTime) = YEAR(NOW()) AND MONTH(myTime) = MONTH(NOW());

# Current year
select count(*) from myTable where YEAR(myTime) = YEAR(NOW());


# yesterday's date
subdate(current_date, 1)
subdate(curdate(), 1)

# tomorrow's date
adddate(current_date, 1)
adddate(curdate(), 1)
