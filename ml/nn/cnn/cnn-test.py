'''
# self notes

seems like smaller kernels can capture finer details while
larger kernels smooth over details, but can capture larger
abstract ideas

if i know i want to detect some patterns thats dependent
on edges, multiple layers could abstract the input into 
edges first, then into the thing i want

i think the idea of designing a hypothesis for CNNs comes 
down to this process of finding architecture you think would be
useful for the task at hand, based on these ideas of 
abstracting features?

i could apply different kernels to the same layer, and get
different views/abstractions from the same layer, and perform
different further convolutions etc. for example, in this case
of edge detection, i could do one for 0-to-1 edges, and another
for 1-to-0 edges. one of the filters below is naturally giving 
-1 for one and 1 for the other. some kind of relu business could
split this information.

kernels operating in paralell for this business thinkthonk


'''
def main():
    test_simple()

def test_simple():
    # simple edge detection on 1d array
    input = [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0]

    # prefer odd kernel size so there's clear center
    simple_edge_kernel = [1, 0, -1]
    test_kernel = [1, 1, 1]

    # we can add a False at the end for no padding
    conv = apply_kernel(input, simple_edge_kernel)
    conv = apply_kernel(input, test_kernel)

    test_kernels(input, [
        [1, 0, -1], [1, 1, 1], [1, 2, 0, -2, -1],
        [1, -1]
        ])

def test_layers():
    input = [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0]
    conv = apply_kernel(input, [1, 0, -1])


def test_kernels(input, kernels):
    print(f"input={ls_align(input)}")
    for kernel in kernels:
        conv = apply_kernel(input, kernel)
        print(f"kernel={kernel}")
        print(f" conv={ls_align(conv)}")


def ls_align(ls, w=2):
    return ", ".join(f"{x:{w}d}" for x in ls)


def pw_mul(ls1, ls2):
    return [a * b for (a, b) in zip(ls1, ls2)]


def dot_mul(ls1, ls2):
    assert len(ls1) == len(ls2)
    sum = 0
    for a, b in zip(ls1, ls2):
        sum += a * b

    return sum


def apply_kernel(ls, kernel, padding=True):
    '''
    this is basically forward pass from one layer to another
    padding=True keeps layer sizes consistent
    '''
    if len(kernel) > len(ls):
        raise ValueError("kernel longer than list")

    padlen = len(kernel) - 1
    lpad = padlen // 2
    rpad = padlen // 2

    if len(kernel) % 2 == 0:
        rpad += 1

    convolution = [
        dot_mul(ls[i : i + len(kernel)], kernel)
        for i in range(len(ls) - len(kernel) + 1)
    ]

    if padding:
        lzeros = [0] * lpad
        rzeros = [0] * rpad
        convolution = lzeros + convolution + rzeros
    return convolution


if __name__ == "__main__":
    main()
