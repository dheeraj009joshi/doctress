# import facebook

# # Set up access token and initialize GraphAPI
# access_token = 'EAAPhkiVeKNEBOyVWtuGXS2UZBjm2ETCZCtvGHZBYJ3iv0J15rvRVjqmyZAeKymxZBZBnDzYu0Lx8iJ63VO6bCloT3csnjaIwNjwk0nfyGz8nvQu1mBJVEmLrpWL5nHiD1ZCNT2oHHRSztBsMjzNFn0HRAPZAZBjflgUqULuaPNk7EBFefr1Ku2NnRAJzwQzPZCLjDLA05WZCjPo9HNhOYmM5DbXNvXZCntGnJFk4383nwmAfK04M3jLkWAYl2Vy7FyW6ZCH1ZCYuAuxgZDZD'
# app_secret = '73d8fa2be400a42c11d41977d89e7acb'
# app_id = '1092442738534609'
# graph = facebook.GraphAPI(access_token=access_token, version='3.1')

# # Example: Retrieving ad campaigns
# ad_campaigns = graph.get_object('me/adaccounts')
# for ad_account in ad_campaigns['data']:
#     campaigns = graph.get_object(f'{ad_account["id"]}/campaigns')
#     for campaign in campaigns['data']:
#         campaign_id = campaign['id']
#         # Example: Retrieving leads for each campaign
#         leads = graph.get_object(f'{campaign_id}/leadgen_forms')
#         for lead in leads['data']:
#             # Process leads here
#             print(lead)



# data={
#     "Monday":{
#         "9-13":["salesperson1",'salesperson2',"etc"],
#         "13-17":["salesperson1",'salesperson2',"etc"],
#     },
#     "Tuesday":{
#         "9-13":["salesperson1",'salesperson2',"etc"],
#         "13-17":["salesperson1",'salesperson2',"etc"],
#     }
# }

from datetime import datetime


def get_72_hours_before_leads(given_date_str):
    # Step 1: Obtain the current date and time
    current_datetime = datetime.today()
    print(current_datetime)
    # Step 2: Determine the given date
    given_datetime = datetime.strptime(given_date_str, "%m/%d/%Y")
    print(given_datetime)
    # # Step 3: Calculate the difference in hours
    # time_difference = current_datetime - given_datetime

    # # Step 4: Convert the difference to hours
    # hours_difference = time_difference.total_seconds() / 3600

    # # Step 5: Check if the difference is within 72 hours
    if current_datetime > given_datetime:
        return True
    else:
        return False
print(get_72_hours_before_leads("05/22/2024"))