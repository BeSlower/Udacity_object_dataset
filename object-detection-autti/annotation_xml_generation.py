import os
from lxml import etree

def process_label_csv(filename):
    img_dict = {}
    file = open(filename, 'r')
    for idx, line in enumerate(file.readlines()):
        # skip first line
        if idx == 0:
            continue
        print idx
        img_name, xmin, xmax, ymin, ymax, cls_ind, label = line.split(' ')[0:7]
        label = label.split('"')[1]
        if img_name in img_dict:
            img_dict[img_name].append([label, xmin, xmax, ymin, ymax])
        else:
            img_dict[img_name] = [[label, xmin, xmax, ymin, ymax]]
    print 'Process .csv file Done'
    return img_dict

def create_object_xml_node(root, object):
    label, xmin, ymin, xmax, ymax = object
    node_object = etree.SubElement(root, "object")
    # ----- properties below belongs to node: object ----- # this is only a template
    node_name = etree.SubElement(node_object, "name") # give default value:
    # label: car, truck, pedestrian
    node_name.text = label
    node_pose = etree.SubElement(node_object, "pose") # give default value: unspecified
    node_pose.text = "unspecified"
    node_truncated = etree.SubElement(node_object, "truncated") # give default value: 0
    node_truncated.text = "0"
    node_difficult = etree.SubElement(node_object, "difficult") # give default value: 1
    node_difficult.text = "0"
    node_bndbox = etree.SubElement(node_object, "bndbox") # give default value: 1
    #  ----- properties below belongs to node: bndbox ----- #
    node_xmin = etree.SubElement(node_bndbox, "xmin")
    node_xmin.text = str(xmin)
    node_ymin = etree.SubElement(node_bndbox, "ymin")
    node_ymin.text = str(ymin)
    node_xmax = etree.SubElement(node_bndbox, "xmax")
    node_xmax.text = str(xmax)
    node_ymax = etree.SubElement(node_bndbox, "ymax")
    node_ymax.text = str(ymax)
    # ----- properties above belongs to node: bndbox ----- #
    return root

def create_annotation_for_one_img(img_name):
    root = etree.Element("annotation")

    node_folder = etree.SubElement(root, "folder")  # give default value: Udacity object
    node_folder.text = "VOC2007"

    node_filename = etree.SubElement(root, "filename")  # one parameter
    node_filename.text = img_name

    node_source = etree.SubElement(root, "source")
    # ----- properties below belongs to node: source ----- #
    node_database = etree.SubElement(node_source, "database")  # give default value: Udacity object
    node_database.text = "The VOC2007 Database"

    node_annotation = etree.SubElement(node_source, "annotation")  # give default value: Udacity object
    node_annotation.text = "PASCAL VOC2007"

    node_image = etree.SubElement(node_source, "image")  # give default value: Udacity object
    node_image.text = "Udacity_object_dataset_2"
    node_flickerid = etree.SubElement(node_source, "flickerid")
    node_flickerid.text = "0000000000"
    # ----- properties above belongs to node: source ----- #

    node_owner = etree.SubElement(root, "owner")  # give default value: Udacity
    # ----- properties below belongs to node: owner ----- #
    node_owner_flickerid = etree.SubElement(node_owner, "flickerid")  # give default value: GO_BLUE
    node_owner_flickerid.text = "GO BLUE"
    node_owner_name = etree.SubElement(node_owner, "name")  # give default value: UMD_ISL
    node_owner_name.text = "UMD_ISL"
    # ----- properties above belongs to node: owner ----- #

    node_size = etree.SubElement(root, "size")
    # ----- properties below belongs to node: source ----- #
    node_width = etree.SubElement(node_size, "width")
    node_width.text = "1920"
    node_height = etree.SubElement(node_size, "height")
    node_height.text = "1200"
    node_depth = etree.SubElement(node_size, "depth")
    node_depth.text = "3"
    # ----- properties above belongs to node: source ----- #

    node_segmentation = etree.SubElement(root, "segmentation")  # give default value: 0
    node_segmentation.text = "0"
    return root

def write_into_xml(img_dict, write_dir):
    for img_name in img_dict.keys():
        # generate xml for one image
        root = create_annotation_for_one_img(img_name)

        # add object into xml
        for object in img_dict[img_name]:
            root = create_object_xml_node(root, object)

        # write file name
        xml_name = write_dir + img_name.split('.')[0] + '.xml'
        with open(xml_name, 'w') as xml:
            xml.write(etree.tostring(root, pretty_print=True))

def main():
    img_dict = process_label_csv('labels.csv')

    pwd = os.getcwd()
    write_dir = pwd + '/annotations/'
    if not os.path.exists(write_dir):
        os.mkdir(write_dir)
    write_into_xml(img_dict, write_dir)

if __name__ == '__main__':
    main()
