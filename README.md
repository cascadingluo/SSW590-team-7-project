The repository of team 8's project for CS555, this team includes, Luo Xu, Annanya Jain, Aya Salama, Spurthi Setty, Yanran Jia and Divya Prahlad from Stevens Institute of Technology.

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
- run the following commands

  - docker build -t ava:latest -f Dockerfile .
  - docker run -d -p 3000:3000 ava:latest

- go to your browser and navigate to localhost:3000 to see AVA in action!

log/track:

- Sprint 1:

  - Created a basic interface using HTML and CSS, not yet integrated with the backend. ✅
  - Developed a functional backend that supports both voice-to-text and text input. ✅
  - Implemented a simple chat response system to showcase basic functionality within a minimal interface. ✅

- Sprint 2:
  - Intergrating the Backend and Frontend, shows the basic functionalities developed in sprint 1 with the actual front end. ✅
  - Further development of the Backend with Voice output and better Voice Input Recognition, Fine-tuning the assistant and using the Q/A document for accurate responses. ✅
  - See Jira for specific user stories. ✅
- Sprint 3:
  -
- Sprint 4:
  - starting in 4 weeks
