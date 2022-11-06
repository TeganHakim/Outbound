"pythonAnywhere API Documentation:" 

'''from docopt import docopt

from pythonanywhere.scripts_commons import ScriptSchema, get_logger
from pythonanywhere.task import Task


def main(*, command, hour, minute, disabled):
    get_logger(set_info=True)
    hour = int(hour) if hour is not None else None
    task = Task.to_be_created(command=command, hour=hour, minute=int(minute), disabled=disabled)
    task.create_schedule()


if __name__ == "__main__":
    schema = ScriptSchema(
        {
            "--command": str,
            "--hour": ScriptSchema.hour,
            "--minute": ScriptSchema.minute,
            "--disabled": ScriptSchema.boolean,
        }
    )
    arguments = schema.validate_user_input(docopt(__doc__))

    main(**arguments)'''