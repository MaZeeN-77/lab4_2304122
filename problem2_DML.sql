USE library;
GO


INSERT INTO AUTHOR (name, country) VALUES
('George Orwell','UK'),     
('Jane Austen','UK'),        
('Naguib Mahfouz','Egypt'),     
('Gabriel Garcia Marquez','Colombia'),  
('Haruki Murakami','Japan');     
GO


INSERT INTO PUBLISHER (name, country) VALUES
('Penguin Books','UK'), 
('Dar El Shorouk','Egypt'),
('Vintage','USA'); 
GO


INSERT INTO CATEGORY (name) VALUES
('Fiction'),  
('Classics'),
('Dystopian');  
GO


INSERT INTO BOOK (title, price, publish_year, author_id, publisher_id, category_id) VALUES
('Nineteen Eighty-Four',             12.99, 1949, 1, 1, 3),  
('Animal Farm',                       9.50, 1945, 1, 1, 3), 
('Homage to Catalonia',              14.00, 1938, 1, 1, 2),  
('Pride and Prejudice',              17.50, 1813, 2, 1, 2),  
('Emma',                             11.25, 1815, 2, 3, 2), 
('Palace Walk',                      22.00, 1956, 3, 2, 1),  
('Midaq Alley',                      13.75, 1947, 3, 2, 1), 
('Children of the Alley',            24.50, 1959, 3, 2, 1),  
('One Hundred Years of Solitude',    21.00, 1967, 4, 3, 1),  
('Love in the Time of Cholera',      10.50, 1985, 4, 3, 1);  
GO

INSERT INTO MEMBER (name, email, join_date) VALUES
('Ahmed Hassan',   'ahmed.hassan@example.com',   '2026-01-10'), 
('Sara Ali',       'sara.ali@example.com',       '2026-02-14'),  
('Omar Khaled',    'omar.khaled@example.com',    '2026-03-05'), 
('Nour Mostafa',   'nour.mostafa@example.com',   '2026-04-20'),  
('Youssef Adel',   'youssef.adel@example.com',   '2026-05-01');  
GO


INSERT INTO LOAN (book_id, member_id, loan_date, return_date) VALUES
(1, 1, '2026-09-01', '2026-09-15'),
(1, 2, '2026-09-20', '2026-10-04'),
(1, 3, '2026-10-10', '2026-10-24'),
(1, 1, '2026-11-01', NULL),         
(4, 1, '2026-09-05', '2026-09-19'),
(4, 2, '2026-10-02', '2026-10-16'),
(4, 4, '2026-10-20', NULL),        
(2, 1, '2026-09-25', '2026-10-09'),
(2, 2, '2026-10-12', '2026-10-26'),
(3, 1, '2026-10-15', '2026-10-29'),
(6, 4, '2026-10-05', '2026-10-19'),
(7, 3, '2026-11-03', '2026-11-10');
GO