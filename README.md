# AutoFolder (WIP)

Python Script to move files from one folder to another and apply transformations along the way.

## Concept

With some simple yet powerful configuration, files can be move from one directory to another and have a number of transformation apply including but not limited to:

- Converting file type _i.e mp4 -> gif_
- Unzipping zipped files.
- Renaming files
- Filter out certain images sizes.
- Segment files based on duration _(video file types only.)_

Tasks are configured in a pipeline where the first task is fed the contents of the source directory and subsequent steps retrieve the most up to date version of the directory.

## Config

### Top Level

There are 4 top level configuration options at the moment:

- Source Directory -> The source directory of the files
- Output Directory -> The output of the files after all tasks have run.
- Files Masks -> Collections of MIME types grouped under an ID so they can be referenced easily.
- Pipeline -> An array of subsequent steps that will happen to the source directory before the eventual contents are copied to another directory.

Each task in the pipeline has it's their own config options.

### Pipeline Task

There are 4 main config options for a pipeline task:

- ID -> An identifier for the step taking place.
- File Mask -> This can be an array of the mime types for the task to operate on OR an ID of a file mask configured at the top level.
- Task -> The name of the task you want to run. These will perform certain operations based on the arguments provided.
- Arguments -> This is an object with the keys being the corresponding parameter name and the value being the argument value.
- Filters -> Logical filters that filter out files based on conditional values.

## Tasks

The current lists of tasks includes:

- Converting File type
- Unzipping files
- Renaming Files
- Deleting files
- Segmenting

## Filters

WIP

## Basic process:

For a given pipeline task, the following steps will be run:

1. The directory data will be updated with all files that fit inside the file mask for this task.
2. Any filters that are to be applied will be applied to the above dataset.
3. Finally, the task will be run with the above data. If an iterator is present the step will be run multiple times _(for the same file)_ based on the configuration.
4. If another step is present, the process begins again for that step's transformation. Else, autofolder will begin to dump the source directory to the output directory.
