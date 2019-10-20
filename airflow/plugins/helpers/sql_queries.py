class SqlQueries:
    
    Home_Values_table_insert = ("""
        SELECT 
             Home_Values_ID int NOT NULL AUTO_INCREMENT,
             Zip code AS City,
             State,
             Metro,
             County name AS County,
             "Home value ($ per m2)" AS Home_Value($perm2)
        FROM Home_Values
        GROUP BY YEAR(Date)
    """)

    Rental_Values_table_insert = ("""
        SELECT 
            Rental_Values_ID int NOT NULL AUTO_INCREMENT,
            ZIP Code,
            City,
            State,
            Metro,
            County,
            "House type" AS House_Type,
            "Price unit" AS Price_Unit,
            "Rental value" AS Rental_Value,
        FROM Rental__Values
        GROUP BY YEAR(Date)
    """)

    Demographics_table_insert = ("""
        SELECT 
            City,
            State, 
            Race, 
            Count AS Race_Count,
            "Median Age" AS Median_Age,
            "Male Population" AS Male_Population,
            "Female Population" AS Female_Population,
            "Total Population" AS Total_Population,
            "Number of Veterans" AS Veterans_Population,
            "Foreign-born" AS Foreign_Born,
            "Average Household Size" AS Avg_Household_Size,
            "State Code" AS State_Code
        FROM Demographics
    """)

    City_Housing_Demographics_table_insert = ("""
            SELECT 
                Home_Values.City,
                Home_Values.State, 
                Home_Values.Home_Value,
                Rental_Values.Rental_Value,
                Demographics.Race,
                Demographics.Median_Age,
                Demographics.Male_Population,
                Demographics.Female_Population ,
                Demographics.Total_Population ,
            FROM 
                Home_Values
            JOIN Rental_Values
                ON Home_Values.City = Rental_Values.City
            JOIN Demographics
                ON Demographics.City = Home_Values.City 
            ORDER BY City
    """)

    City_Housing_Costs_table_insert = ("""
        SELECT 
            Home_Values.City,
            Home_Values.State, 
            Home_Values.Metro,
            Home_Values.County,
            Home_Values.Home_Value,
            Rental_Values.House_Type AS Rental_Type,
            Rental_Values.Rental_Value,
            Demographics.Avg_Household_Size
        FROM 
            Home_Values
        JOIN Rental_Values
            ON Home_Values.City = Rental_Values.City
        JOIN Demographics
            ON Demographics.City = Home_Values.City 
        ORDER BY City
    """)

    