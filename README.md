# tools
我的脚本小工具，成功有效数据输出到 stdout， 错误信息输出到 stderr
## PartMet.py 处理 eMule 的临时元文件
* 默认打印详情    
`$ PartMet.py XXX.part.met`
* 只打印 Ed2kLink    
`$ PartMet.py -l XXX.part.met`
* 只打印 Ed2kPartHashs    
`$ PartMet.py -s XXX.part.met`
## KnownMet.py 处理 eMule 的 known.met
* 默认打印所有记录    
`$ KnownMet.py known.met`
* 只打印所有记录的 Ed2kLink    
`$ KnownMet.py -l known.met`
## Known2Met.py 处理 eMule 的 known2_64.met
* 将二进制文件转换为文本文件    
`$ Known2Met.py -d known2_64.met > known2_64.txt`
* 将文本文件转换为二进制文件    
`$ Known2Met.py -e known2_64.txt > 2_known2_64.met`
## LinkCreator.py 打印 eD2k link    
`$ LinkCreator.py <File>...`
