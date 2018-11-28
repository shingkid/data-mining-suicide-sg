Data
====

The dataset consists of 406 submissions dating from July 2010 to November 2018 - of which 161 were deemed relevant to suicide and depression - and 9,010 comments (responding to the 161 submissions), that were crawled from https://www.reddit.com/r/singapore/ using the **PRAW API**. Queries were informed by previous work in *"Tracking suicide risk factors through Twitter in the US" by J. Jashinsky, S.H. Burton, C.L. Hanson, J. West, C. Giraud-Carrier, M.D. Barnes, and T. Argyle (2013)*.

All data was saved to CSV format and can be found in the ``data`` folder included in this repository.

Sample
------

+---+---------------------------------------------------+-------+--------+---------------------------------------------------+-----------+---------------------+---------------------------------------------------+-------------+----------------------+
|   | title                                             | score | id     | url                                               | comms_num | created             | body                                              | author_name | query                |
+===+===================================================+=======+========+===================================================+===========+=====================+===================================================+=============+======================+
| 0 | Update from the Depressed Asshole                 | 59    | 8vgrob | https://www.reddit.com/r/singapore/comments/8v... | 30        | 2018-07-02 23:26:04 | About 3-4 months ago, I posted on reddit about... | GramTooNoob | feel alone depressed |
+---+---------------------------------------------------+-------+--------+---------------------------------------------------+-----------+---------------------+---------------------------------------------------+-------------+----------------------+
| 1 | Friends, family, acquaintances of someone who ... | 20    | 5scrdi | https://www.reddit.com/r/singapore/comments/5s... | 12        | 2017-02-06 22:45:00 | How did you feel then, and how has it affected... | depressings | friend suicide       |
+---+---------------------------------------------------+-------+--------+---------------------------------------------------+-----------+---------------------+---------------------------------------------------+-------------+----------------------+
| 2 | ...                                               | ...   | ...    | ...                                               | ...       | ...                 | ...                                               | ...         | ...                  |
+---+---------------------------------------------------+-------+--------+---------------------------------------------------+-----------+---------------------+---------------------------------------------------+-------------+----------------------+