# Webcrawlers for brazilian courts 

## Scope

In this project we built three crawlers to acquire jurisprudence documents 
from STF, STJ, TJ-SC and also Jusbrasil Portal.

In the beginning of this process we set as our goal to acquire documents from any juridical context.
And we set as data sources three superior courts (STF, STJ and TJ-SC)

Later to fill our specific needs we built another crawler for Jusbrasil 
portal to get only files related to **consumer law** and **failures in air transport services**

## Project Setup

To execute this project you can run the following command:

`python run.py`

Which will execute all crawlers to acquire documents and then get related metadata. 
However, it takes some weeks to run all these crawlers. So be patient.

Also many non-standard libraries are required, for example `wget`, `selenium` and many others.
So, as you run the script, python will trigger errors about missing libraries. 
To download theses libraries, run:

`pip install name_of_the_library` 

 
## Project Structure

In this project there is a main file called `run.py` as already exposed. 
Then, we divide into the following folders:

- **crawler:** Contains code related to the webcrawlers for documents and metadata.
- **data:** Constains some local data used by the project
- **process_text:** Contains code for dealing with text files
- **utils:** Constains auxiliary code.