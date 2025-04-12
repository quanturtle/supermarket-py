SELECT * 
FROM product_urls 
WHERE supermarket_id = 1 
ORDER BY id 
LIMIT '{{ variables("limit") }}'::int OFFSET '{{ variables("offset") }}'::int;