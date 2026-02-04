-- =====================================
-- DATABASE
-- =====================================
CREATE DATABASE IF NOT EXISTS seismic_db;
USE seismic_db;

-- =====================================
-- TABLE
-- =====================================
CREATE TABLE IF NOT EXISTS earthquakes (
id VARCHAR(50) PRIMARY KEY,
time DATETIME,
latitude FLOAT,
longitude FLOAT,
depth_km FLOAT,
magnitude FLOAT,
magType VARCHAR(20),
place TEXT,
status VARCHAR(20),
tsunami INT,
significance INT,
country VARCHAR(50),
continent VARCHAR(50),
year INT,
month INT,
day INT,
hour INT,
day_of_week VARCHAR(20),
depth_category VARCHAR(20),
mag_category VARCHAR(20),
is_shallow BOOLEAN,
is_major_eq BOOLEAN,
type TEXT,
types TEXT,
alert TEXT,
nst FLOAT,
rms FLOAT,
gap FLOAT
);

-- =====================================
-- ANALYSIS QUERIES
-- =====================================

-- Top strongest earthquakes
SELECT * FROM earthquakes ORDER BY magnitude DESC LIMIT 10;

-- Deepest earthquakes
SELECT * FROM earthquakes ORDER BY depth_km DESC LIMIT 10;

-- Shallow strong earthquakes
SELECT * FROM earthquakes
WHERE depth_km < 50 AND magnitude > 7.5;

-- Avg magnitude by magType
SELECT magType, AVG(magnitude)
FROM earthquakes
GROUP BY magType;

-- Year with most earthquakes
SELECT year, COUNT(*) FROM earthquakes
GROUP BY year ORDER BY COUNT(*) DESC;

-- Month highest earthquakes
SELECT month, COUNT(*) FROM earthquakes
GROUP BY month ORDER BY COUNT(*) DESC;

-- Day most earthquakes
SELECT day_of_week, COUNT(*) FROM earthquakes
GROUP BY day_of_week ORDER BY COUNT(*) DESC;

-- Hour distribution
SELECT hour, COUNT(*) FROM earthquakes
GROUP BY hour;

-- Top impact places
SELECT place, SUM(significance)
FROM earthquakes
GROUP BY place ORDER BY SUM(significance) DESC LIMIT 5;

-- Avg impact by alert
SELECT alert, AVG(significance)
FROM earthquakes GROUP BY alert;

-- Status distribution
SELECT status, COUNT(*) FROM earthquakes GROUP BY status;

-- Earthquake type distribution
SELECT type, COUNT(*) FROM earthquakes GROUP BY type;

-- Data type distribution
SELECT types, COUNT(*) FROM earthquakes GROUP BY types;

-- High station coverage
SELECT * FROM earthquakes WHERE nst > 100;

-- Tsunami per year
SELECT year, COUNT(*) FROM earthquakes
WHERE tsunami = 1 GROUP BY year;

-- Alert level distribution
SELECT alert, COUNT(*) FROM earthquakes GROUP BY alert;

-- Top countries by magnitude
SELECT country, AVG(magnitude)
FROM earthquakes
GROUP BY country ORDER BY AVG(magnitude) DESC LIMIT 5;

-- Shallow vs deep ratio
SELECT country,
SUM(depth_km < 70)/SUM(depth_km >= 70)
FROM earthquakes GROUP BY country;

-- Reliability worst events
SELECT * FROM earthquakes
ORDER BY (significance + depth_km) DESC LIMIT 20;

-- Deep focus regions
SELECT place, COUNT(*) FROM earthquakes
WHERE depth_km > 300
GROUP BY place ORDER BY COUNT(*) DESC;

-- Final count check
SELECT COUNT(*) FROM earthquakes;
