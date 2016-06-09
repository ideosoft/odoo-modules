from mikrotik import ApiRos
from pprint import pprint

def main():
    apiros = ApiRos('217.197.22.1');
    apiros.login('admin', 'Pandora@8192');
    x = apiros.writeSentence(['/ppp/secret/getall'])
    pprint(apiros.parse(x))

if __name__ == "__main__":
    main()