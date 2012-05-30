# Introduction

workflow is a minimalist file based workflow engine. It runs as a background and can automate certain tasks for you such as delete old files, email you when new files are create, run a script to process new files.

## Now to

- create a file workflow.config using the syntax below
- run workflow.py in that folder

## workflow options

- -f <path> the folder to monitor and process
- -s <seconds> the time interval between checks for new files

## workflow.config syntax

The workflow.config file consists of a series of rules with the following syntax

`name: pattern [time]: command`

where 
- `name` is the name of the rule
- `pattern` is a glob pattern for files to monitor
- `time` is a time in seconds only files modified before `time` seconds will be considered
- `command` is the command to execute for each file matching `pattern` created more than `time` seconds ago and not processed already. If the command ends in `&` it is executed in background else it blocks the workflow until completion. The name of the mathing file can be referred into the command with `$0`. Multiline commands can be continued with `\`.

## Examples of rules

### Delete all `*.log` files older tha one day

    delete_old_logs: *.log [1d]: rm $0

### Move all `*.txt` files older than one hour to other folder

    move_old_txt: *.txt [1h]: mv $0 otherfolder/$0

### Email me when a new `*.doc` file is created

    email_me_on_new_doc: *.doc: mail -s 'new file: $0' me@example.com < /dev/null

### Process every new `*.dat` file using a Python script

    process_dat: *.dat: python process.py $0

### Crate a simple finite state machine for each `*src` file

    rule1: *.src [1s]: echo $0.state1
    rule2: *.src [1s]: mv $0.state1 $0.state2
    rule3: *.src [1s]: mv $0.state2 $0.state3
    rule4: *.src [1s]: rm $0.state3

## Details

When a file matches a pattern, a new process is created to execute the corresponding command. The pid of the process is saved in `<filename>.<rulename>.pid`. This file is deleted when the process is completed. If the process fails the output log and error is saved in `<filename>.<rulename>.err`. If the process does not fail the output is stored in `<filename>.<rulename>.out`.

If file has already been processed according to a ceratin rule, this info is stored in a file `workflow.config` and it is not processed again unless:

- the mtime of the file changes (for example you edit or touch the file)
- the rule is cleaned up.

You can cleanup a rule with

    python workflow.py -c rulename

If the main workflow.py process is killed or crashes while some commands are being executed, they also are killed. You can find which file and rules where being processed by looking for `<filename>.<rulename>.pid` files. If you restart workflow.py those pid files are deleted.

If a rule results in an error and a `<filename>.<rulename>.err` is created, the file is not processed again according to the rule, unless the error file is deleted.

If a file is edited or touched and rule runs again, the `<filename>.<rulename>.out` will be overwritten.

Unless otherwise specified each file is processed 1s after it is last modified. It is possible that a different process is still writing the file but it is pausing more than 1s between writes (for example the file is being downloaded via a slow connection). In this case it is best to download the file with a different name than the name used for the patter and mv the file to the pattern matching name, after the write of the file is completed. This must be handled outside of workflow. Workflow has no way of knowing when a file is completed or not.

