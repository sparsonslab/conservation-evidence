import csv

from evidence.models import Evidence
from django.db.models import Model, CharField, IntegerField

# Run this as:
# python manage.py shell < evidence/import_from_csv.py


def string_to_field(cell, field):
    """ Convert a string read from a CSV cell into a value appropriate
    to a field.

    Parameters
    ----------
    cell: str
        The CSV cell's string value.
    field: django.db.models.fields.Field
        The field type.

    Returns
    -------
    Any:
        The cell's value or None if it could not be converted.
    """
    if isinstance(field, CharField):
        return str(cell)

    if isinstance(field, IntegerField):
        if field.choices:
            for i, k in field.choices:
                if k == cell:
                    return i
            return None
        try:
            return int(cell)
        except ValueError:
            return None
    return None


def import_evidence_from_csv(path):
    """ Add entries/objects to the Evidence model, from a CSV file.

    The CSV have a first ("header") row with the names of each 
    Evidence field (case-insensitive).

    Parameters
    ----------
    path: str
        The path of the CSV file.
    """
    # The fields of Evidence that should be expected in the input CSV,
    # Excludes the primary key field ("id").
    field_types = {
        field.name: field
        for field in Evidence._meta.fields
        if field.name != 'id'
    }

    # The set of field names.
    field_names = set(list(field_types.keys()))

    # Open the CSV.
    with open(path) as fs:
        reader = csv.reader(fs)

        # Loop through rows.
        for i, row in enumerate(reader):

            # Check that the header row has all the required fields.
            if i == 0:
                columns = [column.lower() for column in row]
                missing_columns = field_names - set(columns)
                if missing_columns:
                    print(f"Please rename the column headers of your CSV to in include\n {missing_columns}.")
                    break
                continue

            # For a row of data, get the table values converted from
            # string to the field's type.
            kwargs = {
                field: string_to_field(value, field_types[field])
                for field, value in zip(columns, row)
                if(field in field_types)
            }

            # If some row values could not be converted, warn.
            incorrect_columns = {field for field, value in kwargs.items() if value is None}
            if incorrect_columns:
                print(f"Row {i + 1}: Please provide a correct values for {incorrect_columns}.")
                continue

            # Create the Evidence object and save.
            obj = Evidence(**kwargs)
            obj.save()


# The path of the CSV file.
import_evidence_from_csv("data/Task sheet.csv")
