from PIL import Image
import numpy as np, cv2 as cv, os
from datetime import datetime
import random

placementss = {
    (False, False, False): [
        (97, 52),
        (132, 52),
        (176, 52),
        (185, 52),
        (221, 52),
        (265, 52),
        (274, 52),
        (310, 52),
        (345, 52),
        (381, 52),
        (434, 52),
        (470, 52),
        (513, 52),
        (523, 52),
        (559, 52)
    ],
    (False, True, False): [
        (97, 52),
        (132, 52),
        (176, 52),
        (185, 52),
        (221, 52),
        (265, 52),
        (274, 52),
        (310, 52),
        (345, 52),
        (381, 52),
        (434, 52),
        (465, 52),
        (509, 52),
        (519, 52),
        (554, 52)
    ],
    (True, False, False): [
        (97, 52),
        (127, 52),
        (171, 52),
        (181, 52),
        (216, 52),
        (260, 52),
        (270, 52),
        (305, 52),
        (341, 52),
        (376, 52),
        (430, 52),
        (465, 52),
        (509, 52),
        (519, 52),
        (554, 52)
    ],
    (True, True, False): [
        (97, 52),
        (127, 52),
        (171, 52),
        (181, 52),
        (216, 52),
        (260, 52),
        (270, 52),
        (305, 52),
        (341, 52),
        (376, 52),
        (430, 52),
        (460, 52),
        (504, 52),
        (514, 52),
        (549, 52)
    ]
}

for key in list(placementss.keys()):
    placementss[key[:2] + (True,)] = placementss[key][:-1] + [(placementss[key][-1][0] - 5, placementss[key][-1][1])]

assets = dict()

circle5 = np.array([
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0]
], dtype='uint8')

for fname in os.listdir('assets'):
    asset = cv.imread(os.path.join('assets', fname)).mean(axis=-1, keepdims=True) / 255
    boolasset = asset.astype(bool).astype('uint8').reshape(asset.shape[:2])
    dial1 = cv.dilate(boolasset, np.ones((3, 3), dtype='uint8'))
    dial2 = cv.dilate(boolasset, circle5)
    dial3 = cv.dilate(dial2, np.ones((3, 3), dtype='uint8'))
    contours = np.array(np.where(dial3 * (1 - dial2))[::-1]).transpose(1, 0)
    where = np.array(np.where(dial1)[::-1]).transpose(1, 0)
    source_pixels = np.empty_like(where)
    for i, pos in enumerate(where):
        distances = ((contours - pos) ** 2).sum(axis=1)
        source_pixels[i] = contours[np.where(distances == distances.min(axis=0, keepdims=True))[0][0]]
    assets[fname.replace('.png', '')] = {'asset': asset, 'where': where, 'source_pixels': source_pixels}


def pil2cv(img: Image.Image) -> np.ndarray:
    return np.array(img)[..., ::-1].copy()


def cv2pil(img: np.ndarray) -> Image.Image:
    return Image.fromarray(img[..., ::-1])


def days_in_month(year: int, month: int) -> int:
    for day in range(28, 32):
        try:
            datetime(year, month, day + 1)
        except ValueError:
            break
    return day


def str2date(date: str) -> datetime:
    day, month, year = map(int, date.split(' ')[0].split('.'))
    hour, minute = map(int, date.split(' ')[1].split(':'))
    month = min(max(1, month), 12)
    day = min(max(1, day), days_in_month(year, month))
    hour = min(max(0, hour), 23)
    minute = min(max(0, minute), 63)
    return datetime(year, month, day, hour, minute)


def int2str(n: int, length: int) -> str:
    s = str(n)
    assert len(s) <= length
    return '0' * (length - len(s)) + s


def date2str(date: datetime) -> str:
    return int2str(date.day, 2) + '.' + int2str(date.month, 2) + '.' + int2str(date.year, 4) + ' ' + int2str(date.hour,
                                                                                                             2) + ':' + int2str(
        date.minute, 2)


