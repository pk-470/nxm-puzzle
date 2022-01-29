from PIL import Image, ImageDraw, ImageFont
from numpy import floor, Inf
from random import randint, shuffle


def boundary(i, j, n, m, bd):
    if i < 0 or j < 0 or i > n - 1 or j > m - 1 or (i, j) in bd:
        return True
    else:
        return False


def nbhd(i, j, rules, n, m, bd):
    nbhs = []
    for x in rules:
        if not boundary(i + x[0], j + x[1], n, m, bd):
            nbhs.append((i + x[0], j + x[1]))
    shuffle(nbhs)
    return nbhs


def search(i, j, n, m, rules, length, sol_no, sol=None, r=0):
    sols = []
    if sol == None:
        sol = []
    sol.append((i, j))
    nbhs = nbhd(i, j, rules, n, m, sol)
    # If the path is short try to extend it, if it is maximal discard
    if len(sol) < length:
        if nbhs:
            for nbh in nbhs:
                # Break if we have already found sol_no solutions
                if r == sol_no:
                    break
                i, j = nbh[0], nbh[1]
                sol_temp = sol.copy()
                sols_ext, r = search(i, j, n, m, rules, length, sol_no, sol_temp, r)
                sols.extend(sols_ext)
        else:
            return [], r
    # If the path is of the right length but is not maximal, discard
    elif len(sol) == length:
        if nbhs:
            return [], r
        else:
            sols.append(sol)
            r = r + 1
    return sols, r


