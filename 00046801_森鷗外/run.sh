#
arcid="moriogaishu00moriuoft"

git add $arcid
git commit -a -m 'wip'

ocr ${arcid}_jp2 --begin ${arcid}_0508 --end ${arcid}_0510 --output $arcid --toml ./config.toml --ja_only

