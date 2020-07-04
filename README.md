# cheese-shop
Well, it's certainly uncontaminated by cheese.

## Setup
In MySQL, first load the database definition:

    SOURCE sql/def.sql;

Then, create an user named `wensleydale` with appropriate permissions
to be used by `mysql.connector`:

    SOURCE sql/ctl.sql;

To insert the metadata to the `cheese_shop` database, open a shell and run

    pip install -r tools/requirements.txt
    python tools/make-cheeses.py

The script requires Python 3.6 or above.  Due to dummy handling of classifiers,
`sql/def.sql` needs to be reloaded before each run.
