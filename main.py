import asyncio
from owlready2 import *
from openai import OpenAI
import os
from dotenv import load_dotenv
from geo import *
# import getdata
load_dotenv()

async def main(openAIclient, prompt, query):
    completion = await openAIclient.chat.completions.create(model="gpt-3.5-turbo",
                                                      messages=[{"role": "user", "content": (prompt + query)}])
    return completion.choices[0].message.content

if __name__ == "__main__":
    # prompt = open('text.txt', mode='r').read()
    # query = open('query.txt', mode='r').read()
    # openAIclient = OpenAI(
    #     api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
    # )
    # exec(asyncio.run(main(openAIclient, prompt, query)))
    # data = open('data.py', mode='w')
    # completion = openAIclient.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": (prompt + query)[:4097],
    #         }
    #     ],
    #     model="gpt-3.5-turbo",
    # )
    # print(completion.choices[0].message.content)
    # data.write(completion.choices[0].message.content)

    # data = open('geo.py', mode='r').read()
    # classes = ['countries', 'regions', 'districts', 'settlements', 'objects']
    # properties = ['countries_regions', 'regions_settlements ', 'regions_objects']
    # for clss in classes:
    #     x = re.findall(clss + r' = \[.*\]', data, re.DOTALL)[0]
    #     if x:
    #         print(x)
    #         exec(x[0])
    # exit()
    # for prop in properties:
    #     x = re.findall(prop + r' = \[.*\]', data, re.DOTALL)
    #     if x:
    #         print(x)
    #         exec(x[0])

    onto = get_ontology("empty.rdf").load()

    # Adding countries with multilanguage labels to ontology
    for country in countries:
        print(country)
        country_individual = onto.Country(country[0])
        country_individual.label = []
        for label in country[1]:
            country_individual.label.append(locstr(label[0], lang=label[1]))
    # Adding regions with multilanguage labels to ontology
    for region in regions:
        print(region)
        region_individual = onto.Region(region[0])
        region_individual.label = []
        for label in region[1]:
            region_individual.label.append(locstr(label[0], lang=label[1]))
    # Adding properties that adds region into country in ontology
    for country_region in countries_regions:
        country_individual = onto.Country(country_region[1])
        region_individual = onto.Region(country_region[0])
        region_individual.isPart = [country_individual]

    for settlement in settlements:
        print(settlement)
        settlement_individual = onto.Settlement(settlement[0])
        settlement_individual.label = []
        for label in settlement[1]:
            settlement_individual.label.append(locstr(label[0], lang=label[1]))

    for region_settlement in regions_settlements:
        region_individual = onto.Region(region_settlement[1])
        settlement_individual = onto.Settlement(region_settlement[0])
        settlement_individual.isPart = [region_individual]

    for obj in objects:
        print(obj)
        obj_individual = onto.Object(obj[0])
        obj_individual.label = []
        for label in obj[1]:
            obj_individual.label.append(locstr(label[0], lang=label[1]))

    for region_object in regions_objects:
        region_individual = onto.Region(region_object[1])
        object_individual = onto.Object(region_object[0])
        object_individual.isPart = [region_individual]

    onto.save(file="geoold.owl")