def puzzle():

    while True:
        n = input("Enter the vertical side length: ")
        if not n.isnumeric() or not int(n) > 0:
            print("The side length must be a positive integer.")
        else:
            break
    n = int(n)

    while True:
        m = input("Enter the horizontal side length: ")
        if not m.isnumeric() or not int(m) > 0:
            print("The side length must be a positive integer.")
        else:
            break
    m = int(m)

    print(
        "\n"
        "Enter the allowed moves in the format a,b for integers a & b (so for example if you input 2,-3, then "
        "you are allowed to move from square (i, j) to square (i+2, i-3)). When you are done, enter 'ok'."
    )
    k = 1
    rule = ""
    rules_0 = []
    while True:
        rule = input("Allowed move no. " + str(k) + ": ")
        if rule != "ok":
            try:
                rule_i, rule_j = rule.split(",")
                rules_0.append((int(rule_i), int(rule_j)))
                k = k + 1
            except:
                print("Please input a valid move in the correct format.")
        else:
            if rules_0:
                break
            else:
                print("Please enter at least one allowed move.")
    rules = []
    [rules.append(x) for x in rules_0 if x not in rules]  # Remove duplicates
    print("The allowed moves are: " + ", ".join(str(rule) for rule in rules) + ".")

    if n == m:
        print(
            "\n"
            "If you wish to generate solutions starting from particular cells, enter them in the format i,j for 0 <= i, j <= "
            + str(n - 1)
            + " (e.g. 0,1). After entering a cell, input the length of the solutions you wish to get starting from that cell. Finally, "
            "enter the number of solutions of your chosen length you wish to generate starting from that cell. If you want to generate "
            "all solutions of your chosen length from a particular starting cell, input 'all' after entering the cell coordinates and "
            "the solution length. If you want to generate solutions from a randomly chosen starting cell, enter 'any' as the cell "
            "coordinates. If you want to generate solutions from all possible starting cells, enter 'all' as the cell coordinates. "
            "Note that due to the 8 symmetries of the square, to produce solutions starting from all cells it suffices to consider "
            "sequences starting from cells in the region 0 <= i <= j <= "
            + str(int(floor((n - 1) / 2)))
            + ". Enter 'ok' when you are done."
        )
    else:
        print(
            "\n"
            "If you wish to generate solutions starting from particular cells, enter them in the format i,j for 0 <= i <= "
            + str(n - 1)
            + ", 0 <= j <= "
            + str(m - 1)
            + " (e.g. 0,1). After entering a cell, input the length of the solutions you wish to get starting from that cell. Finally, "
            "enter the number of solutions of your chosen length you wish to generate starting from that cell. If you want to generate "
            "all solutions of your chosen length from a particular starting cell, input 'all' after entering the cell coordinates and "
            "the solution length. If you want to generate solutions from a randomly chosen starting cell, enter 'any' as the cell "
            "coordinates. If you want to generate solutions from all possible starting cells, enter 'all' as the cell coordinates. "
            "Note that due to the 4 symmetries of the rectangle, to produce solutions starting from all cells it suffices to consider "
            "sequences starting from cells in the region 0 <= i <= "
            + str(int(floor((n - 1) / 2)))
            + ", 0 <= j <= "
            + str(int(floor((m - 1) / 2)))
            + ". Enter 'ok' when you are done."
        )
    k = 1
    starts = []
    lengths = []
    sol_nos = []
    while True:
        start = input("\nStarting cell " + str(k) + ": ")
        if start != "ok" and start != "all":
            check = False
            if start == "any":
                start_i, start_j = randint(0, n - 1), randint(0, m - 1)
                starts.append((start_i, start_j))
                start_i, start_j = str(start_i), str(start_j)
                check = True
            else:
                try:
                    start_i, start_j = start.split(",")
                    if (
                        int(start_i) >= 0
                        and int(start_i) < n
                        and int(start_j) >= 0
                        and int(start_j) < m
                    ):
                        starts.append((int(start_i), int(start_j)))
                        check = True
                    else:
                        if n == m:
                            print(
                                "Please enter a valid starting cell in the correct format, or 'all' if you wish to get solutions "
                                "starting from all cells in the region 0 <= i, j <= "
                                + str(int(floor((n - 1) / 2)))
                                + ", or 'ok' if you are done."
                            )
                        else:
                            print(
                                "Please enter a valid starting cell in the correct format, or 'all' if you wish to get solutions "
                                "starting from all cells in the region 0 <= i <= "
                                + str(int(floor((n - 1) / 2)))
                                + ", 0 <= j <= "
                                + str(int(floor((m - 1) / 2)))
                                + ", or 'ok' if you are done."
                            )
                except:
                    if n == m:
                        print(
                            "Please enter a valid starting cell in the correct format, or 'all' if you wish to get solutions "
                            "starting from all cells in the region 0 <= i, j <= "
                            + str(int(floor((n - 1) / 2)))
                            + ", or 'ok' if you are done."
                        )
                    else:
                        print(
                            "Please enter a valid starting cell in the correct format, or 'all' if you wish to get solutions "
                            "starting from all cells in the region 0 <= i <= "
                            + str(int(floor((n - 1) / 2)))
                            + ", 0 <= j <= "
                            + str(int(floor((m - 1) / 2)))
                            + ", or 'ok' if you are done."
                        )
            if check:
                while True:
                    length = input(
                        "Enter the desired length of the solutions starting from cell ("
                        + start_i
                        + ", "
                        + start_j
                        + "): "
                    )
                    if (
                        not length.isnumeric()
                        or not int(length) > 0
                        or not int(length) <= n * m
                    ):
                        print(
                            "The solution length must be a positive integer, and at most "
                            + str(n * m)
                            + "."
                        )
                    else:
                        lengths.append(int(length))
                        while True:
                            sol_no = input(
                                "Enter the desired number of solutions of length "
                                + length
                                + " starting from cell ("
                                + start_i
                                + ", "
                                + start_j
                                + "): "
                            )
                            if sol_no.isnumeric() and int(sol_no) > 0:
                                sol_nos.append(int(sol_no))
                                break
                            elif sol_no == "all":
                                sol_nos.append(Inf)
                                break
                            else:
                                print(
                                    "The number of solutions must be a positive integer or 'all'."
                                )
                        break
                print(
                    sol_no
                    + " solutions of length "
                    + length
                    + " starting from cell ("
                    + start_i
                    + ", "
                    + start_j
                    + ")."
                )
                k = k + 1
        elif start == "ok":
            if starts:
                break
            else:
                print("Please enter at least one starting cell.")
        elif start == "all":
            if n == m:
                starts = [
                    (i, j)
                    for j in range(int(floor((n - 1) / 2)) + 1)
                    for i in range(j + 1)
                ]
            else:
                starts = [
                    (i, j)
                    for j in range(int(floor((m - 1) / 2)) + 1)
                    for i in range(int(floor((n - 1) / 2)) + 1)
                ]
            while True:
                if n == m:
                    length = input(
                        "Enter the desired length of the solutions starting from each cell in the region 0 <= i <= j <= "
                        + str(int(floor((n - 1) / 2)))
                        + ": "
                    )
                else:
                    length = input(
                        "Enter the desired length of the solutions starting from each cell in the region 0 <= i <= "
                        + str(int(floor((n - 1) / 2)))
                        + ", 0 <= j <= "
                        + str(int(floor((m - 1) / 2)))
                        + ": "
                    )
                if (
                    not length.isnumeric()
                    or not int(length) > 0
                    or not int(length) <= n * m
                ):
                    print(
                        "The solution length must be a positive integer, and at most "
                        + str(n * m)
                        + "."
                    )
                else:
                    lengths = [int(length)] * len(starts)
                    while True:
                        if n == m:
                            sol_no = input(
                                "Enter the desired number of solutions of length "
                                + length
                                + " starting from each cell in the region 0 <= i <= j <= "
                                + str(int(floor((n - 1) / 2)))
                                + ": "
                            )
                        else:
                            sol_no = input(
                                "Enter the desired number of solutions of length "
                                + length
                                + " starting from each cell in the region 0 <= i <= "
                                + str(int(floor((n - 1) / 2)))
                                + ", 0 <= j <= "
                                + str(int(floor((m - 1) / 2)))
                                + ": "
                            )
                        if sol_no.isnumeric() and int(sol_no) > 0:
                            sol_nos = [int(sol_no)] * len(starts)
                            break
                        elif sol_no == "all":
                            sol_nos = [Inf] * len(starts)
                            break
                        else:
                            print(
                                "The number of solutions must be a positive integer or 'all'."
                            )
                    break
            if n == m:
                print(
                    sol_no
                    + " solutions of length "
                    + length
                    + " starting from each cell in the region 0 <= i <= j <= "
                    + str(int(floor((n - 1) / 2)))
                    + "."
                )
            else:
                print(
                    sol_no
                    + " solutions of length "
                    + length
                    + " starting from each cell in the region 0 <= i <= "
                    + str(int(floor((n - 1) / 2)))
                    + ", 0 <= j <= "
                    + str(int(floor((m - 1) / 2)))
                    + "."
                )

            break

    sols_mega = []
    out_nos = []

    for ind in range(len(starts)):
        start = starts[ind]
        length = lengths[ind]
        sol_no = sol_nos[ind]
        sols = search(start[0], start[1], n, m, rules, length, sol_no)[0]
        sols_mega.append(sols)
        if sols:
            print(
                "\n"
                + str(len(sols))
                + " solutions of length "
                + str(length)
                + " starting from cell "
                + str(start)
                + " were found."
            )
            if len(sols) > 10:
                while True:
                    out_no = input(
                        "How many out of the "
                        + str(len(sols))
                        + " solutions starting from cell "
                        + str((sols[0][0]))
                        + " would you like to print? "
                    )
                    if (
                        not out_no.isnumeric()
                        or not int(out_no) >= 0
                        or not int(out_no) <= len(sols)
                    ):
                        print("Please choose a number between 0 and " + str(len(sols)))
                    else:
                        break
                out_no = int(out_no)
            else:
                out_no = len(sols)
            out_nos.append(out_no)
            for r in range(out_no):
                print("\nSolution " + str(r + 1) + ":\n", sols[r], sep="")
        else:
            print(
                "\n"
                "No solutions of length "
                + str(length)
                + " starting from cell "
                + str(start)
                + " were found."
            )
    print("\n")

    return sols_mega, out_nos, n, m


