-- CREATE TABLE public.Home_Values (
-- 	Home_Values_ID int NOT NULL AUTO_INCREMENT,
-- 	Zip code varchar(256) NOT NULL AS City,
-- 	State varchar(256),
-- 	Metro varchar(256),
-- 	County name varchar(256) AS County,
-- 	Date timestamp,
-- 	Home value ($ per m2) numeric(18,0) AS Home_Value($perm2),
-- 	CONSTRAINT Home_Values_pkey PRIMARY KEY (Home_Values_ID)

-- );
CREATE TABLE public.Home_Values (
	Home_Values_ID int NOT NULL AUTO_INCREMENT,
	City varchar(256) NOT NULL,
	State varchar(256),
	Metro varchar(256),
	County varchar(256),
	Date timestamp,
	Home_Value($perm2),numeric(18,0),
	CONSTRAINT Home_Values_pkey PRIMARY KEY (Home_Values_ID)

);

-- CREATE TABLE public.Rental_Values (
-- 	Rental_Values_ID int NOT NULL AUTO_INCREMENT,
-- 	ZIP Code numeric(18,0),
-- 	City varchar(256),
-- 	State varchar(256),
-- 	Metro varchar(256),
-- 	County varchar(256),
-- 	House type varchar(256) AS House_Type,
-- 	Price unit varchar(256) AS Price_Unit,
-- 	Date timestamp,
-- 	Rental value numeric(18,0) AS Rental_Value,
-- 	CONSTRAINT Rental_Values_pkey PRIMARY KEY (Rental_Values_ID)
-- );
CREATE TABLE public.Rental_Values (
	Rental_Values_ID int NOT NULL AUTO_INCREMENT,
	ZIP Code numeric(18,0),
	City varchar(256) NOT NULL,
	State varchar(256),
	Metro varchar(256),
	County varchar(256),
	House_Type varchar(256),
	Price_Unit varchar(256),
	Date timestamp,
	Rental_Value numeric(18,0),
	CONSTRAINT Rental_Values_pkey PRIMARY KEY (Rental_Values_ID)
);


-- CREATE TABLE public.Demographics(
-- 	City varchar(32),
-- 	State varchar(32), 
-- 	Race varchar(32), 
-- 	Count numeric(18,0),
-- 	Median Age numeric(18,0) AS Median_Age,
-- 	Male Population numeric(18,0) AS Male_Population,
-- 	Female Population numeric(18,0) AS Female_Population,
-- 	Total Population numeric(18,0) AS Total_Population,
-- 	"Number of Veterans" numeric(18,0) AS Veterans_Population,
-- 	"Foreign-born" numeric(18,0) AS Foreign_Born,
-- 	Average Household Size numeric(18,0) AS Avg_Household_Size,
-- 	State Code varchar(32) AS State_Code
-- );
CREATE TABLE public.Demographics(
	City varchar(32) NOT NULL,
	State varchar(32), 
	Race varchar(32), 
	Count numeric(18,0),
	Median_Age numeric(18,0),
	Male_Population numeric(18,0),
	Female_Population numeric(18,0),
	Total_Population numeric(18,0),
	Veterans_Population numeric(18,0),
	Foreign_Born numeric(18,0),
	Avg_Household_Size numeric(18,0),
	State_Code varchar(32)
);

CREATE TABLE public.City_Housing_Costs(
	City varchar(256) NOT NULL,
	State varchar(256),
	Metro varchar(256),
	County varchar(256),
	Home_Value numeric(18,0),
	Rental_Type varchar(256),
	Rental_Value numeric(18,0),
	Avg_Household_Size numeric(18,0)
);

CREATE TABLE public.City_Housing_Demographics (
	City varchar(256),
	State varchar(256),
	Home_Value numeric(18,0),
	Rental_Value numeric(18,0),
	Race varchar(256),
	Race_Count int64,
	Median_Age int64,
	Male_Population int64,
	Female_Population int64,
	Total_Population int64
);

