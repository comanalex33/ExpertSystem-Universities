import json
from time import sleep
from threading import Thread
import jmespath

import firebase_admin
from firebase_admin import credentials, db

FIREBASE_ACCESS_PERIOD = 30 * 60    # Time given in seconds

class KnowledgeBase:
    
    def __init__(self):
        cred = credentials.Certificate('theuniversity4you-firebase-adminsdk-rcpmy-786e5f2729.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://theuniversity4you-default-rtdb.firebaseio.com/'
        })
        self._access_Firebase(firstAccess=True)
        thread_FirebaseAccess = Thread(target=self._access_Firebase)
        thread_FirebaseAccess.start()
        # self.data = self._read_inputFile()
        # self.programs = self.data['programs']
        # self.universities = self.data['universities']
        # self.rules = self.data['rules']

    def _access_Firebase(self, firstAccess = False):
        
        databaseRef = db.reference('/')
        
        while True:
            try:
                if firstAccess == False:
                    sleep(FIREBASE_ACCESS_PERIOD)
                    
                data = databaseRef.get()
                self.programs = data['programs']
                self.universities = data['universities']
                self.rules = data['rules']
                print("Rules updated")
            except Exception:
                if firstAccess == True:
                    print("Cannot get the rules from Firebase")
                    exit(1)
                    
            if firstAccess:
                break
            
    def filter_universitiesPrograms(self, responses):
        recommandedUniversities = []
        programs = self.programs
        universities = self.universities
        rule = self.rules
        for response in responses:
            condition = str(rule['condition']['check'])
            if response == False:
                condition = condition.replace('?', '?!')
            if 'contains' in condition:
                programs = jmespath.search(condition, data=programs)
            else:
                universities = jmespath.search(condition, data=universities)
                
            if response == True:
                rule = rule['true']
            else:
                rule = rule['false']
                
        for university in universities:
            for faculty in university['faculties']:
                if self._contains_program(programs, faculty['program']):
                    recommandedUniversity = {
                        'name': university['name'],
                        'country': university['country'],
                        'program': faculty['program'],
                        'faculty': faculty['name']
                    }
                    recommandedUniversities.append(recommandedUniversity)
        recommandations = {
            'programs': [program['name'] for program in programs],
            'universities': recommandedUniversities
        }
        return recommandations
                
    def _contains_program(self, programs, programName):
        for program in programs:
            if program['name'] == programName:
                return True
        return False

    def _read_inputFile(self):
        try:
            with open('se.json') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print('File not found')
            exit(1)
        except json.JSONDecodeError:
            print('Invalid JSON format')
            exit(1)
