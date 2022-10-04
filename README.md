# IRS - Imported Requirements Search

Have you ever had to make a requirements.txt file and had your `pip freeze > requirements.txt` throw a bunch of nonsense your way? Packages and Modules that are useful yes but not necessarily relevant to the project code you currently are focused on?

Well look no further! This script here will recursively parse all of the directories in your project for python files that import modules, if those modules aren't a part of your Project Code and not found in (most) of the Standard Python Library -- this util will generate an `irs_requirements.txt` for you!

That file needs a manual review to confirm what packages have "business" being in it but at least you don't have to parse through some junk; check out the regular `requirements.txt` to see what I mean.

Having your Project Python Code audited has never been easier! Just run: `python irs.py` to generate a project specific `irs_requirements.txt` (assuming the script is in the root dir of your project)


