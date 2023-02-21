import pandas as pd


def fl_to_perc(val: float) -> float:
    return round(val * 100, 1)


def round_to_1(val: float) -> float:
    return round(val, 1)


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby("race")["race"].count()

    # What is the average age of men?
    average_age_men = round_to_1(df["age"][df["sex"] == "Male"].mean())

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = fl_to_perc(
        df["education"][df["education"] == "Bachelors"].count()
        / df["education"].count()
    )
    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[
        (df["education"] == "Bachelors")
        | (df["education"] == "Masters")
        | (df["education"] == "Doctorate")
    ]
    lower_education = df[
        (df["education"] != "Bachelors")
        & (df["education"] != "Masters")
        & (df["education"] != "Doctorate")
    ]
    # percentage with salary >50K
    higher_education_rich = fl_to_perc(
        higher_education["salary"][higher_education["salary"] == ">50K"].count()
        / higher_education["salary"].count()
    )
    lower_education_rich = fl_to_perc(
        lower_education["salary"][lower_education["salary"] == ">50K"].count()
        / lower_education["salary"].count()
    )
    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[df["hours-per-week"] == min_work_hours]
    rich_percentage = fl_to_perc(
        num_min_workers["salary"][num_min_workers["salary"] == ">50K"].count()
        / num_min_workers["salary"].count()
    )

    # What country has the highest percentage of people that earn >50K?
    list_of_countries = df.groupby("native-country")["native-country"].count().index
    temp_highest_earning_country_name = "None"
    temp_highest_earning_country_val = 0.0
    for country in list_of_countries:
        temp_val = (
            df["salary"][
                (df["salary"] == ">50K") & (df["native-country"] == country)
            ].count()
            / df["salary"][df["native-country"] == country].count()
        )
        if temp_val > temp_highest_earning_country_val:
            temp_highest_earning_country_val = temp_val
            temp_highest_earning_country_name = country

    highest_earning_country = temp_highest_earning_country_name
    highest_earning_country_percentage = fl_to_perc(temp_highest_earning_country_val)

    # Identify the most popular occupation for those who earn >50K in India.
    df_india_50k = df[(df["native-country"] == "India") & (df["salary"] == ">50K")]
    num_per_occupation = df_india_50k.groupby("occupation")["occupation"].count()
    top_in_occupation = num_per_occupation.idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%"
        )
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%"
        )
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%"
        )
        print("Country with highest percentage of rich:", highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
        )
        print("Top occupations in India:", top_in_occupation)

    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_in_occupation,
    }
