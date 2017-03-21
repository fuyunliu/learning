from PIL import Image


def main():
    img1 = Image.open('img1.png')
    img2 = Image.open('img2.png')
    w1, h1 = img1.size
    w2, h2 = img2.size
    assert w1 == w2, h1 == h2

    for i in range(w1):
        for j in range(h1):
            pix1 = img1.load()[i, j]
            pix2 = img2.load()[i, j]
            a = abs(pix1[0] - pix2[0])
            b = abs(pix1[1] - pix2[1])
            c = abs(pix1[2] - pix2[2])
            if a > 60 and b > 60 and c > 60:
                print(i, j, pix1, pix2, (a, b, c))


if __name__ == '__main__':
    main()
