import marimo

__generated_with = "0.6.2"
app = marimo.App()


@app.cell
def __():
    import polars as pl
    return pl,


@app.cell
def __():
    from ete3 import Tree, TreeStyle
    return Tree, TreeStyle


@app.cell
def __():
    path_to_dict_file = "input/homo_or_het.txt"
    return path_to_dict_file,


@app.cell
def __():
    current_tree = "input/OG0000157.nwk"
    return current_tree,


@app.cell
def __(mo):
    mo.md(rf"# Functions")
    return


@app.cell
def __():
    def lines_to_dict(read_lines:list, sep:str = "\t"):

        dict_one = {}

        '''
        Does: 
            Takes a list made of `readlines()` and for each line returns a dictionary type object

        Arguments:
            A list where each item is a line and the first item is a species code and second item is species names in the fashion of first_second
            separator that defaults to "\t"

        Returns:
            A dict where the keys are species codes and values are species names
        '''
        for i in read_lines:

            i = i.rstrip()

            i = i.rsplit(sep)

            dict_one[i[0]] = i[1]

        return dict_one
    return lines_to_dict,


@app.cell
def __():
    def append_reference_status(tree,my_dict):
        """
        Written for: Convienience

        Context:
            I have a dict that has the follwoing information:

            {
                ABCD : code1
                EFGH : code2
            }

            I have gene treefiles in newick format and I need to wrangle the strings in the names of the genes at the species level.
            For example:
                If I have a two genes in the newick file from one species each:
                    a. Gene-ABCD-1234
                    b. Gene-EFGH-5678
                Now, the sub-string "ABCD" identifies the first species and the sub-string "EFGH" identifies the second. 
                I need to add the code "{code1}" to the gene's name because `Hyphy BUSTED-PH` expects that in its input.

            My solution here is to have a dictionary that pairs the species code (sub-)string as keys with the status of the species as the value i.e. "{"ABCD": "code1", "EFGH":"code2"}".

            I iterate through the nodes of the tree, iterate through the keys of the dict i.e. the species code (sub-)sting (double nested for-loops, what blasphemy!) and if the node's name has the species key (sub-)string, I append "reference" to the node's name.

        Does:
            Takes a ete3 Treefile object and a dictionary.
            The dictionary should have keys that are the species code (sub-)strings and the values indicate whether the species is of type reference or not. And use this relationship to wrangle the newick file.
        """
        func_tree = tree # This is needed because ete3 appends in place and that messes up the original data.

        for node in func_tree:
            for code in my_dict:
                if code in node.name:
                    status = my_dict.get(code)
                    node.name += f"{{{status}}}"
                elif code in node.name:
                    status = my_dict.get(code)
                    node.name += f"{{{status}}}"
                else:
                    continue

        return func_tree
    return append_reference_status,


@app.cell
def __(homo_or_het):
    def list_all_tests(my_tree, my_dict, my_group:str):

        """

        Context:
        
            When you have a gene tree with some distinct groups of species. How can you separate the sub-groups of species from the list of all nodes.

            For example, if you have a gene tree with 50 genes that have 20 genes coming from Clade A, 25 from Clade B and 5 from Clade C. How can you get the sublist of nodes that belong to their respective Clades/groups/classification.

        What do you have?
        
        1. A tree
        
        2. A dict where all the keys are substrings that help you identify what species a gene tree belongs to. For example, if "Homo_erectus_Gene_123_abc" is a node in the gene tree, then "Homo_erectus" is the substring that helps you note that that node belongs to the "Homo_erectus".
        
            a. In the dict, an item would look like {"Homo_erectus":"clade_ape"} - This tells you that the "Homo_erectus" is in "clade_ape".
        
        This function is meant to take
        
        1. my_tree: A ete3 tree object
        2. my_dict: A dict that has the substrings that can help you identify a species
        3. my_group: A value from the key-value pairs that tells the function what subset of nodes belong to which classification to find.

        Returns:

            A list of nodes that belong to the "my_group" classifications in the key-value pairs.
        """

        list_of_nodes = []

        my_sub_dict = {k: v for k, v in homo_or_het.items() if v == my_group}

        for node in my_tree:
            for code in my_sub_dict:
                if code in node.name:
                    list_of_nodes.append(node.name)
        
        return list_of_nodes
                
    return list_all_tests,


@app.cell
def __(mo):
    mo.md(rf"# Wrangling and flow")
    return


@app.cell
def __(path_to_dict_file):
    with open(path_to_dict_file,"r") as dict_file:

        dict_file_lines = dict_file.readlines()
    return dict_file, dict_file_lines


@app.cell
def __(dict_file_lines, lines_to_dict):
    # This dictionary tells you if a given species code is homosporous or heterosporous
    homo_or_het = lines_to_dict(dict_file_lines)
    return homo_or_het,


@app.cell
def __(Tree, current_tree):
    current_tree_obj = Tree(current_tree)
    return current_tree_obj,


@app.cell
def __(homo_or_het):
    # This is a subset of the dict will. The original dict was filtered for keys where values are homo.
    all_homos = {k: v for k, v in homo_or_het.items() if v == "homo"} # Not re-usable because used a hard-coded "homo"
    return all_homos,


@app.cell
def __(current_tree_obj, homo_or_het, list_all_tests):
    all_hets = list_all_tests(current_tree_obj,homo_or_het,"het")
    return all_hets,


@app.cell
def __(all_hets, current_tree_obj):
    hets_common_ancestor = current_tree_obj.get_common_ancestor(all_hets)
    return hets_common_ancestor,


@app.cell
def __(hets_common_ancestor):
    hets_common_ancestor_all_desc = hets_common_ancestor.get_descendants()
    return hets_common_ancestor_all_desc,


@app.cell
def __(current_tree_obj, hets_common_ancestor):
    if hets_common_ancestor.is_root():
        print("The common ancestor of hets is the the root")
    else:
        # Does the common ancestor of all heterosporous leaves in the gene tree have homosporous leaves or something other than hets
        if_homos = set(current_tree_obj.get_leaves()) - set(hets_common_ancestor.get_leaves())
        if if_homos != 0:
            print("The last common anscestor of hets has",if_homos," that are not heterosporous.")
        else:
            print("The last common anscestor of hets has",if_homos," that are not heterosporous.")
    return if_homos,


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
