from .cli import main
import sys
if len(sys.argv) == 1:
    main.callback(None, 5, None)
else:
    from .cli import app
    app()
