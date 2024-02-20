# Version-Control
Basic python based version control system named EVC(Eren's Version Control). Currently supports initiliazing, committing with messages, jumping between commits and deleting repository. In future I hope to learn more about GIT version control system and create VC that is compatible with GIT.

EVC holds everything inside a directory .EVC. Currently it only works on Windows because it calls Windows API to make .EVC invisible. But deleting 2 lines of API code would allow it to run on linux as well.
In Windows if you add the directory that evc.py is in to PATH and make Python default runner of .py files you can use it directly from command line. Below figure represents usage of EVC inside Windows Powershell.

![image](https://github.com/SalihErenYzb/Version-Control/assets/128384160/f2b0bce3-556c-4c3a-a5ba-16e2efd76128)
