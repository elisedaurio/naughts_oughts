# Naughts and Oughts

## How to Build
- Clone this repository. 
- Create a new MongoDB with a DB named `naughts` and a collection called `games`
- Install `fastapi`, and ensure any ports are configured correctly. (You can align this to the FastAPI defaults for sanity.)

## How to run
- Run the following command from the root directory
- `fastapi dev main.py`

## What was done that I can't see in this repo?
- This repo should be a fairly accurate indicator of time I spent on the work.
- There was roughly two hours not captured here in my figuring out how to develop on my personal Windows machine without tools like PyCharm.
- By the turn execution stage, I've roughly spent three hours on the actual work.
    - I've spent another thirty or so minutes on handling things in Github, or reading how to leverage MongoDB + Pydantic correctly.
- By the final commit to MVP, I've spent roughly four hours on the actual problem at hand, and much more on the tooling around it.
  
## Trade-offs 
- The most apparent trade off I made was around unit testing.
    - I could spend time implementing a unit test framework, but I've not done it before, and this seems like not the wrong time to try and figure out what I'd like to use.
    - Timed exercises like this aren't good candidates for unit testing/integration testing.
        - I'd argue you can easily do this, if you're consistently using the language and framework.
            - I'm a casual polyglot who speaks in several different scripting languages, I'm not really what I'd consider an expert of any of them. But I can utilize nearly any of them to fairly useful effect.
            - I most recently developed in HCL for Terraform.
- I wanted to dynamically select the first player, between the CPU and the human.
    - This didn't really work out the way I wanted it to work out in the end. That's okay, but still frustrating.
    - I think if I hadn't felt the time pressure, I would have continued down the path I was on, but ended up refactored some pieces instead.
    - I would much prefer more files, isolation of functions, and far fewer imports in the game.py file.

## What did I do that was different than others?
- I think that my strong desire to use a real database (MongoDB) instead of a flat file costed me tons of time, but reflects a far more "realistic" situation.
- I think leveraging FastAPI is something that most people would do, or something similar in Django, Flask or otherwise.
    - I have seen FastAPI thrown around in my current job, and I wanted to use it because I never coded with it before. So maybe that's exceptional in it's own kind of way.
- Commentary in the code should make it understandable by actual humans.
    - Something I feel that is almost always lost along the way with code, is the very important fact that code itself is for _humans_ not for computers.
    - Compilers, interpreters, VMs and the like are all running highly optimized versions of the code we actually write by doing either live or compiled optmizations that would make it otherwise completely indecipherable from what normal people would read.
- I would like to think that a human could wake up at 3:00AM, and debug this code (I'm sure there's _something_ wrong I could find in here.) because it's written to be human friendly.
    - Except for the spacing/structure inside of the validation function.       
