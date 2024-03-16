# Lab setup for testing

In order to run all tests, you need a lab environment where you can freely create and delete objects. This guide is
about to give you a guidance how to set up such a lab.

## Virtual lab

In case you have no real lab at your disposal, you can run test on virtual machines. On Windows, Hyper-V is a convenient
solution. You have to make sure you can access the devices from your desktop and also that devices can access each
other.

## FMG setup

It is advisable to have a separate testing ADOM with workspace mode enabled. This way - during development - no errors
would leave garbage in the configuration. `Workspace` mode tests will discard changes done on FMG.
All this is not a requirement, but makes development easy. `Workflow` mode is not tested and most probably won't work.
