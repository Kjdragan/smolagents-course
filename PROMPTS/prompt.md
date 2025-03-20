Search for the latest news from AI in the last week. Write a comprehensive report in markdown and save it to copypasta.md on my desktop

Get the transcript from this video.  It is an instructional video.  Make a markdown list of the instructions and save it to instruction_video.md on my desktop.  https://www.youtube.com/watch?v=LYMwLixmTZQ

it looks like we can run our project like this:
 .\.venv\Scripts\python.exe -m src.llm_router_client_revised4 --model claude-3-5-haiku-latest
or
.\run_client.ps1 -DebugMode

what are best practices.  I want to do that, and keep all the functionalty for modifiers like model selection and debug both in the cli and ant runtime.


I started a new chat because you don't seem to be able to solve this issue. Take a look at my project fresh. You can review the documentation, You should go through the source code and the associated files. The issue we are having is with logging. Right now we are, when we run our code, we are creating two log directories under the C:\Users\kevin\repos\fresh_client\logs. Each session we run creates its own subdirectory with a custom ID number and a date time for the session run. All our log files are saved in that special description blog file.. We should only be creating one of these log directories. per session.. However right two are being created. The first log directory that is being created is very incomplete, But the second one that's being created  ialmost immediately thereafter thats pretty much fully complete except for there is a sub directory called session states and that session states folder should have the state of the context upon completion of each step iterated as we try to solve our query.  Right now, both logs are creating that folder, but neithjer is creating the individual session state files for each of those. So at the end of the day, we only want one log directory, and the second one we created seems to be the complete one, yet we don't seem to be able to get the session states saved into that second directory. We don't seem to be able to fix the initial log directory so that we only have one. One thing I noticed is that there are three files that mention session states. @process_session_states.py@session_state_manager.py@session_state_processor.py. Make sure you investigate each of these because they may be duplicative or broken.
