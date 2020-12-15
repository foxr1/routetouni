import io


def main():
    data_file = "revision_data.txt"
    revision_list = parse_file(data_file)
    return revision_list


def parse_file(data_file):
    text_as_list = []

    with io.open(data_file, "r", encoding="utf-8") as f:
        for line in f:
            text_as_list.append(line)
    for i in range(len(text_as_list)):
        if text_as_list[i] == "NOTETAKING\n":
            notetaking_marker = i
        if text_as_list[i] == "USEFUL NOTETAKING SOFTWARE\n":
            notetaking_software_marker = i
        if text_as_list[i] == "REFERENCING\n":
            referencing_marker = i
        if text_as_list[i] == "REFERENCING SOFTWARE\n":
            referencing_software_marker = i
        if text_as_list[i] == "EXAMS AND REVISION\n":
            revision_marker = i
        if text_as_list[i] == "USEFUL REVISION SOFTWARE\n":
            revision_software_marker = i
        if text_as_list[i] == "UNIVERSITY LIBRARY\n":
            library_marker = i
        if text_as_list[i] == "USEFUL UNIVERSITY LINKS\n":
            library_software_marker = i

    notetaking = [text_as_list[notetaking_marker + 1:notetaking_software_marker - 1],
                  text_as_list[notetaking_software_marker + 1:referencing_marker - 1]]
    referencing = [text_as_list[referencing_marker + 1:referencing_software_marker - 1],
                   text_as_list[referencing_software_marker + 1:revision_marker - 1]]
    revision = [text_as_list[revision_marker + 1:revision_software_marker - 1],
                text_as_list[revision_software_marker + 1:library_marker - 1]]
    library = [text_as_list[library_marker + 1:library_software_marker - 1], text_as_list[library_software_marker + 1:]]
    revision_list = [notetaking, referencing, revision, library]
    return revision_list
