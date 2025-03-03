import openai
import asyncio

#Function that passes each review to ChatGPT to analyze.
# Returns: {}
async def run_gpt(api_openai, element):
    openai.api_key = api_openai

    prepared_meal = """You receive: Customer review.
Your tasks: 1) Analyze the review's text and rate its attitude from 1 to 5 (1 - Very negative, 2 - Negative, 3 - Neutral, 4 - Positive, 5 - Very positive). Result should be a number.
2) Identify emotions relevant to the text (choose from 1 to 3 from: Appreciative, Casual, Critical, Enthusiastic, Funny, Informative, Passionate, Worried, Urgent).Emotions separated with ",". 3) If a problem is mentioned in the review or you can see from the review what can be improved in the business, provide recommendations to the business owner. Keep it short, recommendation should consist of bullet points. If no problems are mentioned, use a hyphen (-) for the recommendation. Result should be your recommendation
You return: answers to all 3 tasks separeted by "|" in order.
The input:\n{}""".format("Title of the review was: " + element["Title"] + "\nBody  of the review was: "+ element["Body"])

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Imagine that you are a sentiment analysis machine."},
            {"role": "user", "content": prepared_meal}
        ]
    )

    response = completion.choices[0].message.content
    values = [container.strip() for container in response.split('|')]
    values[1] = values[1].replace(" ","").split(",")

    element["Attitude"] = values[0]
    element["Emotions"] = values[1]
    element["Recommendation"] = values[2]
    print("Run was successful for the {}!!!".format(element["Name"]))
    print("The VALUE of values was ", values)
    return element
    await asyncio.sleep(20) # this is a temporary solution for GPT Free plan.



# Temporary process_elements function for the Free GPT version
async def process_elements(api_openai, reviews):
    result = []
    for element in reviews:
        await asyncio.sleep(20)  # Delay for 20 seconds before running the next 'run_gpt'
        result.append(await run_gpt(api_openai, element))
    return result