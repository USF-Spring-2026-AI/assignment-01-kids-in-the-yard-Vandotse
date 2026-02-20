from family_tree import FamilyTree


def main():
    """create the family tree and respond to user queries"""
    print("Reading files...")
    tree = FamilyTree()
    print("Generating family tree...")
    tree.generate()

    while True:
        print("\nAre you interested in:")
        print("(T)otal number of people in the tree")
        print("Total number of people in the tree by (D)ecade")
        print("(N)ames duplicated")
        print("(Q)uit")
        try:
            choice = input("> ").strip().upper()
        except EOFError:
            break

        if not choice:
            continue
        if choice == "Q":
            break
        if choice == "T":
            total = tree.get_total_count()
            print(f"The tree contains {total} people total")
        elif choice == "D":
            by_decade = tree.get_count_by_decade()
            for decade in sorted(by_decade.keys(), key=lambda d: int(d[:4])):
                print(f"{decade}: {by_decade[decade]}")
        elif choice == "N":
            duplicates = tree.get_duplicate_names()
            if not duplicates:
                print("There are no duplicate names in the tree.")
            else:
                print(f"There are {len(duplicates)} duplicate name(s) in the tree:")
                for name in duplicates:
                    print(f"* {name}")
        else:
            print("Invalid choice. Please enter T, D, N, or Q.")


if __name__ == "__main__":
    main()
