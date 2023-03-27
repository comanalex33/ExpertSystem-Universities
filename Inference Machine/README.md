# Inference Machine

This is the inference machine for a expter system.

The inference machine:

- It is a server created in python
- It was implemented using `backward chaining`

## How it works

It has 3 dicferent parts:

- Knowledge Base
  - Gets data and rules from Firebase Realtime database
  - It also contains 2 methods for manipulating data, filterUniversities to create the final response and a function to check if the program is in the list of programs
- Channels Manager
  - This is used to keep information about each channel of communication
  - When someone starts the quiz, a token will be generated and a channel of communication is created
  - A channel contains:
    - `token` - an unique numeric id to differentiate the channels
    - `timestamp` - the time when the channel is created
    - `responses` - a list of booleans, which represent the orderes list of answers that were given
  - What can do:
    - Generate unique token
    - Check if all of the questions were answered
    - Update responses
    - Get response based on token and previous answers
    - Get results for token by filtering programs and universities
    - Cleanup channels by deleting channels with a life longer then an hour
- Web Server
  - It is a simple HTTP server with 3 types of GET endpoints:
    - `/start`
      - Will generate a token and the response will have the following format:
        ```json
        {
            "token": 1
        }
        ```
    - `/execute`
      - Will return the next question or an answer
      - It can be used in 2 modes:
        - Generate the first question using: `/execute?token=1`
        - Generate the next question/answer based on previous answer: `/execute?token=1&answer=true` (token = 1, answer = true)
      - Response format:
        ```json
        {
            "question": "true",
            "text": "Question from Firebase?"
        }
        ```
    - `/results`
      - Will return the results after filtering universities and programs
      - This will filter using `check` field from the question
      - The `check` field contains a check in jmespath format
      - Response format:
        ```json
        {
            "programs": [
                "Program 1",
                "Program 2",
            ],
            "universities": [
                {
                    "name": "University 1",
                    "country": "Romania",
                    "program": "Program 1",
                    "faculty": "Faculty 1"
                },
                {
                    "name": "University 2",
                    "country": "Romania",
                    "program": "Program 2",
                    "faculty": "Faculty 2"
                }
            ]
        }
        ```

## How data looks in Firebase

There are 3 sections in the databse:

- `programs`
  - A list of programs
  - Each program has:
    - `name` - Name of the program
    - a list of `characteristics`
- `universities`
  - A list of universities
  - Each university has:
    - `name` - Name of the university
    - `public` - The university is public or private
    - `country` - The country of the university
    - `faculties` - The list of faculties in the university
- `rules`
  - This is a tree structure that contains the rules
  - Each rule has:
    - A `condition` (which contains a `question` and a `check` in jmespath format) or an `answer`
    - `true` - If the question is true, this will be the next branch
    - `false` - If the question is false, this will be the next branch

Example:

```json
{
    "programs": [
        {
            "name": "Program 1",
            "characteristics": [
                "technical",
                "computer-skills",
                "problem-solving",
                "precision"
            ]
        },
        {
            "name": "Program 2",
            "characteristics": [
                "technical",
                "computer-skills",
                "problem-solving",
                "precision"
            ]
        },
        {
            "name": "Program 3",
            "characteristics": [
                "technical",
                "computer-skills",
                "problem-solving",
                "precision"
            ]
        }
    ],
    "universities": [
        {
            "name": "University 1",
            "public": true,
            "country": "Romania",
            "faculties": [
                {
                    "program": "Program 1",
                    "name": "Faculty 1"
                },
                {
                    "program": "Program 2",
                    "name": "Faculty 2"
                }
            ]
        },
        {
            "name": "University 2",
            "public": true,
            "country": "Romania",
            "faculties": [
                {
                    "program": "Program 1",
                    "name": "Faculty 3"
                },
                {
                    "program": "Program 3",
                    "name": "Faculty 4"
                }
            ]
        }
    ],
    "rules": {
        "condition": {
            "question": "Vrei sa continui sa studiezi in Romania?",
            "check": "[?country=='Romania']"
        },
        "true": {
            "condition": {
                "question": "Crezi ca te poti raporta la un program strict de lucru?",
                "check": "[?contains(characteristics, 'strict')]"
            },
            "true": {
                "condition": {
                    "question": "Iti place mai mult matematica in detrimentul istoriei?",
                    "check": "[?contains(characteristics, 'technical')]"
                },
                "true": {
                    "condition": {
                        "question": "Ti-ar placea mai mult sa ajuti oamenii in detrimentul societatii?",
                        "check": "[?contains(characteristics, 'helping-people')]"
                    },
                    "true": {
                        "answer": "MEDICINA"
                    },
                    "false": {
                        "condition": {
                            "question": "Iti place sa lucrezi pe calculator?",
                            "check": "[?contains(characteristics, 'computer-skills')]"
                        },
                        "true": {
                            "answer": "INFORMATICA"
                        },
                        "false": {
                            "answer": "MATEMATICA"
                        }
                    }
                },
                "false": {
                    "answer": "RELATII UMANE/POLITIST"
                }
            },
            "false": {}
        },
        "false": {}
    }
}
```

## Run the application locally

#### Install prerequisites

```sh
    pip install -r requirements.txt
```

#### Run application

```sh
    python 3 webserver.py
```

This will wun the server and this can be accessed on http://localhost:8000

## Build and run the application using Docker

```sh
    # Create docker image using Dockerfile
    docker build -t inference_machine:1.0 .

    # Run docker container
    docker run -d -p 8080:80 --name webserver --restart always inference_machine:1.0    
```
