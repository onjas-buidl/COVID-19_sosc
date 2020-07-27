* yuhang data -- 原来：襄樊市、莱芜市 现在已经没了..
  * 改成襄阳市 莱芜区

* CN Geodata is from: https://data.humdata.org/dataset/china-administrative-boundaries




## 观察政策和新冠数量的发现

* （河北）秦皇岛 1.25 就lockdown, 但其第一例要到2.1才被发现
* 河北唐山1.28 lockdown，刚刚发现一例
* 河北省其他一些地市 -- like 保定, interestingly, 第一例在1.25



## 观察第一例到lockdown vs. 时间

在lockdown的城市中，似乎大部分情况下第一例都发现时间较早（约等于1.24）

* 抚顺、东营、阿拉善盟：没有确诊病例但还是lockdown
  * 阿拉善盟：内蒙古全区统一lockdown
* 秦皇岛：在确诊病例出现数天前lockdown
* 绝大部分lockdown的城市在1.24前后发现第一例（数据范围有限），并在武汉lockdown后相继lockdown。
* (似乎是)统一lockdown
  * 湖北 1.24 （武汉 actually 1.23 ）
  * 辽宁（13/14城封城）：2.5
  * 山东四个城市：2.5
  * 江西（9/11城封城） [萍乡市](https://zh.wikipedia.org/wiki/萍乡市)、[九江市](https://zh.wikipedia.org/wiki/九江市)、[新余市](https://zh.wikipedia.org/wiki/新余市)、[鹰潭市](https://zh.wikipedia.org/wiki/鹰潭市)、[赣州市](https://zh.wikipedia.org/wiki/赣州市)、[吉安市](https://zh.wikipedia.org/wiki/吉安市)、[宜春市](https://zh.wikipedia.org/wiki/宜春市)、[抚州市](https://zh.wikipedia.org/wiki/抚州市)、[上饶市](https://zh.wikipedia.org/wiki/上饶市) ：2.6
  * 内蒙古全区统一lockdown -- 2.13

### Special Note on data

* 上海的新冠json数据有问题！第一次在数据集中出现是1.27（？），但是上海第一例要好早之前。



## 测量政策效果 with Baidu intra-city index

* Go though plot of each city
* 绝大部分城市都在1.20-23开始有巨大的decline 
* 一开始武汉和23号封城的几个城市效果in-city index极其显著
* 仙桃、唐山虽然晚一点封城，但是其index的decline在约22号



## Expr_official

* 实施lockdown的近100位官员 average age 偏大？
  * magnitude = 1，但是似乎是statistically significant的，因为这个级别官员本身年龄的variation并不大