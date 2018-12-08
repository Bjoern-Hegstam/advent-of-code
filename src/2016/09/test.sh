#!/usr/bin/env bash

echo 'TEST - PART 1'
echo '---'
echo 'ADVENT' | main.py
echo '6 - Expected'
echo '---'
echo 'A(1x5)BC' | main.py
echo '7 - Expected'
echo '---'
echo '(3x3)XYZ' | main.py
echo '9 - Expected'
echo '---'
echo '(6x1)(1x3)A' | main.py
echo '6 - Expected'
echo '---'
echo 'X(8x2)(3x3)ABCY' | main.py
echo '18 - Expected'

echo '---'
echo 'TEST - PART 2'
echo '---'
echo '(3x3)XYZ' | main.py --part 2
echo '9 - Expected'
echo '---'
echo 'X(8x2)(3x3)ABCY' | main.py  --part 2
echo '20 - Expected'
echo '---'
echo '(27x12)(20x12)(13x14)(7x10)(1x12)A' | main.py  --part 2
echo '241920 - Expected'
echo '---'
echo '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN' | main.py  --part 2
echo '445 - Expected'