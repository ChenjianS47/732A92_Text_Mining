from google_play_scraper import Sort, reviews_all
import pandas as pd



def scrap_data(score,data_csv,country):
    result = reviews_all(
        'com.miHoYo.GenshinImpact',
        sleep_milliseconds=0,  # defaults to 0
        lang='en',  # defaults to 'en'
        country=country,  # defaults to 'us'
        sort=Sort.MOST_RELEVANT,  # defaults to Sort.MOST_RELEVANT
        filter_score_with=score  # defaults to None(means all score)
    )

    for i in range(len(result)):
        temp = pd.DataFrame({'Time': result[i]["at"], 'Score': result[i]["score"], 'Content': result[i]['content']},
                            index=[0])

        data_csv = data_csv.append(temp, ignore_index=True)
        pass
    return data_csv

def scrap_data_to_csv(country):
    data_csv = pd.DataFrame(columns=['Time', 'Score', 'Content'])

    print('Scrapping 5 score data')
    data_csv = scrap_data(5, data_csv, country)

    print('Scrapping 4 score data')
    data_csv = scrap_data(4, data_csv, country)

    print('Scrapping 3 score data')
    data_csv = scrap_data(3, data_csv, country)

    print('Scrapping 2 score data')
    data_csv = scrap_data(2, data_csv, country)

    print('Scrapping 1 score data')
    data_csv = scrap_data(1, data_csv, country)

    print('Saving data')

    data_len = len(data_csv)

    filename = 'data_' + (str(data_len )[:2]) + 'k_' + country + '.xlsx'

    data_csv.to_excel(filename, index=False)
    pass

scrap_data_to_csv('gb')


