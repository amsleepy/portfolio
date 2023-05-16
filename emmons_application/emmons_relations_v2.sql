CREATE TABLE ZipCode (
    num CHAR(5),
    city_name VARCHAR(50) NOT NULL,             --is_in relation
    state_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (num)
);

CREATE TABLE ZipData (
    zipcode CHAR(5),
    medianIncome INTEGER,
    avgIncome INTEGER,
    population INTEGER,
    PRIMARY KEY (zipcode)
);

CREATE TABLE Business (
    bid VARCHAR(50),
    business_name VARCHAR(200),
    zip VARCHAR(5) NOT NULL,
    state_name VARCHAR(50) NOT NULL,
    city_name VARCHAR(50) NOT NULL,
    checkins INTEGER,
    numReviews INTEGER,
    stars DECIMAL(2,1),
    avgRating DECIMAL(2,1)
    CONSTRAINT stars CHECK (stars BETWEEN 0 and 5),
    CONSTRAINT avgRating CHECK (avgRating BETWEEN 0 and 5),
    business_address VARCHAR(200),     --is_in relation
    isPopular BOOLEAN,
    isSuccessful BOOLEAN,
    PRIMARY KEY (bid)
);

CREATE TABLE Review (
    review_Id VARCHAR(50),
    review_date DATE,
    stars INTEGER,
    review_text TEXT,
    business VARCHAR(200),
    CONSTRAINT stars CHECK (stars BETWEEN 0 and 6),  
    PRIMARY KEY (review_Id),
    FOREIGN KEY (business) REFERENCES Business(bid)
);

CREATE TABLE Categories (
    business_id VARCHAR(50),
    category VARCHAR(50),
    PRIMARY KEY (business_id, category)
);