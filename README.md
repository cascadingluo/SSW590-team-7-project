The repository of team 7's project for SSW590, this team includes, Luo Xu, Annanya Jain, and Gavin Lam. 

This repository is a modification and continuation of the project for CS555 created by Luo Xu, Annanya Jain, Aya Salama, Spurthi Setty, Yanran Jia and Divya Prahlad from Stevens Institute of Technology.

This goal of this project is to create an AI voice chatbot that the user can interact with to talk about mental health problems and surface level physical health problems.

**_important! instructions to run:_**
the basic chatbot functions:

- in the AVA file run:
  ```bash
    pip install -r requirements.txt
    python3 app.py
  ```

head to http://127.0.0.1:3000 to see AVA in action!

make sure you have the packages below when running:

**_important! instructions to run with Docker:_**

- after cloning repository, navigate to the AVA folder
- open docker
- run the following commands
  ```bash
    docker build -t ava:latest -f Dockerfile .
    docker run -d -p 3000:3000 ava:latest
  ```

- go to your browser and navigate to localhost:3000 to see AVA in action!

