-- 1. Display all books
SELECT * FROM books;

-- 2. Display books costing more than £40
SELECT title, price_gbp
FROM books
WHERE price_gbp > 40;

-- 3. Display the 10 cheapest books
SELECT title, price_gbp
FROM books
ORDER BY price_gbp ASC
LIMIT 10;

-- 4. Display the average book price in INR
SELECT AVG(price_inr) AS average_price_inr
FROM books;

-- 5. Join books with categories
SELECT
    books.title,
    books.price_gbp,
    categories.category_name
FROM books
JOIN categories
    ON books.category_id = categories.category_id;