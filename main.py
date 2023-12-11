import asyncio
from owlready2 import *
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

async def main(openAIclient, prompt, query):
    completion = await openAIclient.chat.completions.create(model="gpt-3.5-turbo",
                                                      messages=[{"role": "user", "content": (prompt + query)[:4097]}])
    return completion.choices[0].message.content

if __name__ == "__main__":
    prompt = open('text.txt', mode='r').read()
    query = open('query.txt', mode='r').read()
    openAIclient = AsyncOpenAI(
        api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
    )
    exec(asyncio.run(main(openAIclient, prompt, query)))
    data = open('data.py', mode='w')
    print(data.write(asyncio.run(main(openAIclient, prompt, query))))
    # from data import *
    onto = get_ontology("geo.owl").load()
    print(countries)
    for country in countries:
        print(country)
        city = onto.settlement(country[0])
        city.label = []

    for settlement in settlements:
        print(settlement)
        city = onto.settlement(settlement[0])
        city.label = []
        # for label in settlement[1]:
        #     city.label.append(locstr(label[0], lang=label[1]))


        # if competency[2]:
        #     parent_skill = onto.Skill(competency[2])
        #     skill.isPartOf = [parent_skill]

    onto.save(file="geo.owl")