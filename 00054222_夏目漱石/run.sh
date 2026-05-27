#
git add 188*/*.txt
git commit -a -m 'wip'

ychar=12
param=" --ychar $ychar --choon"

main() {
  ocr 漱石全集_$1 --begin ${2}_0000 --end ${3}_0000 --output $1 $param
}
main 1883179 0161 0170 # 第1巻 (吾輩は猫である)

# main 1883187 0081 0090   #第2巻 (坊つちゃん・外七篇) 

# main 1883261 0061 0070  # 第8巻 (心・道草) 

# main 1883288 0091 0100   #第10巻 (小品集)

# main 1883306 0151 0160  # 1883318  第12巻 (文学評論) 昭11

# main 1883318 0081 0090  # 1883318  第13巻 (評論・雜篇) 昭11

# ndl=1883350
# ocr 漱石全集_$ndl --begin 0011_0000 --end 0020_0000 --output $ndl $param $*