def remove_date(img: 'np.ndarray|Image.Image', date: 'str|None|datetime' = None):
    pil = isinstance(img, Image.Image)
    if pil: img = pil2cv(img)
    img_old = img
    if img.shape[1] < 600:
        img = np.zeros((img_old.shape[0], 600, 3), dtype='uint8')
        img[:, :img_old.shape[1]] = img_old
    if date is None: _, date = get_date(img)
    if isinstance(date, datetime): date = date2str(date)
    assert len(date) == 16
    short1 = (date[:2] == '11')
    short2 = (date[11:13] == '11')
    short3 = (date[-2:] == '11')
    date = date.replace(' ', '')
    for i, pos in enumerate(placementss[short1, short2, short3]):
        where = assets[date[i]]['where']
        source_pixels = assets[date[i]]['source_pixels']
        x, y = pos
        img[where[:, 1] + y, where[:, 0] + x] = img[source_pixels[:, 1] + y, source_pixels[:, 0] + x]
    img = img[:, :img_old.shape[1]]
    return cv2pil(img) if pil else img


def apply_date(img: 'np.ndarray|Image.Image', date: 'str|datetime'):
    date = proseed_time(date)
    pil = isinstance(img, Image.Image)
    if pil: img = pil2cv(img)
    img_old = img
    if img.shape[1] < 600:
        img = np.zeros((img_old.shape[0], 600, 3), dtype='uint8')
        img[:, :img_old.shape[1]] = img_old
    if isinstance(date, datetime): date = date2str(date)
    assert len(date) == 16
    assert date[2] == '.' and date[5] == '.' and date[10] == ' ' and date[13] == ':'
    assert set(date[:2] + date[3:5] + date[6:10] + date[11:13] + date[14:]).issubset('0123456789')
    short1 = (date[:2] == '11')
    short2 = (date[11:13] == '11')
    short3 = (date[-2:] == '11')
    date = date.replace(' ', '')
    for i, pos in enumerate(placementss[short1, short2, short3]):
        if date[i] == ':':
            asset = assets['_']['asset']
        else:
            asset = assets[date[i]]['asset']
        x, y = pos
        reg = img[y: y + asset.shape[0], x: x + asset.shape[1]]
        reg[...] = reg * (1 - asset) + asset * 255
    img = img[:, :img_old.shape[1]]
    return cv2pil(img) if pil else img


def proseed_time(date: 'str|datetime'):
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    # Форматирование строки
    formatted_date = f"{date.day:02d}.{date.month:02d}.{date.year} {random_hour:02d}:{random_minute:02d}"
    return formatted_date

def get_date(img: 'np.ndarray|Image.Image', _placements: 'list[tuple[int, int]]' = None) -> 'tuple[float, str]':
    if isinstance(img, Image.Image): img = pil2cv(img)
    if img.shape[1] < 600:
        img_old = img
        img = np.zeros((img_old.shape[0], 600, 3), dtype='uint8')
        img[:, :img_old.shape[1]] = img_old
    if _placements is None:
        accs = []
        dates = []
        for placements in placementss.values():
            accuracy, date = get_date(img, placements)
            accs.append(accuracy)
            dates.append(date)
        accuracy = max(accs)
        date = dates[accs.index(accuracy)]
        if date[2] != '.' or date[5] != '.' or date[13] != ':' or not set(
                date[:2] + date[3:5] + date[6:10] + date[11:13] + date[14:]).issubset('0123456789'):
            accuracy = 0
        return accuracy, date
    date = ''
    accuracy = 1
    for i, pos in enumerate(_placements):
        x, y = pos
        evals = dict()
        for c in assets:
            asset = assets[c]['asset']
            reg = img[y: y + asset.shape[0], x: x + asset.shape[1]] / 255
            eval = (reg * asset).sum() / asset.sum() + ((1 - reg) * (1 - asset)).sum() / (1 - asset).sum()
            # if _placements == placementss[False, False, False]:
            #     print(i, c, eval)
            evals[eval] = c
        c = evals[max(evals)]
        if c == '.' and i not in [2, 5]:
            evals = dict()
            for c in assets:
                asset = assets[c]['asset']
                reg = img[y: y + asset.shape[0], x: x + asset.shape[1]] / 255
                d_reg = (reg[:-2, 1:-1] - reg[2:, 1:-1]) ** 2 + (reg[1:-1:, :-2] - reg[1:-1, 2:]) ** 2
                d_asset = (asset[:-2, 1:-1] - asset[2:, 1:-1]) ** 2 + (asset[1:-1:, :-2] - asset[1:-1, 2:]) ** 2
                eval = (d_asset * d_reg).mean()
                evals[eval] = c
            c = evals[max(evals)]
        accuracy *= max(evals)
        date += c
    return accuracy, date[:10] + ' ' + date[10:]

# ii = Image.open(rf"base.jpg")
# print(type(ii))
# img = remove_date(ii)
# img.show()
# img = apply_date(img, datetime(2024, 7, 30, 0, 0))
# img.show()
