import timeit

from aiohttp import ClientSession
import asyncio

from bs4 import BeautifulSoup
from owlready2 import *
from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv
from data import *

# import getdata
load_dotenv()


async def get_html(url):
    async with ClientSession() as session:
        async with session.get(url=url) as response:
            page = await response.read()
            soup = BeautifulSoup(page, "html.parser")
            title = soup.find('span', class_='mw-page-title-main').contents[0]
            body = soup.find('div', class_='mw-content-ltr mw-parser-output')
            return str(title) + "\n" + str(body)




async def analyze_wiki(openAIclient, prompt, query):
    completion = await openAIclient.chat.completions.create(model="gpt-3.5-turbo", \
        messages=[{"role": "user", "content": (str(prompt)[:8000] + query)}])
    return completion.choices[0].message.content


async def main():
    prompt = await get_html('https://en.wikipedia.org/wiki/Geography_of_Kazakhstan')
    query = open('query.txt', mode='r').read()
    openAIclient = AsyncOpenAI(api_key=os.environ['OPENAI_API_KEY'])
    completion = await analyze_wiki(openAIclient, prompt, query)
    data = open('geo.py', mode='w')
    # print(completion)
    data.write(completion)


async def stats():
    prompt = await get_html('https://en.wikipedia.org/wiki/Geography_of_Kazakhstan')
    arrays = ['countries', 'regions', 'settlements', 'objects']
    errors = []
    for item in countries:
        if prompt.find(item[0].split()[0]) == -1:
            print(item[0].split()[0])
            errors.append(item[0].split()[0])
    for item in regions:
        if prompt.find(item[0].split()[0]) == -1:
            print(item[0].split()[0])
            errors.append(item[0].split()[0])
    for item in settlements:
        if prompt.find(item[0].split()[0]) == -1:
            print(item[0].split()[0])
            errors.append(item[0].split()[0])
    for item in objects:
        if prompt.find(item[0].split()[0]) == -1:
            print(item[0].split()[0])
            errors.append(item[0].split()[0])

    print('Elements total:', len(countries + regions + objects + settlements + countries_regions + regions_settlements + regions_objects))
    print('Errors:', len(errors))

if __name__ == "__main__":
    # prompt = await get_html('https://en.wikipedia.org/wiki/Geography_of_Kazakhstan')
    load_dotenv()
    start = timeit.timeit()
    asyncio.run(main())
    end = timeit.timeit()
    print(end - start)
    from geo import *
    asyncio.run(stats())