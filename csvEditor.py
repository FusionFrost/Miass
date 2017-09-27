import csv
import io
import config
from SQLighter import  SQLighter
import re

def csv_dict_reader(text, user_id):
    """
    Read a text file (csv-text)
    """
    db_worker = SQLighter(config.database_contacts)
    reader = csv.DictReader(io.StringIO(text), delimiter=',')

    for line in reader:
        name = line['Name']
        birth = line['Birthday']
        resultName = re.sub('[^А-Яа-яA-Za-z ]', '', name)
        resultBirth = re.sub('[^-\wА-Яа-яA-Za-z.;0-9 ]', '', birth)
        if birth != '':
            if name != '':
                db_worker.insert_new_contacts(name, birth, user_id)
    db_worker.close()
