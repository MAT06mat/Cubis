import functools

def if_no_message(func):
    """Test if there is no current message"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].parent.message != None:
            return super(args[0].__class__ ,args[0]).on_press()
        return func(*args, **kwargs)
    return wrapper

def if_no_piece(func):
    """Test if there is no piece between the button and the user"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].parent.current_piece != None:
            if args[0].parent.current_piece.delta_pos == None:
                return func(*args, **kwargs)
            return super(args[0].__class__ ,args[0]).on_press()
        else:
            return func(*args, **kwargs)
    return wrapper