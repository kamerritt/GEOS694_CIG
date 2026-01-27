import os


CONSTANT = 1000
cool_variable = 5
cooler_variable = 6
coolest_variable = 7

def overwrite_print():
    """
    Although we overwrite the `print` command here, it does not have downstream
    consequences because once the function ends, all of the modifications 
    are gone. 

    Think about the syntactical format of the function as Las Vegas, whatever 
    happens in the function stays in the function.
    """
    print = 5
    # print(5)  <- This will not work because we have overwritten `print`
    return print


def global_parameters():
    """
    Global parameters are defined everywhere
    """
    return a


if __name__ == "__main__":
    # This is okay because the function is self-contained
    a = overwrite_print()
    print(a)

    # Global parameters are dangerous if you are not using them intentionally
    print(global_parameters())

    # If you are using something like a CONSTANT, be very clear that you do
    # not intend for this to change
    print(CONSTANT)

    CONSTANT *= 10  # <- BAD practice, we do not expect CONSTANT to change, ever

    # Be careful about `=`, sometimes it 
    modified_constant = CONSTANT
    CONSTANT /= 10

    print(CONSTANT)
    print(modified_constant)
