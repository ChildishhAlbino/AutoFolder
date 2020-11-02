# AutoFolder

Python Script to move files from one folder to another and apply transformations along the way.

## Concept

With some simple yet powerful configuration, files can be move from one directory to another and have a number of transformation apply including but not limited to:

- Converting file type _i.e mp4 -> gif_
- Unzipping zipped files.
- Renaming files
- Filter out certain images sizes.

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

- Converting File type (uses ffmpeg, will be multi-threaded)
- Unzipping files
- Renaming Files
- Deleting files
