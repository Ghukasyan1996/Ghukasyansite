I’m working on Linux OS. Working on big data count were,
“Review_MAP” is main directory where I have “cells” directory in which I have large number of directories
In every directory in cells directory let` define %%CELL we have %%CELL.info file.
I need python code which will read info file and check the below arguments exist on it or not:
(ArchkRunDate CellArea CellHeight CellHeightGrids CellWidth CellWidthGrids DiffAreas GDSCellName GateAreas LefGeneration NumTransistors RawGateDensity TransistorsPerGrid pin_V)
The below arguments should be checked only for cells which start with (fs|fd|fr|sync) prefixes or contain (_fs|_fd|_fr|_sync) :
(IntNode_ NoCKSkew_ NACKSkew_)
The below arguments should not be checked only for cells which start with (fill_|filld_) prefixes or contain (_fill_|_filld_) :
("DiffAreas,GateAreas")

Script should take 2 arguments:
1st path where script should check info files
2nd file, where defined list of cells which need to be checked, if we need to check all cells from 1st argument 2nd argument should be -all



After checking each cell summarize status and in report file add the following:
-	All cells Passed
-	Failed cells where info files exist but missing X arguments
-	Failed cells where info files are missing

============================================================
SUMMARY:
Failed cells were missing arguments – XXXXX cell
Failed cells were missing info files – XXXXX cell
Report file created: /remote/us01sgnfs01031/proj_lp_gf22ag6p75t116cpp/Review_MAP/cell_check_report.csv
Report file created: /remote/us01sgnfs01031/proj_lp_gf22ag6p75t116cpp/Review_MAP/cell_check_report.csv
============================================================
