-- Category tablosuna veri ekleme
INSERT INTO Category (Title) VALUES
('Artificial Intelligence'),
('Cyber Security'),
('Cloud Computing'),
('Data Science'),
('Software Engineering'),
('Machine Learning'),
('Internet of Things'),
('Blockchain'),
('Quantum Computing'),
('Big Data');

-- Conference tablosuna veri ekleme
INSERT INTO Conference (Title, StartDate, EndDate, Location, Organizer) VALUES
('AI Summit 2025', '2025-05-10', '2025-05-12', 'New York, USA', 'TechWorld'),
('CyberSec Expo 2025', '2025-06-15', '2025-06-17', 'Berlin, Germany', 'CyberSec Inc.'),
('CloudCon 2025', '2025-07-20', '2025-07-22', 'London, UK', 'CloudTech'),
('Data Analytics Forum', '2025-08-05', '2025-08-07', 'Paris, France', 'DataCorp'),
('Software Dev Summit', '2025-09-12', '2025-09-14', 'San Francisco, USA', 'DevCon'),
('ML Conference', '2025-10-18', '2025-10-20', 'Tokyo, Japan', 'ML Innovators'),
('IoT Innovations', '2025-11-08', '2025-11-10', 'Dubai, UAE', 'IoT Global'),
('Blockchain Revolution', '2025-12-01', '2025-12-03', 'Singapore', 'CryptoTech'),
('Quantum Computing Symposium', '2026-01-15', '2026-01-17', 'Zurich, Switzerland', 'Quantum Labs'),
('Big Data Analytics', '2026-02-10', '2026-02-12', 'Toronto, Canada', 'BigData Inc.');

-- Hall tablosuna veri ekleme
INSERT INTO Hall (Capacity) VALUES
(200), (150), (300), (250), (180), (220), (270), (320), (400), (500);

-- Speaker tablosuna veri ekleme
INSERT INTO Speaker (FirstName, LastName, Bio, Email, Phone, PhotoUrl) VALUES
('John', 'Doe', 'AI researcher and keynote speaker.', 'johndoe@example.com', '+1 123-456-7890', 'https://example.com/johndoe.jpg'),
('Alice', 'Smith', 'Cybersecurity expert.', 'alicesmith@example.com', '+1 987-654-3210', 'https://example.com/alicesmith.jpg'),
('Bob', 'Johnson', 'Cloud solutions architect.', 'bobjohnson@example.com', '+44 7890-123456', 'https://example.com/bobjohnson.jpg'),
('Emily', 'Davis', 'Data scientist and analyst.', 'emilydavis@example.com', '+33 612-345-678', 'https://example.com/emilydavis.jpg'),
('Michael', 'Brown', 'Software engineering specialist.', 'michaelbrown@example.com', '+49 152-987-6543', 'https://example.com/michaelbrown.jpg'),
('Sarah', 'Wilson', 'Machine learning engineer.', 'sarahwilson@example.com', '+81 90-1234-5678', 'https://example.com/sarahwilson.jpg'),
('David', 'Martinez', 'IoT hardware developer.', 'davidmartinez@example.com', '+971 50-9876543', 'https://example.com/davidmartinez.jpg'),
('Jessica', 'Taylor', 'Blockchain researcher.', 'jessicataylor@example.com', '+65 9123-4567', 'https://example.com/jessicataylor.jpg'),
('Daniel', 'Anderson', 'Quantum computing specialist.', 'danielanderson@example.com', '+41 78-901-2345', 'https://example.com/danielanderson.jpg'),
('Sophia', 'Thomas', 'Big data analytics expert.', 'sophiathomas@example.com', '+1 613-555-0199', 'https://example.com/sophiathomas.jpg');

-- Paper tablosuna veri ekleme (ConferenceId eklendi)
INSERT INTO Paper (Title, SpeakerId, CategoryId, Duration, Description, HallId, ConferenceId) VALUES
('Future of AI in Healthcare', 1, 1, 45, 'Discussion on AI-driven medical advancements.', 1, 1),
('Cyber Threats in 2025', 2, 2, 40, 'Analyzing emerging cybersecurity risks.', 2, 2),
('Scalability in Cloud Computing', 3, 3, 50, 'Techniques to improve cloud scalability.', 3, 3),
('Deep Learning Applications', 4, 6, 55, 'Exploring real-world deep learning models.', 4, 6),
('Best Practices in Software Dev', 5, 5, 60, 'Modern software engineering methodologies.', 5, 5),
('IoT in Smart Cities', 7, 7, 35, 'Implementing IoT solutions for urban development.', 6, 7),
('Blockchain and Privacy', 8, 8, 40, 'Enhancing privacy using blockchain.', 7, 8),
('Quantum Computing Algorithms', 9, 9, 50, 'New approaches in quantum computing.', 8, 9),
('Big Data in Business', 10, 10, 45, 'Using big data analytics for business growth.', 9, 10),
('AI-Powered Cyber Defense', 1, 2, 60, 'How AI can revolutionize cybersecurity.', 10, 2);
