import numpy as np
import cv2
from glob import glob
import os, sys
import random
from copy import deepcopy

from create_xml import *


def supaiSort(su):
    return sorted(su, key=lambda x: x[0])


def hupaiSort(hu):
    ids = {"ton": 1,
           "nan": 2,
           "sha": 3,
           "pe": 4}
    iids = {1: "ton",
            2: "nan",
            3: "sha",
            4: "pe"}

    hu = [[ids[h[0]], h[1]] for h in hu]  # 数字に変換
    hu = sorted(hu, key=lambda x: x[0])  # 数字でソート
    hu = [[iids[h[0]], h[1]] for h in hu]  # 字に戻す

    return hu


def sanpaiSort(san):
    ids = {"haku": 1,
           "hatsu": 2,
           "chun": 3}

    iids = {1: "haku",
            2: "hatsu",
            3: "chun"}

    san = [[ids[s[0]], s[1]] for s in san]
    # print(san)
    san = sorted(san, key=lambda x: x[0])
    # print(san)
    san = [[iids[s[0]], s[1]] for s in san]
    # print(san)

    return san


def handSort(hand):
    _hand = deepcopy(hand)  # 最後に消しながら整理するので
    tiles = [os.path.basename(tile)[:-4] for tile in _hand]
    result = []

    man = []
    pin = []
    sou = []
    hu = []
    san = []

    # まずは牌種ごとに整理
    for i, tile in enumerate(tiles):
        if tile in ["ton", "nan", "sha", "pe"]:
            # 北にｐが含まれるので、ピンズより先に処理しておく
            hu.append([tile, i])
        elif tile in ["haku", "hatsu", "chun"]:
            # ソーズより先に三元牌を処理しておく
            san.append([tile, i])
        elif "m" in tile:
            man.append([tile, i])
        elif "p" in tile:
            pin.append([tile, i])
        elif "s" in tile:
            sou.append([tile, i])

    # 各種をソート
    if man != []:
        man = supaiSort(man)
        # print("man:", man)
        for m in man:
            result.append(_hand[m[1]])
            # del tiles[tiles.index(m)]
    if pin != []:
        pin = supaiSort(pin)
        # print("pin:", pin)
        for p in pin:
            result.append(_hand[p[1]])
            # del tiles[tiles.index(p)]
    if sou != []:
        sou = supaiSort(sou)
        # print("sou:", sou)
        for s in sou:
            result.append(_hand[s[1]])
            # del tiles[tiles.index(s)]
    if hu != []:
        hu = hupaiSort(hu)
        # print("hu:", hu)
        for h in hu:
            result.append(_hand[h[1]])
            # del tiles[tiles.index(h)]
    if san != []:
        san = sanpaiSort(san)
        for s in san:
            result.append(_hand[s[1]])
            # del tiles[tiles.index(s)]

    return result


bx = 500
by = 500
tx = 24
ty = 33
folder = "mahjong-pai"
tiles = glob(f"{folder}/*.jpg")

for num in range(1, 11):
    back = cv2.imread("mahjong-matt.jpg", 1)

    xoff = int((bx - tx * 14) / 2)
    yoff = int(by // 2 - ty // 2)

    hand = []
    for i in range(14):
        tile = random.choice(tiles)
        while hand.count(tile) >= 3:  # 槓子は考えない
            tile = random.choice(tiles)
        hand.append(tile)

    hand = handSort(hand)
    print(hand)
    # sys.exit()

    bboxes = []
    for tile in hand:
        bbox = []

        tileName = os.path.basename(tile)
        bbox.append(tileName)

        tileImg = cv2.imread(tile, 1)

        tileImg = cv2.resize(tileImg, dsize=(tx, ty))

        back[yoff:yoff + ty, xoff:xoff + tx] = tileImg

        bbox.append(xoff)  # xmin
        bbox.append(yoff)  # ymin
        bbox.append(xoff + tx)  # xmax
        bbox.append(yoff + ty)  # ymax

        xoff += tx

        bboxes.append(bbox)

    print(bboxes)
    imgName = f"{num:04d}.jpg"
    body = xmlBody(folder, imgName, bx, by, bboxes)
    with open(f"datasets/{num:04d}.xml", "w", encoding="utf-8") as f:
        f.write(xmlFormatter(body))

    cv2.imshow("", back)
    cv2.imwrite(f"datasets/{imgName}", back)
    cv2.waitKey()
    cv2.destroyAllWindows()
