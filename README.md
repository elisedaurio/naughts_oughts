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

## Trade-offs 
- The most apparent trade off I made was around unit testing.
    - I could spend time implementing a unit test framework, but I've not done it before, and this seems like not the wrong time to try and figure out what I'd like to use.
    - Timed exercises like this aren't good candidates for unit testing/integration testing.
        - I'd argue you can easily do this, if you're consistently using the language and framework. I've not really been doing development as my primary role in nearly three or four years. And it definitely hasn't been in python at any point.
            - I'm a casual polyglot who speaks _(poorly)_ in several different scripting languages, I'm not really what I'd consider an expert of any of them. 
            - For the record, I most recently developed in HCL with Terraform, if you'd consider that development. (I hope we do!)