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
- There will be at least an hour sitting in "How do you even do these kinds of things in VSCode without losing your mind?" such as managing git.
    - Note: I eventually just started to do everything in the command line. It's just easier for me at this point. I'm a Sublime Text kind of girl anyhow.
- By the turn execution stage, I've roughly spent three hours on the actual work.
    - I've spent another thirty or so minutes on handling things in Github, or reading how to leverage MongoDB + Pydantic correctly.
- By the final commit to MVP, I've spent roughly five hours on the project specifically.
    - Had I been wiser, I wouldn't have tried to be fancy with dynamic first turns or other similar functionality.
    - I also spent hours reading up on MongoDB, Pydantic, PyMongo, details around document storage in MongoDB, feeling immense disppointment at overloading Game ID with the object ID in Mongo and more.    

## Trade-offs 
- The most apparent trade off I made was around unit testing.
    - I could spend time implementing a unit test framework, but I've not done it before, and this seems like not the wrong time to try and figure out what I'd like to use.
    - Timed exercises like this aren't good candidates for unit testing/integration testing.
        - I'd argue you can easily do this, if you're consistently using the language and framework. I've not really been doing development as my primary role in nearly three or four years. And it definitely hasn't been in python at any point.
            - I'm a casual polyglot who speaks _(poorly)_ in several different scripting languages, I'm not really what I'd consider an expert of any of them. 
            - For the record, I most recently developed in HCL with Terraform, if you'd consider that development. (I hope we do!)
- I wanted to dynamically select the first player, between the CPU and the human.
    - This didn't really work out the way I wanted it to work out in the end. That's okay, but still frustrating.
    - I think if I hadn't felt the time pressure, I would have continued down the path I was on, but refactored some pieces.
    - The code is currently very messy, by my own standards. I would much prefer more files, isolation of functions, and far fewer imports in the game.py file.

## What did I do that was different than others?
- Without seeing what most people do, I think that my strong desire to use a real database (MongoDB) instead of a flat file costed me tons of time, but reflects a far more "realistic" situation.
    - Most people would absolutely know better than to say "You only have four hours to do something, you should totally deploy a production quality database to store this on your personal gaming computer!"
        - And now we know that I'm the kind of person who _would_ do that. And that's likely exceptional considering there's no need to bother with it in the requirements.
            - Not to mention it would have saved me tons of headache.
    - I think leveraging FastAPI is something that most people would do, or something similar in Django, Flask or otherwise.
        - I have seen FastAPI thrown around in my current job, and I wanted to use it because I never coded with it before. So maybe that's exceptional in it's own kind of way.
    - Commentary in the code should make it understandable by actual humans.
        - Something I feel that is almost always lost along the way with code, is the very important fact that code itself is for _humans_ not for computers. Compilers, interpreters, VMs and the like are all running highly optimized versions of the code we actually write by doing either live or compiled optmizations that would make it otherwise completely indecipherable from what normal people would read.
        - I would like to think that a human could wake up at 3:00AM, and debug this code (I'm sure there's _something_ wrong I could find in here.) because it's written to be human friendly.
            - Except for the spacing/structure inside of the validation function. That was a horrid `DRY` failure on my part, but again, time pressure does things to people. (And I don't think we ever write great things under that kind of pressure. And I also think it's rare that we are put in a position where that needs to be the case, even in a start up.)
                - For the record, I think I've only needed to live-fire, code under extreme time pressure due a client coming into a damaged environment once, maybe twice. Which involved doing some helm work to stabilize an otherwise unhappy environment.        
