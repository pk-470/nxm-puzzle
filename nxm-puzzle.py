from PIL import Image, ImageDraw, ImageFont
from math import floor, inf
import random
import copy


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
    random.shuffle(nbhs)
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
                sol_temp = copy.deepcopy(sol)
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
    print()
    print("Welcome to the n × m path explorer!")
    print()
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

    print()
    print(
        "Enter the allowed moves in the format a,b for integers a & b "
        "(so for example if you input 2,-3, then you are allowed to move from "
        "square (i, j) to square (i+2, i-3)). When you are done, enter 'ok'."
    )
    k = 1
    rule = ""
    rules_input = []
    while True:
        rule = input(f"Allowed move no. {k}: ")
        if rule != "ok":
            try:
                rule_i, rule_j = rule.split(",")
                rules_input.append((int(rule_i), int(rule_j)))
                k = k + 1
            except:
                print("Please input a valid move in the correct format.")
        else:
            if rules_input:
                break
            else:
                print("Please enter at least one allowed move.")
    rules = []
    [rules.append(x) for x in rules_input if x not in rules]  # Remove duplicates
    print("The allowed moves are: " + ", ".join([str(rule) for rule in rules]) + ".")

    if n == m:
        print()
        print(
            "If you wish to generate solutions starting from particular cells, "
            f"enter them in the format i,j for 0 ≤ i, j ≤ {n - 1} (e.g. 0,1). "
            "After entering a cell, input the length of the solutions you wish to "
            "get starting from that cell. Finally, enter the number of solutions of "
            "your chosen length you wish to generate starting from that cell."
        )
        print("Options:")
        print(
            "-  If you want to generate all solutions of your chosen length from a "
            "particular starting cell, input 'all' after entering the cell coordinates "
            "and the solution length."
        )
        print(
            "-  If you want to generate solutions from a randomly chosen starting cell, "
            "enter 'any' as the cell coordinates. "
        )
        print(
            "-  If you want to generate solutions from all possible starting cells, "
            "enter 'all' as the cell coordinates. Note that due to the 8 symmetries of "
            "the square, to produce solutions starting from all cells it suffices to "
            "consider sequences starting from cells in the region 0 ≤ i ≤ j ≤ "
            f"{int(floor((n - 1) / 2))}."
        )
        print("Enter 'ok' when you are done.")
    else:
        print()
        print(
            "If you wish to generate solutions starting from particular cells, enter "
            f"them in the format i,j for 0 ≤ i ≤ {n - 1}, 0 ≤ j ≤ {m - 1} (e.g. 0,1). "
            "After entering a cell, input the length of the solutions you wish to get "
            "starting from that cell. Finally, enter the number of solutions of your chosen "
            "length you wish to generate starting from that cell."
        )
        print("Options:")
        print(
            "-  If you want to generate all solutions of your chosen length from a "
            "particular starting cell, input 'all' after entering the cell coordinates "
            "and the solution length."
        )
        print(
            "-  If you want to generate solutions from a randomly chosen starting cell, "
            "enter 'any' as the cell coordinates. "
        )
        print(
            "-  If you want to generate solutions from all possible starting cells, "
            "enter 'all' as the cell coordinates. Note that due to the 4 symmetries "
            "of the rectangle, to produce solutions starting from all cells it suffices "
            "to consider sequences starting from cells in the region 0 ≤ i ≤ "
            f"{int(floor((n - 1) / 2))}, 0 ≤ j ≤ {int(floor((m - 1) / 2))}."
        )
        print("Enter 'ok' when you are done.")
    k = 1
    starts = []
    lengths = []
    sol_nos = []
    while True:
        print()
        start = input(f"Starting cell {k}: ")
        if start != "ok" and start != "all":
            check = False
            if start == "any":
                start_i, start_j = random.randint(0, n - 1), random.randint(0, m - 1)
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
                        raise Exception()
                except:
                    if n == m:
                        print(
                            "Please enter a valid starting cell in the correct format, "
                            "or 'all' if you wish to get solutions starting from all "
                            f"cells in the region 0 ≤ i, j ≤ {int(floor((n - 1) / 2))}, "
                            "or 'ok' if you are done."
                        )
                    else:
                        print(
                            "Please enter a valid starting cell in the correct format, "
                            "or 'all' if you wish to get solutions starting from all "
                            f"cells in the region 0 ≤ i ≤ {int(floor((n - 1) / 2))}, "
                            f"0 ≤ j ≤ {int(floor((m - 1) / 2))}, or 'ok' if you are done."
                        )
            if check:
                while True:
                    length = input(
                        "Enter the desired length of the solutions starting from "
                        f"cell ({start_i}, {start_j}): "
                    )
                    if (
                        not length.isnumeric()
                        or not int(length) > 0
                        or not int(length) <= n * m
                    ):
                        print(
                            "The solution length must be a positive integer, and at "
                            f"most {n * m}."
                        )
                    else:
                        lengths.append(int(length))
                        while True:
                            sols_no = input(
                                "Enter the desired number of solutions of length "
                                f"{length} starting from cell ({start_i}, {start_j}): "
                            )
                            if sols_no.isnumeric() and int(sols_no) > 0:
                                sol_nos.append(int(sols_no))
                                break
                            elif sols_no == "all":
                                sol_nos.append(inf)
                                break
                            else:
                                print(
                                    "The number of solutions must be a positive integer or 'all'."
                                )
                        break
                print(
                    f"{sols_no} solutions of length {length} starting from cell ({start_i}, {start_j})."
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
                        "Enter the desired length of the solutions starting from each cell in the region "
                        f"0 ≤ i ≤ j ≤ {int(floor((n - 1) / 2))}: "
                    )
                else:
                    length = input(
                        "Enter the desired length of the solutions starting from each cell in the region "
                        f"0 ≤ i ≤ {int(floor((n - 1) / 2))}, 0 ≤ j ≤ {int(floor((m - 1) / 2))}: "
                    )
                if (
                    not length.isnumeric()
                    or not int(length) > 0
                    or not int(length) <= n * m
                ):
                    print(
                        f"The solution length must be a positive integer, and at most {n * m}."
                    )
                else:
                    lengths = [int(length)] * len(starts)
                    while True:
                        if n == m:
                            sols_no = input(
                                f"Enter the desired number of solutions of length {length} "
                                "starting from each cell in the region 0 ≤ i ≤ j ≤ "
                                f"{int(floor((n - 1) / 2))}: "
                            )
                        else:
                            sols_no = input(
                                f"Enter the desired number of solutions of length {length} "
                                "starting from each cell in the region 0 ≤ i ≤ "
                                f"{int(floor((n - 1) / 2))}, 0 ≤ j ≤ {int(floor((m - 1) / 2))}: "
                            )
                        if sols_no.isnumeric() and int(sols_no) > 0:
                            sol_nos = [int(sols_no)] * len(starts)
                            break
                        elif sols_no == "all":
                            sol_nos = [inf] * len(starts)
                            break
                        else:
                            print(
                                "The number of solutions must be a positive integer or 'all'."
                            )
                    break
            if n == m:
                print(
                    f"{sols_no} solutions of length {length} starting from each cell in the "
                    f"region 0 ≤ i ≤ j ≤ {int(floor((n - 1) / 2))}."
                )
            else:
                print(
                    f"{sols_no} solutions of length {length} starting from each cell in the "
                    f"region 0 ≤ i ≤ {int(floor((n - 1) / 2))}, 0 ≤ j ≤ "
                    f"{int(floor((m - 1) / 2))}."
                )

            break

    sols_mega = []
    out_nos = []

    for ind, start in enumerate(starts):
        length = lengths[ind]
        sols_no = sol_nos[ind]
        sols = search(start[0], start[1], n, m, rules, length, sols_no)[0]
        sols_mega.append(sols)
        if sols:
            print()
            print(
                f"{len(sols)} solutions of length {length} starting from "
                f"cell {start} were found."
            )
            if len(sols) > 10:
                while True:
                    out_no = input(
                        f"How many out of the {len(sols)} solutions starting from "
                        f"cell {sols[0][0]} would you like to print? "
                    )
                    if (
                        not out_no.isnumeric()
                        or not int(out_no) >= 0
                        or not int(out_no) <= len(sols)
                    ):
                        print(f"Please choose a number between 0 and {sols}")
                    else:
                        break
                out_no = int(out_no)
            else:
                out_no = len(sols)
            out_nos.append(out_no)
            for r in range(out_no):
                print()
                print(f"Solution {r + 1}:")
                print()
                print(sols[r])
        else:
            print()
            print(
                f"No solutions of length {length} starting from cell {start} were found."
            )
            out_nos.append(0)
    print("\n")

    return sols_mega, out_nos, n, m


def lin(n, b):
    return (2 * b + 1) * n + b


def draw_puzzle(sols_mega, out_nos, n, m):

    b = 60
    n_1 = (2 * b + 1) * n
    m_1 = (2 * b + 1) * m
    font = ImageFont.truetype("OpenSans-Regular.ttf", b)

    for ind, sols in enumerate(sols_mega):
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

                    for k, cell in enumerate(sol):
                        i, j = cell[0], cell[1]
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


if __name__ == "__main__":
    sols_mega, out_nos, n, m = puzzle()
    draw_puzzle(sols_mega, out_nos, n, m)
