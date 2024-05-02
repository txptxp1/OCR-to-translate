# OCR翻译

## 使用方式

这是一个用Python写的ocr翻译器

这个翻译器一共有两种识别方式

- paddleocr识别（无需联网，本地识别）
- 百度ocr识别（需联网）

百度ocr的申请方式<[OCR文字识别_免费试用_图片转文字-百度AI开放平台 (baidu.com)](https://ai.baidu.com/tech/ocr)>

以及一种翻译方式

- 腾讯TMT翻译（需联网）

<https://cloud.tencent.com/product/tmt)>

## paddleocr识别语言选择

'ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin', 'arabic', 'cyrillic', 'devanagari'

更多请参阅官方文档

<[PaddleOCRPlus/PaddleOCR-2.6: Awesome multilingual OCR toolkits based on PaddlePaddle (practical ultra lightweight OCR system, support 80+ languages recognition, provide data annotation and synthesis tools, support training and deployment among server, mobile, embedded and IoT devices) (github.com)](https://github.com/PaddleOCRPlus/PaddleOCR-2.6)>

注：第一次运行会自动下载模型所以会比较慢

## 腾讯TMT翻译语言选择

| Source | 是   | String | 源语言，支持： auto：自动识别（识别为一种语言） zh：简体中文 zh-TW：繁体中文 en：英语 ja：日语 ko：韩语 fr：法语 es：西班牙语 it：意大利语 de：德语 tr：土耳其语 ru：俄语 pt：葡萄牙语 vi：越南语 id：印尼语 th：泰语 ms：马来西亚语 ar：阿拉伯语 hi：印地语 示例值：en |
| ------ | ---- | ------ | ------------------------------------------------------------ |
| Target | 是   | String | 目标语言，各源语言的目标语言支持列表如下  zh（简体中文）：zh-TW（繁体中文）、en（英语）、ja（日语）、ko（韩语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）、vi（越南语）、id（印尼语）、th（泰语）、ms（马来语）zh-TW（繁体中文）：zh（简体中文）、en（英语）、ja（日语）、ko（韩语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）、vi（越南语）、id（印尼语）、th（泰语）、ms（马来语）en（英语）：zh（中文）、zh-TW（繁体中文）、ja（日语）、ko（韩语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）、vi（越南语）、id（印尼语）、th（泰语）、ms（马来语）、ar（阿拉伯语）、hi（印地语）ja（日语）：zh（中文）、zh-TW（繁体中文）、en（英语）、ko（韩语）ko（韩语）：zh（中文）、zh-TW（繁体中文）、en（英语）、ja（日语）fr（法语）：zh（中文）、zh-TW（繁体中文）、en（英语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）es（西班牙语）：zh（中文）、zh-TW（繁体中文）、en（英语）、fr（法语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）it（意大利语）：zh（中文）、zh-TW（繁体中文）、en（英语）、fr（法语）、es（西班牙语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）de（德语）：zh（中文）、zh-TW（繁体中文）、en（英语）、fr（法语）、es（西班牙语）、it（意大利语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）tr（土耳其语）：zh（中文）、zh-TW（繁体中文）、en（英语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、ru（俄语）、pt（葡萄牙语）ru（俄语）：zh（中文）、zh-TW（繁体中文）、en（英语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、pt（葡萄牙语）pt（葡萄牙语）：zh（中文）、zh-TW（繁体中文）、en（英语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）vi（越南语）：zh（中文）、zh-TW（繁体中文）、en（英语）id（印尼语）：zh（中文）、zh-TW（繁体中文）、en（英语）th（泰语）：zh（中文）、zh-TW（繁体中文）、en（英语）ms（马来语）：zh（中文）、zh-TW（繁体中文）、en（英语）ar（阿拉伯语）：en（英语）hi（印地语）：en（英语） |

更多请参阅<[机器翻译 文本翻译-API 文档-文档中心-腾讯云 (tencent.com)](https://cloud.tencent.com/document/product/551/15619)>

## 百度OCR语言选择

我只接入了普通（不含位置）的OCR接口

所以语言适配不清楚

建议查阅官方文档

由于没有做language_type的选择/输入框

所以请直接修改代码或者直接更换api链接



## 体量问题

由于我直接把paddleocr部署在了本地

而paddleocr所依赖的库非常的多

导致我打包的时候还得一个个导入没有hook的库

这也导致了体量直逼1G

事后会找时间解决问题的



## 优化问题

后台基本站内存100多mb

调用本地ocr默认不开启GPU加速（可直接在代码中修改）

本地运行OCR时cpu（本人cpu：e3 1230v2）占用在10-20左右



## 结语

总的来说这个翻译器在正常使用上是不如其他翻译器的

这本质上是一个练手的程序

有许多地方写的不好，以及许多地方有着无意义的全局变量

还望海涵