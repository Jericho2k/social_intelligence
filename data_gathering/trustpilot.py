import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from gpt.chatgpt import process_elements
#from core.tg_functionality import send_notification

#Date modification function
def date_modifier(date): # MONTH/DAY/YEAR
    result = ""
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    specific_case = ['day', 'hour', 'hours', 'days']

    day = ""
    month = ""

    date = date.replace(",", "")
    date_cut = date.split(" ")
    if ('Updated' in date_cut):
        date_cut.remove('Updated')



    if  ((specific_case[0] not in date_cut) and
         (specific_case[1] not in date_cut) and
         (specific_case[2] not in date_cut) and
         (specific_case[3] not in date_cut)): 
        date_cut[0] = str(int(month_list.index(date_cut[0])) + 1)
        result = date_cut[0] + "/" + date_cut[1] + "/" + date_cut[2]
        return result
    elif ((specific_case[0] in date_cut)): # day
        result = str(datetime.today() - timedelta(days=1))
    elif ((specific_case[3] in date_cut)): # days
        result = str(datetime.today() - timedelta(days=int(date_cut[0])))
    elif ((specific_case[2] in date_cut)): # hours
        result = str(datetime.today() - timedelta(hours=int(date_cut[0])))
    else:                                  # hour
        result = str(datetime.today() - timedelta(hours=1))

    if result[5] == '0':
        month = result[6:7]
    else:
        month = result[5:7]    
    if result[8] == '0':
        day = result[9:10]
    else:
        day = result[8:10]    

    result = '{}/{}/{}'.format(month,day,result[:4])  

    return result

#Main function
async def get_trustpilot_reviews(url, proxy_server, proxy_port, proxy_login, proxy_pass, api_openai, reviews_limit):
    print("Entered ASYNC Function")
    try:
        
        proxies = {
            'http': 'http://{}:{}@{}:{}'.format(proxy_login, proxy_pass, proxy_server, proxy_port)
            #'https': 'https://{}:{}@{}:{}'.format(proxy_login, proxy_pass, proxy_server, proxy_port)
        }

        final_url = url + "?sort=recency"

        # Send a GET request to the URL
        response = requests.get(final_url, proxies=proxies) #  headers=header,

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the review containers
        review_containers = soup.find_all("div",
                                        class_="styles_reviewCardInner__EwDq2")


        # Extract the required information from each review container
        reviews = []
        
        container = 0

        while ((container < len(review_containers)) and (container + 1 <= reviews_limit)):
            #Extract reviewer's name
            reviewer_name = review_containers[container].find("span",
                                            class_="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17"
                                            ).text.strip()

            #Extract given rating
            review_rating = int(review_containers[container].find("div",
                                        class_="styles_reviewHeader__iU9Px"
                                        )['data-service-review-rating'])
            
            #Extract Review title
            review_title = review_containers[container].find("h2",
                                            class_="typography_heading-s__f7029 typography_appearance-default__AAY17"
                                            ).text.strip()
            
            #Extract Review body
            try:
                review_body = review_containers[container].find("p",
                                                class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
                                                ).text
            except:
                    review_body = ""    
            
            #Extract Review date/time
            review_time = str(review_containers[container].find("time").text.replace(",",""))

            #Adding to our main file
            reviews.append({"Name": reviewer_name,
                            "Rating": review_rating,
                            "Title": review_title,
                            "Body": review_body,
                            "Time": date_modifier(str(review_time)),
                            "Attitude": "This data is still being processed...",
                            "Emotions": "This data is still being processed...",
                            "Recommendation": "This data is still being processed...",
                            "Source": "Trustpilot",
                            "Url": final_url
                            })
            
            container+=1

        #Extract Number of review pages
        number_of_pages_raw = soup.find("div",
                                        class_="styles_pagination__6VmQv"
                                        )
        for number in number_of_pages_raw:
            try:
                n = [x.text for x in number.find_all("span",
                                class_="typography_heading-xxs__QKBS8 typography_appearance-inherit__D7XqR typography_disableResponsiveSizing__OuNP7"
                                )]
                
            except:
                pass

        number_of_pages = int(n[len(n) - 2]) # the last one is "Next Page", so we ignore that and get the one before





        #Getting reviews from all other pages. Starting from 2nd
        page_counter = 2
        try:
            #Checking for more pages of reviews
            while (page_counter<=number_of_pages) and (container + 1 <= reviews_limit):
                sec_url = url + "?page={}".format(page_counter) + "&sort=recency"

                proxies = {
                    'http': 'http://{}:{}@{}:{}'.format(proxy_login, proxy_pass, proxy_server, proxy_port)
                    #'https': 'https://{}:{}@{}:{}'.format(proxy_login, proxy_pass, proxy_server, proxy_port)
                }

                response = requests.get(sec_url, proxies=proxies)
                soup = BeautifulSoup(response.content, "html.parser")
                review_containers = soup.find_all("div", class_="styles_reviewCardInner__EwDq2")
                container_local = 0
                while ((container_local < len(review_containers)) and (container + 1 <= reviews_limit)):
                    reviewer_name = review_containers[container_local].find("span",
                                                    class_="typography_heading-xxs__QKBS8 typography_appearance-default__AAY17"
                                                    ).text.strip()
                    review_rating = review_containers[container_local].find("div",
                                                class_="styles_reviewHeader__iU9Px"
                                                )['data-service-review-rating']
                    review_title = review_containers[container_local].find("h2",
                                                    class_="typography_heading-s__f7029 typography_appearance-default__AAY17"
                                                    ).text.strip()
                    try:
                        review_body = review_containers[container_local].find("p",
                                                        class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
                                                        ).text
                    except:
                        review_body = ""    
                    review_time = str(review_containers[container_local].find("time").text.replace(",",""))
                    
                    #Adding to our main file
                    reviews.append({"Name": reviewer_name,
                            "Rating": review_rating,
                            "Title": review_title,
                            "Body": review_body,
                            "Time": date_modifier(str(review_time)),
                            "Attitude": "This data is still being processed...",
                            "Emotions": "This data is still being processed...",
                            "Recommendation": "This data is still being processed...",
                            "Source": "Trustpilot",
                            "Url": sec_url 
                            })
                    
                    container+=1
                    container_local+=1


                page_counter+=1    

        except Exception as error:
            pass

        print("Getting to the async function")
        processed_reviews = await process_elements(api_openai, reviews)
        print(processed_reviews)

        #send_notification(reviews, processed_reviews) - TG function to implement

    except Exception as e:
        pass