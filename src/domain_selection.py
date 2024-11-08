import requests
import os
from dotenv import load_dotenv

load_dotenv()

HACKERONE_API_TOKEN = os.getenv('HACKERONE_API_KEY')
if not HACKERONE_API_TOKEN:
    raise Exception('HackerOne API key not found')


def fetch_scoped_domains():
    headers = {
        'Authorization': f'Bearer {HACKERONE_API_TOKEN}',
        'Accept': 'application/json'
    }
    response = requests.get('https://api.hackerone.com/v1/hackers/programs', headers=headers)
    if response.status_code == 200:
        programs = response.json()['data']
        scoped_domains = []
        for program in programs:
            # Filter programs that offer bounties and have domains in scope
            if program['attributes']['bug_bounty_enabled']:
                domains = program['attributes']['domains']
                scoped_domains.extend(domains)
        return scoped_domains
    else:
        raise Exception('Failed to fetch programs from HackerOne')

domains = fetch_scoped_domains()