def lin(n, b):
    return (2 * b + 1) * n + b


def draw_puzzle(sols_mega, out_nos, n, m):

    b = 60
    n_1 = (2 * b + 1) * n
    m_1 = (2 * b + 1) * m
    font = ImageFont.truetype("OpenSans-Regular.ttf", b)

    for ind in range(len(sols_mega)):
        sols = sols_mega[ind]
        if sols:
            out_no = out_nos[ind]
            for sol in sols[:out_no]:
                with Image.new("RGB", (m_1, n_1), "White") as im:
                    draw = ImageDraw.Draw(im)
                    # Draw an n*m chessboard
                    for j in range(m_1):
                        for i in range(n_1):
                            if (j + i) % 2 == 1:
                                draw.polygon(
                                    [
                                        (lin(j, b) - b, lin(i, b) - b),
                                        (lin(j, b) - b, lin(i, b) + b),
                                        (lin(j, b) + b, lin(i, b) + b),
                                        (lin(j, b) + b, lin(i, b) - b),
                                    ],
                                    fill="Black",
                                )

                    for k in range(len(sol)):
                        i, j = sol[k][0], sol[k][1]
                        w, h = draw.textsize(str(k + 1), font=font)
                        # Draw start
                        if k == 0:
                            draw.text(
                                (int(lin(j, b) - w / 2), int(lin(i, b) - 10 - h / 2)),
                                str(k + 1),
                                font=font,
                                fill="Green",
                                align="center",
                            )
                        elif (j + i) % 2 == 0 and k < len(sol) - 1:
                            draw.text(
                                (int(lin(j, b) - w / 2), int(lin(i, b) - 10 - h / 2)),
                                str(k + 1),
                                font=font,
                                fill="Black",
                                align="center",
                            )
                        elif (j + i) % 2 == 1 and k < len(sol) - 1:
                            draw.text(
                                (int(lin(j, b) - w / 2), int(lin(i, b) - 10 - h / 2)),
                                str(k + 1),
                                font=font,
                                fill="White",
                                align="center",
                            )
                        # Draw end
                        else:
                            draw.text(
                                (int(lin(j, b) - w / 2), int(lin(i, b) - 10 - h / 2)),
                                str(len(sol)),
                                font=font,
                                fill="Red",
                                align="center",
                            )

                    im.show()


sols_mega, out_nos, n, m = puzzle()
draw_puzzle(sols_mega, out_nos, n, m)
