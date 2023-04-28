# ISAM
Sequential Index Organization - README

This project implements a sequential index organization used to store data in the form of records. 
Each record has fields such as a key, information about whether the record is empty, and an overflow pointer. 
A record is a complex number with ranges of (-100,100) for the real and imaginary parts, respectively, extended by a key that is a natural number.

To ensure system performance and scalability, a locking mechanism is applied. 
When a page reaches a certain filling level, it is rewritten and expanded with new records. 
The blocking factor is set to b=4, the alpha factor to 0.5, indicating that the pages will be filled to half after reorganization, 
and the vn_ratio to 0.5, indicating that if the number of pages (overflow/number of pages) exceeds the vn_ratio threshold,
the program will perform automatic reorganization.

The project contains implementations of methods that allow adding, deleting, and updating records in the sequential index organization, 
as well as methods to reorganize data to maintain the appropriate page-filling ratio.

Test file format:

The test file consists of several instructions in a single line. Possible instructions are:

A - add a record - followed by an integer > 0, which will be the key.
P - displays all current pages and overflow pages.

U - update a record without a key - followed by an integer - the key that identifies the record we want to update.

D - delete a record - followed by an integer - the key that identifies the record we want to mark for deletion.

O - allows manual file reorganization.

The program generates a random record value so we do not need to complete the instruction with the value of the stored record.

Implementation:

The program stores the entire index in the main memory of the computer and performs operations on it there.
