# RMV_Data_Analysis
Analyzing police data to identify cases of misuse of facial recognition technology.

Contained in this repo are a few of the files that we have used to narrow down the number of police emails we are interested in examining. The actual data and many other python files are not included in this repo for privacy reasons. The full repository is also not included due to privacy reasons, so the files in this repo have been downloaded from the original and uploaded into this one. Will try to update this repo periodically if I get the chance :)

Also, a pre-emptive apology for how messy the code is. We pretty much only need to execute each file once to produce a new .json file with concentrated data, so we haven't been worrying about how pretty the code looks :(

All code is the result of a collaborative effort between myself, Anahitha, Andrea, and Mr. Boxer.

## File Structure
```
├── README.md
├── helpers.py          - helper functions
|
├── completed_scripts
|
├── data
|   ├── cleaned_data    - completed, usable data!
|   ├── other_data      - in-progress json or txt files
|   ├── source_extract  - computer readable data extracted from docs
|   └── docs_source     - original pdf & csv sources from MA RMV 
|
└── explorations        - scripts that are not yet finished (and may never be :D)
    ├── current
    ├── old
    └── paused
