SELECT * 
FROM product_urls 
WHERE supermarket_id = 1 
ORDER BY id 
LIMIT 10 OFFSET 0;
-- LIMIT '{{ variables("limit") }}'::int OFFSET '{{ variables("offset") }}'::int;