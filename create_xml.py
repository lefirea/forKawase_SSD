from xml.dom import minidom
from xml.etree import ElementTree as et
import re


def xmlFormatter(root):
    rs = et.tostring(root, "utf-8")
    reparsed = minidom.parseString(rs)
    pretty = re.sub(r"[\r ]+\n", "", reparsed.toprettyxml(indent="\t"))
    pretty = pretty.replace(">\n\n\t<", ">\b\t<")
    return pretty


def xmlBody(folderName, imgName, imgWidth, imgHeight, bboxes):
    # ルートタグ（annotation）
    root = et.Element("annotation")

    # ルートタグ内の記述
    folderTag = et.SubElement(root, "folder")
    folderTag.text = folderName

    filenameTag = et.SubElement(root, "filename")
    filenameTag.text = imgName

    sourceTag = et.SubElement(root, "source")

    """ ↓↓↓ ルートタグ内のsourceタグ内の記述 ↓↓↓ """
    databaseTag = et.SubElement(sourceTag, "database")
    databaseTag.text = "mahjang-pai dataset"

    sourceAnnotationTag = et.SubElement(sourceTag, "annotation")
    sourceAnnotationTag.text = "mahjang-pai"

    imageTag = et.SubElement(sourceTag, "image")
    imageTag.text = "XXX"

    identificationTag = et.SubElement(sourceTag, "identification")
    identificationTag.text = "XXX"
    """ ↑↑↑ sourceタグ内の記述終わり ↑↑↑ """

    """ ↓↓↓ ルートタグ内のownerタグ内の記述 ↓↓↓ """
    ownerTag = et.SubElement(root, "owner")

    titleTag = et.SubElement(ownerTag, "title")
    titleTag.text = "XXX"

    ownerNameTag = et.SubElement(ownerTag, "name")
    """ ↑↑↑ ルートタグ内のownerタグ内の記述終わり ↑↑↑ """

    """ ↓↓↓ ルートタグ内のsizeタグ内の記述 ↓↓↓ """
    sizeTag = et.SubElement(root, "size")

    widthTag = et.SubElement(sizeTag, "width")
    widthTag.text = str(imgWidth)

    heightTag = et.SubElement(sizeTag, "height")
    heightTag.text = str(imgHeight)
    """ ↑↑↑ ルートタグ内のsizeタグ内の記述終わり ↑↑↑ """

    segmentedTag = et.SubElement(root, "segmented")
    segmentedTag.text = "0"

    for bbox in bboxes:
        """ ↓↓↓ ルートタグ内のobjectタグ内の記述 ↓↓↓ """
        objectTag = et.SubElement(root, "object")

        objectNameTag = et.SubElement(objectTag, "name")
        objectNameTag.text = str(bbox[0])

        poseTag = et.SubElement(objectTag, "pose")
        poseTag.text = "Unspecified"

        truncatedTag = et.SubElement(objectTag, "truncated")
        truncatedTag.text = "1"

        difficultTag = et.SubElement(objectTag, "difficult")
        difficultTag.text = "0"

        """ ↓↓↓ objectタグ内のbndboxタグ内の記述 ↓↓↓ """
        bboxTag = et.SubElement(objectTag, "bndbox")

        xminTag = et.SubElement(bboxTag, "xmin")
        xminTag.text = str(bbox[1])

        yminTag = et.SubElement(bboxTag, "xmin")
        yminTag.text = str(bbox[2])

        xmaxTag = et.SubElement(bboxTag, "xmin")
        xmaxTag.text = str(bbox[3])

        ymaxTag = et.SubElement(bboxTag, "xmin")
        ymaxTag.text = str(bbox[4])
        """ ↑↑↑ objectタグ内のbndboxタグ内の記述 ↑↑↑ """
        """ ↑↑↑ ルートタグ内のobjectタグ内の記述 ↑↑↑ """

    return root
