# vasp_things
Some scripts for formatting vasp output

They read the vasprun.xml file. 

Carl Belle helped out with float conversion.

NB: as of writing the current VASP release (5.4.4) has a bug which results in the root node not being closed for TDDFT and BSE runs, so you must insert this tag manually before running the TDDFT_Process_Vasprun and BSE_Process_Vasprun scripts. 

To do this just open vasprun.xml in a text editor, and at the end of the file write "</modeling>" on a new line.

If you have set LORBIT to write the projected DOS, vasprun.xml can be quite large (100s of MB), if you are using a cluster, consider running these scripts on the compute nodes and not the login nodes. 

You may find that you have to use the compute nodes as the login node will run out of memory.
