import tushare as ts
import requests
import lxml
from lxml import etree
from bs4 import BeautifulSoup
import re

ts.set_token('85a6e863fa91060204e5339228932e52c4f90863d773778f3040f14a')

g_industryPathBase = 'C:/python/csv/industry/'

get_url = 'http://q.10jqka.com.cn/thshy/'
headers = {
            #'Referer': g_ciWebPage,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            #'Host': '10.159.215.231:8080'
        }
testText = ''''
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="X-UA-Compatible" content="edge" charset="gbk"> </meta>
    <title>同花顺行业_同花顺行情中心_同花顺财经网</title>
    <meta name="keywords" content="金融,金融网,金融服务,金融网站,金融信息,金融资讯,金融信息服务,投资,金融投资,投资理财,股票"/>
    <meta name="description" content="核新同花顺网络信息股份有限公司（同花顺）成立于1995年，是一家专业的互联网金融数据服务商，为您全方位提供财经资讯及全球金融市场行情，覆盖股票、基金、期货、外汇、债券、银行、黄金等多种面向个人和企业的服务。"/>
    <link rel="stylesheet" href="http://s.thsi.cn/js/webHQ/resources/m.min.css">
        <script type="text/javascript" src="//s.thsi.cn/js/chameleon/chameleon.min.1596715.js"></script> <script type="text/javascript">
    var targetProtocol = "https:";
    if (window.location.protocol == targetProtocol)
        window.location.href = 'http:' +
        window.location.href.substring(window.location.protocol.length);
    </script>
    <link rel="stylesheet" href="http://s.thsi.cn/cb?css/q/;reset.css;common_v1.css&20161130"/>
        <link rel="stylesheet" href="http://s.thsi.cn/cb?css/q/;concept.css;/gn/common.css&20161130"/>
                
     
    <script type="text/javascript" src="http://s.thsi.cn/cb?js/sogo/jquery-1.8.3.min.js;js/ta_callback.min.20150327.js;js/webHQ/resources/excanvas.min.js&"></script>
</head>
<body>
<div class="header fixed">

    <div class="w1200">

        <div class="hdlogo">

            <a target="_blank" class="site-logo" href="http://www.10jqka.com.cn"> <img src="/images/logo-ths.jpg" title="同花顺" alt="同花顺"></a>

            <h1><a target="_blank" title="行情中心" class="sub-logo" href="http://q.10jqka.com.cn">行情中心</a></h1>

        </div>

        <div class="nav">

            <a href="http://q.10jqka.com.cn/"  data-type="hssc" class="arr-trigger ">沪深市场</a>
            <a href="http://q.10jqka.com.cn/hk/" >香港市场</a>
            <a href="http://q.10jqka.com.cn/usa/" >美国市场</a>
			<a href="http://q.10jqka.com.cn/eu/" >英国市场</a>
            <a href="http://q.10jqka.com.cn/global/" >全球股市</a>
            <a href="http://q.10jqka.com.cn/gn/" data-type="bk" class="arr-trigger cur">板块</a>
            <a href="http://q.10jqka.com.cn/xsb/" target="_blank" >新三板</a>
            <a href="http://data.10jqka.com.cn" target="_blank" data-type="sjzx" class="arr-trigger">数据中心</a>

        </div>

        <div class="sub-nav" data-type="sjzx" style="display: none;">

            <div class="triangle"></div>

            <ul class="channel clearfix">

                <li class="cur"><a href="http://data.10jqka.com.cn/market/longhu/" target="_blank">龙虎榜</a></li>

                <li><a href="http://data.10jqka.com.cn/market/dzjy/" target="_blank">大宗交易</a></li>

                <li><a href="http://data.10jqka.com.cn/ipo/xgsgyzq/" target="_blank">新股申购</a></li>

                <li><a href="http://data.10jqka.com.cn/market/xsjj/" target="_blank">限售解禁</a></li>

                <li><a href="http://data.10jqka.com.cn/financial/yjyg/" target="_blank">财务分析</a></li>

                <li><a href="http://data.10jqka.com.cn/hgt/hgtb/" target="_blank">沪港通</a></li>

                <li><a href="http://data.10jqka.com.cn/funds/ggzjl/" target="_blank">资金流向</a></li>

                <li><a href="http://data.10jqka.com.cn/tradetips/mrtbts/" target="_blank">交易提示</a></li>

                <li><a href="http://data.10jqka.com.cn/rank/cxg/" target="_blank">技术选股</a></li>

                <li><a href="http://data.10jqka.com.cn/market/ggsd/" target="_blank">公告速递</a></li>

                <li><a href="http://data.10jqka.com.cn/market/rzrq/" target="_blank">融资融券</a></li>

                <li><a href="http://data.10jqka.com.cn/gzqh/" target="_blank">股指期货</a></li>

            </ul>

        </div>
        
        <div class="sub-nav" data-type="bk" style="display: none;">

            <div class="triangle"></div>

            <ul class="channel clearfix">
                <li ><a href="http://q.10jqka.com.cn/gn/" target="_blank">概念板块</a></li>
                <li ><a href="http://q.10jqka.com.cn/dy/" target="_blank">地域板块</a></li>
                <li class="cur"><a href="http://q.10jqka.com.cn/thshy/" target="_blank">同花顺行业</a></li>
                <li ><a href="http://q.10jqka.com.cn/zjhhy/" target="_blank">证监会行业</a></li>

            </ul>
        </div>
        
        <div class="sub-nav" data-type="hssc" style="display: none;">
            <div class="triangle"></div>
            <ul class="channel clearfix">
                <li ><a href="http://q.10jqka.com.cn/" target="_blank">沪深市场</a></li>
                <li ><a href="http://q.10jqka.com.cn/zs/" target="_blank">沪深指数</a></li>
                <li ><a href="http://q.10jqka.com.cn/index/fxjs/" target="_blank">风险警示</a></li>
            </ul>
        </div>

        <div class="login-box">

            <a href="http://upass.10jqka.com.cn/login?redir=HTTP_REFERER" target="_blank">登录</a>

        </div>

        <div class="logined_box hide fr">

            <a href="http://stock.10jqka.com.cn/my/" target="_blank" id="J_username" style="background-position: 100% 40px;">linhanzi</a>

            <span>|</span>

            <a href="javascript:;" id="header_logined_out" target="_self" class="homeloginout">退出</a>

        </div>

    </div>

</div><div class="container w1200">
<div class="category boxShadow m_links">
        <div class="cate_inner visible">
                        <div class="cate_group">
                <span class="cate_letter">A~E</span>
                <div class="cate_items">
                                         <a href="http://q.10jqka.com.cn/thshy/detail/code/881121/" target="_blank">半导体及元件</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881131/" target="_blank">白色家电</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881156/" target="_blank">保险及其他</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881138/" target="_blank">包装印刷</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881107/" target="_blank">采掘服务</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881164/" target="_blank">传媒</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881145/" target="_blank">电力</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881120/" target="_blank">电气设备</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881124/" target="_blank">电子制造</a>
                                    </div>
            </div>
                        <div class="cate_group">
                <span class="cate_letter">F~J</span>
                <div class="cate_items">
                                         <a href="http://q.10jqka.com.cn/thshy/detail/code/881153/" target="_blank">房地产开发</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881127/" target="_blank">非汽车交运</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881136/" target="_blank">服装家纺</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881135/" target="_blank">纺织制造</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881166/" target="_blank">国防军工</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881150/" target="_blank">公交</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881148/" target="_blank">港口航运</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881149/" target="_blank">公路铁路运输</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881112/" target="_blank">钢铁</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881122/" target="_blank">光学光电子</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881147/" target="_blank">环保工程</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881110/" target="_blank">化工合成材料</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881111/" target="_blank">化工新材料</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881109/" target="_blank">化学制品</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881140/" target="_blank">化学制药</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881108/" target="_blank">基础化学</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881151/" target="_blank">机场航运</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881161/" target="_blank">酒店及餐饮</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881160/" target="_blank">景点及旅游</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881130/" target="_blank">计算机设备</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881163/" target="_blank">计算机应用</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881139/" target="_blank">家用轻工</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881128/" target="_blank">交运设备服务</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881115/" target="_blank">建筑材料</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881116/" target="_blank">建筑装饰</a>
                                    </div>
            </div>
                        <div class="cate_group">
                <span class="cate_letter">K~O</span>
                <div class="cate_items">
                                         <a href="http://q.10jqka.com.cn/thshy/detail/code/881158/" target="_blank">零售</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881105/" target="_blank">煤炭开采加工</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881159/" target="_blank">贸易</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881103/" target="_blank">农产品加工</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881104/" target="_blank">农业服务</a>
                                    </div>
            </div>
                        <div class="cate_group">
                <span class="cate_letter">P~T</span>
                <div class="cate_items">
                                         <a href="http://q.10jqka.com.cn/thshy/detail/code/881126/" target="_blank">汽车零部件</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881125/" target="_blank">汽车整车</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881123/" target="_blank">其他电子</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881146/" target="_blank">燃气水务</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881134/" target="_blank">食品加工制造</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881132/" target="_blank">视听器材</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881142/" target="_blank">生物制品</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881106/" target="_blank">石油矿业开采</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881162/" target="_blank">通信服务</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881129/" target="_blank">通信设备</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881117/" target="_blank">通用设备</a>
                                    </div>
            </div>
                        <div class="cate_group">
                <span class="cate_letter">U~Z</span>
                <div class="cate_items">
                                         <a href="http://q.10jqka.com.cn/thshy/detail/code/881152/" target="_blank">物流</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881114/" target="_blank">新材料</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881144/" target="_blank">医疗器械服务</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881133/" target="_blank">饮料制造</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881154/" target="_blank">园区开发</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881119/" target="_blank">仪器仪表</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881113/" target="_blank">有色冶炼加工</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881155/" target="_blank">银行</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881143/" target="_blank">医药商业</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881102/" target="_blank">养殖业</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881165/" target="_blank">综合</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881157/" target="_blank">证券</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881141/" target="_blank">中药</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881118/" target="_blank">专用设备</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881137/" target="_blank">造纸</a>
                                        <a href="http://q.10jqka.com.cn/thshy/detail/code/881101/" target="_blank">种植业与林业</a>
                                    </div>
            </div>
                       
        </div>
    </div>
    <!-- <div class="cate_toggle_wrap">
        <a class="cate_toggle boxShadow" href="javascript: void(0)">展开全部</a>
    </div> -->

<div class="box">
    <div class="head">
        <h2>同花顺行业一览表</h2>
    </div>
    <div class="body m-pager-box" id="maincont" data-fixedthead="true">
        
        <table class="m-table m-pager-table">
            <thead>
            <tr>
                <th width="5%">序号</th>
                <th width="8%">板块</th>
                <th width="10%" class='cur'><a href="javascript:void(0)" field="199112" order="desc"  class="desc">涨跌幅(%)<i></i></a></th>
                <th width="10%" ><a href="javascript:void(0)" field="13" >总成交量（万手）<i></i></a></th>
                <th width="10%" ><a href="javascript:void(0)" field="19" >总成交额（亿元）<i></i></a></th>
                <th width="10%" ><a href="javascript:void(0)" field="zjjlr" >净流入（亿元）<i></i></a></th>
                <th width="5%">上涨家数</th>
                <th width="5%">下跌家数</th>   
                <th width="8%" ><a href="javascript:void(0)" field="330184" >均价<i></i></a></th>             
                <th width="10%">领涨股</th>
                <th width="8%">最新价</th>
                <th width="10%">涨跌幅(%)</th>
            </tr>
            </thead>
            <tbody>
                         <tr>
                <td>1</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881150/" target="_blank">公交</a></td>
                <td class="c-rise">4.86</td>
                <td>209.41</td>
                <td>34.18</td>
                <td>1.32</td>
                <td class="c-rise">7</td>
                <td class="c-fall">1</td> 
                <td>16.32</td>
                <td><a href="http://stockpage.10jqka.com.cn/600834/" target="_blank">申通地铁</a></td>     
                <td class="c-rise">14.27</td>  
                <td class="c-rise">10.02</td>                     
            </tr>
                        <tr>
                <td>2</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881166/" target="_blank">国防军工</a></td>
                <td class="c-rise">3.60</td>
                <td>3684.81</td>
                <td>700.02</td>
                <td>22.12</td>
                <td class="c-rise">58</td>
                <td class="c-fall">10</td> 
                <td>19.00</td>
                <td><a href="http://stockpage.10jqka.com.cn/300123/" target="_blank">亚光科技</a></td>     
                <td class="c-rise">23.28</td>  
                <td class="c-rise">10.02</td>                     
            </tr>
                        <tr>
                <td>3</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881157/" target="_blank">证券</a></td>
                <td class="c-rise">2.90</td>
                <td>5446.73</td>
                <td>831.61</td>
                <td>21.78</td>
                <td class="c-rise">46</td>
                <td class="c-fall">1</td> 
                <td>15.27</td>
                <td><a href="http://stockpage.10jqka.com.cn/002670/" target="_blank">国盛金控</a></td>     
                <td class="c-rise">11.19</td>  
                <td class="c-rise">10.03</td>                     
            </tr>
                        <tr>
                <td>4</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881113/" target="_blank">有色冶炼加工</a></td>
                <td class="c-rise">2.08</td>
                <td>7144.75</td>
                <td>652.37</td>
                <td>39.98</td>
                <td class="c-rise">67</td>
                <td class="c-fall">22</td> 
                <td>9.13</td>
                <td><a href="http://stockpage.10jqka.com.cn/600331/" target="_blank">宏达股份</a></td>     
                <td class="c-rise">2.93</td>  
                <td class="c-rise">10.15</td>                     
            </tr>
                        <tr>
                <td>5</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881112/" target="_blank">钢铁</a></td>
                <td class="c-rise">1.25</td>
                <td>1639.83</td>
                <td>72.23</td>
                <td>-1.64</td>
                <td class="c-rise">22</td>
                <td class="c-fall">9</td> 
                <td>4.41</td>
                <td><a href="http://stockpage.10jqka.com.cn/603995/" target="_blank">甬金股份</a></td>     
                <td class="c-rise">33.88</td>  
                <td class="c-rise">10.00</td>                     
            </tr>
                        <tr>
                <td>6</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881154/" target="_blank">园区开发</a></td>
                <td class="c-rise">1.21</td>
                <td>219.87</td>
                <td>34.70</td>
                <td>4.64</td>
                <td class="c-rise">7</td>
                <td class="c-fall">4</td> 
                <td>15.78</td>
                <td><a href="http://stockpage.10jqka.com.cn/600895/" target="_blank">张江高科</a></td>     
                <td class="c-rise">23.83</td>  
                <td class="c-rise">6.81</td>                     
            </tr>
                        <tr>
                <td>7</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881132/" target="_blank">视听器材</a></td>
                <td class="c-rise">1.17</td>
                <td>310.29</td>
                <td>19.06</td>
                <td>0.47</td>
                <td class="c-rise">5</td>
                <td class="c-fall">2</td> 
                <td>6.14</td>
                <td><a href="http://stockpage.10jqka.com.cn/603996/" target="_blank">中新科技</a></td>     
                <td class="c-rise">2.64</td>  
                <td class="c-rise">5.18</td>                     
            </tr>
                        <tr>
                <td>8</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881130/" target="_blank">计算机设备</a></td>
                <td class="c-rise">1.01</td>
                <td>1613.12</td>
                <td>299.48</td>
                <td>5.65</td>
                <td class="c-rise">30</td>
                <td class="c-fall">19</td> 
                <td>18.57</td>
                <td><a href="http://stockpage.10jqka.com.cn/300368/" target="_blank">汇金股份</a></td>     
                <td class="c-rise">12.86</td>  
                <td class="c-rise">10.01</td>                     
            </tr>
                        <tr>
                <td>9</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881125/" target="_blank">汽车整车</a></td>
                <td class="c-rise">0.95</td>
                <td>701.20</td>
                <td>71.63</td>
                <td>0.60</td>
                <td class="c-rise">16</td>
                <td class="c-fall">7</td> 
                <td>10.22</td>
                <td><a href="http://stockpage.10jqka.com.cn/000572/" target="_blank">ST海马</a></td>     
                <td class="c-rise">3.29</td>  
                <td class="c-rise">5.11</td>                     
            </tr>
                        <tr>
                <td>10</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881156/" target="_blank">保险及其他</a></td>
                <td class="c-rise">0.93</td>
                <td>1211.37</td>
                <td>187.15</td>
                <td>-0.46</td>
                <td class="c-rise">24</td>
                <td class="c-fall">12</td> 
                <td>15.45</td>
                <td><a href="http://stockpage.10jqka.com.cn/600318/" target="_blank">新力金融</a></td>     
                <td class="c-rise">14.42</td>  
                <td class="c-rise">6.97</td>                     
            </tr>
                        <tr>
                <td>11</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881121/" target="_blank">半导体及元件</a></td>
                <td class="c-rise">0.85</td>
                <td>2477.05</td>
                <td>842.24</td>
                <td>30.08</td>
                <td class="c-rise">52</td>
                <td class="c-fall">46</td> 
                <td>34.00</td>
                <td><a href="http://stockpage.10jqka.com.cn/300460/" target="_blank">惠伦晶体</a></td>     
                <td class="c-rise">14.94</td>  
                <td class="c-rise">10.02</td>                     
            </tr>
                        <tr>
                <td>12</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881165/" target="_blank">综合</a></td>
                <td class="c-rise">0.76</td>
                <td>626.59</td>
                <td>47.97</td>
                <td>-8.52</td>
                <td class="c-rise">16</td>
                <td class="c-fall">14</td> 
                <td>7.66</td>
                <td><a href="http://stockpage.10jqka.com.cn/002967/" target="_blank">广电计量</a></td>     
                <td class="c-rise">34.43</td>  
                <td class="c-rise">10.00</td>                     
            </tr>
                        <tr>
                <td>13</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881114/" target="_blank">新材料</a></td>
                <td class="c-rise">0.73</td>
                <td>1004.90</td>
                <td>135.20</td>
                <td>0.61</td>
                <td class="c-rise">20</td>
                <td class="c-fall">16</td> 
                <td>13.46</td>
                <td><a href="http://stockpage.10jqka.com.cn/300855/" target="_blank">图南股份</a></td>     
                <td class="c-rise">39.23</td>  
                <td class="c-rise">10.01</td>                     
            </tr>
                        <tr>
                <td>14</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881106/" target="_blank">石油矿业开采</a></td>
                <td class="c-rise">0.65</td>
                <td>568.76</td>
                <td>25.85</td>
                <td>-0.77</td>
                <td class="c-rise">8</td>
                <td class="c-fall">4</td> 
                <td>4.54</td>
                <td><a href="http://stockpage.10jqka.com.cn/601969/" target="_blank">海南矿业</a></td>     
                <td class="c-rise">6.47</td>  
                <td class="c-rise">10.03</td>                     
            </tr>
                        <tr>
                <td>15</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881163/" target="_blank">计算机应用</a></td>
                <td class="c-rise">0.61</td>
                <td>4128.26</td>
                <td>774.84</td>
                <td>-11.64</td>
                <td class="c-rise">108</td>
                <td class="c-fall">95</td> 
                <td>18.77</td>
                <td><a href="http://stockpage.10jqka.com.cn/688004/" target="_blank">博汇科技</a></td>     
                <td class="c-rise">89.01</td>  
                <td class="c-rise">11.96</td>                     
            </tr>
                        <tr>
                <td>16</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881155/" target="_blank">银行</a></td>
                <td class="c-rise">0.56</td>
                <td>2307.34</td>
                <td>197.46</td>
                <td>-6.08</td>
                <td class="c-rise">25</td>
                <td class="c-fall">6</td> 
                <td>8.56</td>
                <td><a href="http://stockpage.10jqka.com.cn/601838/" target="_blank">成都银行</a></td>     
                <td class="c-rise">9.25</td>  
                <td class="c-rise">4.28</td>                     
            </tr>
                        <tr>
                <td>17</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881116/" target="_blank">建筑装饰</a></td>
                <td class="c-rise">0.51</td>
                <td>2213.33</td>
                <td>163.53</td>
                <td>-9.15</td>
                <td class="c-rise">50</td>
                <td class="c-fall">71</td> 
                <td>7.39</td>
                <td><a href="http://stockpage.10jqka.com.cn/600477/" target="_blank">杭萧钢构</a></td>     
                <td class="c-rise">5.25</td>  
                <td class="c-rise">10.06</td>                     
            </tr>
                        <tr>
                <td>18</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881119/" target="_blank">仪器仪表</a></td>
                <td class="c-rise">0.39</td>
                <td>504.36</td>
                <td>54.99</td>
                <td>-1.78</td>
                <td class="c-rise">16</td>
                <td class="c-fall">19</td> 
                <td>10.90</td>
                <td><a href="http://stockpage.10jqka.com.cn/300572/" target="_blank">安车检测</a></td>     
                <td class="c-rise">77.99</td>  
                <td class="c-rise">7.29</td>                     
            </tr>
                        <tr>
                <td>19</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881108/" target="_blank">基础化学</a></td>
                <td class="c-rise">0.34</td>
                <td>2957.25</td>
                <td>209.41</td>
                <td>-2.60</td>
                <td class="c-rise">20</td>
                <td class="c-fall">33</td> 
                <td>7.08</td>
                <td><a href="http://stockpage.10jqka.com.cn/603938/" target="_blank">三孚股份</a></td>     
                <td class="c-rise">28.93</td>  
                <td class="c-rise">10.00</td>                     
            </tr>
                        <tr>
                <td>20</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881151/" target="_blank">机场航运</a></td>
                <td class="c-rise">0.33</td>
                <td>692.26</td>
                <td>40.02</td>
                <td>-0.17</td>
                <td class="c-rise">6</td>
                <td class="c-fall">6</td> 
                <td>5.78</td>
                <td><a href="http://stockpage.10jqka.com.cn/600221/" target="_blank">海航控股</a></td>     
                <td class="c-rise">1.66</td>  
                <td class="c-rise">5.06</td>                     
            </tr>
                        <tr>
                <td>21</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881122/" target="_blank">光学光电子</a></td>
                <td class="c-rise">0.25</td>
                <td>4401.60</td>
                <td>363.19</td>
                <td>9.67</td>
                <td class="c-rise">31</td>
                <td class="c-fall">44</td> 
                <td>8.25</td>
                <td><a href="http://stockpage.10jqka.com.cn/600363/" target="_blank">联创光电</a></td>     
                <td class="c-rise">23.39</td>  
                <td class="c-rise">10.02</td>                     
            </tr>
                        <tr>
                <td>22</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881118/" target="_blank">专用设备</a></td>
                <td class="c-rise">0.24</td>
                <td>2348.55</td>
                <td>292.52</td>
                <td>-23.21</td>
                <td class="c-rise">79</td>
                <td class="c-fall">103</td> 
                <td>12.46</td>
                <td><a href="http://stockpage.10jqka.com.cn/002689/" target="_blank">远大智能</a></td>     
                <td class="c-rise">4.13</td>  
                <td class="c-rise">10.13</td>                     
            </tr>
                        <tr>
                <td>23</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881115/" target="_blank">建筑材料</a></td>
                <td class="c-rise">0.23</td>
                <td>1281.14</td>
                <td>179.09</td>
                <td>-10.30</td>
                <td class="c-rise">26</td>
                <td class="c-fall">41</td> 
                <td>13.98</td>
                <td><a href="http://stockpage.10jqka.com.cn/600876/" target="_blank">洛阳玻璃</a></td>     
                <td class="c-rise">18.67</td>  
                <td class="c-rise">10.02</td>                     
            </tr>
                        <tr>
                <td>24</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881117/" target="_blank">通用设备</a></td>
                <td class="c-rise">0.21</td>
                <td>1587.09</td>
                <td>180.02</td>
                <td>-6.58</td>
                <td class="c-rise">54</td>
                <td class="c-fall">66</td> 
                <td>11.34</td>
                <td><a href="http://stockpage.10jqka.com.cn/300554/" target="_blank">三超新材</a></td>     
                <td class="c-rise">27.73</td>  
                <td class="c-rise">10.00</td>                     
            </tr>
                        <tr>
                <td>25</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881139/" target="_blank">家用轻工</a></td>
                <td class="c-rise">0.14</td>
                <td>682.60</td>
                <td>77.25</td>
                <td>-3.43</td>
                <td class="c-rise">26</td>
                <td class="c-fall">41</td> 
                <td>11.32</td>
                <td><a href="http://stockpage.10jqka.com.cn/300729/" target="_blank">乐歌股份</a></td>     
                <td class="c-rise">68.65</td>  
                <td class="c-rise">10.00</td>                     
            </tr>
                        <tr>
                <td>26</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881149/" target="_blank">公路铁路运输</a></td>
                <td class="c-rise">0.11</td>
                <td>425.23</td>
                <td>31.37</td>
                <td>-1.18</td>
                <td class="c-rise">6</td>
                <td class="c-fall">15</td> 
                <td>7.38</td>
                <td><a href="http://stockpage.10jqka.com.cn/000828/" target="_blank">东莞控股</a></td>     
                <td class="c-rise">13.75</td>  
                <td class="c-rise">10.00</td>                     
            </tr>
                        <tr>
                <td>27</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881123/" target="_blank">其他电子</a></td>
                <td class="c-rise">0.08</td>
                <td>475.90</td>
                <td>92.01</td>
                <td>-5.71</td>
                <td class="c-rise">12</td>
                <td class="c-fall">21</td> 
                <td>19.34</td>
                <td><a href="http://stockpage.10jqka.com.cn/300747/" target="_blank">锐科激光</a></td>     
                <td class="c-rise">112</td>  
                <td class="c-rise">5.02</td>                     
            </tr>
                        <tr>
                <td>28</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881153/" target="_blank">房地产开发</a></td>
                <td class="c-rise">0.06</td>
                <td>2671.93</td>
                <td>204.22</td>
                <td>-20.73</td>
                <td class="c-rise">37</td>
                <td class="c-fall">71</td> 
                <td>7.64</td>
                <td><a href="http://stockpage.10jqka.com.cn/000616/" target="_blank">海航投资</a></td>     
                <td class="c-rise">3.16</td>  
                <td class="c-rise">10.11</td>                     
            </tr>
                        <tr>
                <td>29</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881126/" target="_blank">汽车零部件</a></td>
                <td class="c-fall">-0.00</td>
                <td>2084.61</td>
                <td>261.04</td>
                <td>-9.76</td>
                <td class="c-rise">53</td>
                <td class="c-fall">75</td> 
                <td>12.52</td>
                <td><a href="http://stockpage.10jqka.com.cn/600960/" target="_blank">渤海汽车</a></td>     
                <td class="c-rise">3.81</td>  
                <td class="c-rise">10.12</td>                     
            </tr>
                        <tr>
                <td>30</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881127/" target="_blank">非汽车交运</a></td>
                <td class="c-fall">-0.02</td>
                <td>350.61</td>
                <td>31.52</td>
                <td>-3.04</td>
                <td class="c-rise">10</td>
                <td class="c-fall">17</td> 
                <td>8.99</td>
                <td><a href="http://stockpage.10jqka.com.cn/002105/" target="_blank">信隆健康</a></td>     
                <td class="c-rise">10.09</td>  
                <td class="c-rise">5.54</td>                     
            </tr>
                        <tr>
                <td>31</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881147/" target="_blank">环保工程</a></td>
                <td class="c-fall">-0.12</td>
                <td>959.26</td>
                <td>79.72</td>
                <td>-8.08</td>
                <td class="c-rise">22</td>
                <td class="c-fall">43</td> 
                <td>8.31</td>
                <td><a href="http://stockpage.10jqka.com.cn/300263/" target="_blank">隆华科技</a></td>     
                <td class="c-rise">9.52</td>  
                <td class="c-rise">5.78</td>                     
            </tr>
                        <tr>
                <td>32</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881137/" target="_blank">造纸</a></td>
                <td class="c-fall">-0.24</td>
                <td>388.69</td>
                <td>40.17</td>
                <td>-2.62</td>
                <td class="c-rise">7</td>
                <td class="c-fall">9</td> 
                <td>10.34</td>
                <td><a href="http://stockpage.10jqka.com.cn/600966/" target="_blank">博汇纸业</a></td>     
                <td class="c-rise">14.35</td>  
                <td class="c-rise">5.98</td>                     
            </tr>
                        <tr>
                <td>33</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881159/" target="_blank">贸易</a></td>
                <td class="c-fall">-0.26</td>
                <td>683.38</td>
                <td>28.97</td>
                <td>-3.16</td>
                <td class="c-rise">10</td>
                <td class="c-fall">15</td> 
                <td>4.24</td>
                <td><a href="http://stockpage.10jqka.com.cn/600981/" target="_blank">汇鸿集团</a></td>     
                <td class="c-rise">3.89</td>  
                <td class="c-rise">9.89</td>                     
            </tr>
                        <tr>
                <td>34</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881105/" target="_blank">煤炭开采加工</a></td>
                <td class="c-fall">-0.36</td>
                <td>878.08</td>
                <td>48.65</td>
                <td>-6.27</td>
                <td class="c-rise">8</td>
                <td class="c-fall">23</td> 
                <td>5.54</td>
                <td><a href="http://stockpage.10jqka.com.cn/000571/" target="_blank">*ST大洲</a></td>     
                <td class="c-rise">3.93</td>  
                <td class="c-rise">4.52</td>                     
            </tr>
                        <tr>
                <td>35</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881152/" target="_blank">物流</a></td>
                <td class="c-fall">-0.36</td>
                <td>561.97</td>
                <td>60.59</td>
                <td>-5.21</td>
                <td class="c-rise">11</td>
                <td class="c-fall">27</td> 
                <td>10.78</td>
                <td><a href="http://stockpage.10jqka.com.cn/002210/" target="_blank">*ST飞马</a></td>     
                <td class="c-rise">2.73</td>  
                <td class="c-rise">5.00</td>                     
            </tr>
                        <tr>
                <td>36</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881129/" target="_blank">通信设备</a></td>
                <td class="c-fall">-0.39</td>
                <td>1850.92</td>
                <td>279.41</td>
                <td>-22.67</td>
                <td class="c-rise">33</td>
                <td class="c-fall">68</td> 
                <td>15.10</td>
                <td><a href="http://stockpage.10jqka.com.cn/300531/" target="_blank">优博讯</a></td>     
                <td class="c-rise">23.41</td>  
                <td class="c-rise">10.01</td>                     
            </tr>
                        <tr>
                <td>37</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881120/" target="_blank">电气设备</a></td>
                <td class="c-fall">-0.39</td>
                <td>4125.66</td>
                <td>518.07</td>
                <td>-47.41</td>
                <td class="c-rise">61</td>
                <td class="c-fall">141</td> 
                <td>12.56</td>
                <td><a href="http://stockpage.10jqka.com.cn/002506/" target="_blank">协鑫集成</a></td>     
                <td class="c-rise">3.77</td>  
                <td class="c-rise">9.91</td>                     
            </tr>
                        <tr>
                <td>38</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881161/" target="_blank">酒店及餐饮</a></td>
                <td class="c-fall">-0.49</td>
                <td>73.02</td>
                <td>10.23</td>
                <td>-0.91</td>
                <td class="c-rise">4</td>
                <td class="c-fall">5</td> 
                <td>14.01</td>
                <td><a href="http://stockpage.10jqka.com.cn/601007/" target="_blank">金陵饭店</a></td>     
                <td class="c-rise">9.05</td>  
                <td class="c-rise">2.84</td>                     
            </tr>
                        <tr>
                <td>39</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881145/" target="_blank">电力</a></td>
                <td class="c-fall">-0.49</td>
                <td>1624.82</td>
                <td>84.50</td>
                <td>-11.85</td>
                <td class="c-rise">15</td>
                <td class="c-fall">50</td> 
                <td>5.20</td>
                <td><a href="http://stockpage.10jqka.com.cn/002256/" target="_blank">*ST兆新</a></td>     
                <td class="c-rise">1.33</td>  
                <td class="c-rise">4.72</td>                     
            </tr>
                        <tr>
                <td>40</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881111/" target="_blank">化工新材料</a></td>
                <td class="c-fall">-0.54</td>
                <td>369.91</td>
                <td>65.77</td>
                <td>-1.89</td>
                <td class="c-rise">7</td>
                <td class="c-fall">9</td> 
                <td>17.78</td>
                <td><a href="http://stockpage.10jqka.com.cn/300196/" target="_blank">长海股份</a></td>     
                <td class="c-rise">15.04</td>  
                <td class="c-rise">4.30</td>                     
            </tr>
                        <tr>
                <td>41</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881109/" target="_blank">化学制品</a></td>
                <td class="c-fall">-0.56</td>
                <td>2901.09</td>
                <td>404.32</td>
                <td>-27.58</td>
                <td class="c-rise">57</td>
                <td class="c-fall">142</td> 
                <td>13.94</td>
                <td><a href="http://stockpage.10jqka.com.cn/002748/" target="_blank">世龙实业</a></td>     
                <td class="c-rise">8.65</td>  
                <td class="c-rise">10.05</td>                     
            </tr>
                        <tr>
                <td>42</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881140/" target="_blank">化学制药</a></td>
                <td class="c-fall">-0.59</td>
                <td>2198.56</td>
                <td>429.63</td>
                <td>-41.85</td>
                <td class="c-rise">32</td>
                <td class="c-fall">81</td> 
                <td>19.54</td>
                <td><a href="http://stockpage.10jqka.com.cn/002550/" target="_blank">千红制药</a></td>     
                <td class="c-rise">5.59</td>  
                <td class="c-rise">10.04</td>                     
            </tr>
                        <tr>
                <td>43</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881131/" target="_blank">白色家电</a></td>
                <td class="c-fall">-0.64</td>
                <td>860.49</td>
                <td>160.63</td>
                <td>-19.29</td>
                <td class="c-rise">15</td>
                <td class="c-fall">35</td> 
                <td>18.67</td>
                <td><a href="http://stockpage.10jqka.com.cn/300824/" target="_blank">北鼎股份</a></td>     
                <td class="c-rise">33.3</td>  
                <td class="c-rise">10.01</td>                     
            </tr>
                        <tr>
                <td>44</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881124/" target="_blank">电子制造</a></td>
                <td class="c-fall">-0.75</td>
                <td>1460.81</td>
                <td>342.22</td>
                <td>-20.92</td>
                <td class="c-rise">19</td>
                <td class="c-fall">50</td> 
                <td>23.43</td>
                <td><a href="http://stockpage.10jqka.com.cn/300083/" target="_blank">创世纪</a></td>     
                <td class="c-rise">11.36</td>  
                <td class="c-rise">6.97</td>                     
            </tr>
                        <tr>
                <td>45</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881143/" target="_blank">医药商业</a></td>
                <td class="c-fall">-0.75</td>
                <td>629.81</td>
                <td>95.37</td>
                <td>-10.44</td>
                <td class="c-rise">9</td>
                <td class="c-fall">17</td> 
                <td>15.14</td>
                <td><a href="http://stockpage.10jqka.com.cn/600090/" target="_blank">同济堂</a></td>     
                <td class="c-rise">2.06</td>  
                <td class="c-rise">5.10</td>                     
            </tr>
                        <tr>
                <td>46</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881148/" target="_blank">港口航运</a></td>
                <td class="c-fall">-0.78</td>
                <td>830.12</td>
                <td>49.31</td>
                <td>-6.41</td>
                <td class="c-rise">8</td>
                <td class="c-fall">20</td> 
                <td>5.94</td>
                <td><a href="http://stockpage.10jqka.com.cn/600279/" target="_blank">重庆港九</a></td>     
                <td class="c-rise">4.41</td>  
                <td class="c-rise">2.80</td>                     
            </tr>
                        <tr>
                <td>47</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881138/" target="_blank">包装印刷</a></td>
                <td class="c-fall">-0.80</td>
                <td>439.80</td>
                <td>41.89</td>
                <td>-4.74</td>
                <td class="c-rise">13</td>
                <td class="c-fall">23</td> 
                <td>9.53</td>
                <td><a href="http://stockpage.10jqka.com.cn/002836/" target="_blank">新宏泽</a></td>     
                <td class="c-rise">14.08</td>  
                <td class="c-rise">4.61</td>                     
            </tr>
                        <tr>
                <td>48</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881136/" target="_blank">服装家纺</a></td>
                <td class="c-fall">-0.84</td>
                <td>690.37</td>
                <td>45.77</td>
                <td>-6.44</td>
                <td class="c-rise">10</td>
                <td class="c-fall">42</td> 
                <td>6.63</td>
                <td><a href="http://stockpage.10jqka.com.cn/002569/" target="_blank">ST步森</a></td>     
                <td class="c-rise">15.47</td>  
                <td class="c-rise">5.02</td>                     
            </tr>
                        <tr>
                <td>49</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881107/" target="_blank">采掘服务</a></td>
                <td class="c-fall">-0.86</td>
                <td>352.19</td>
                <td>20.00</td>
                <td>-2.45</td>
                <td class="c-rise">3</td>
                <td class="c-fall">12</td> 
                <td>5.68</td>
                <td><a href="http://stockpage.10jqka.com.cn/603727/" target="_blank">博迈科</a></td>     
                <td class="c-rise">21.02</td>  
                <td class="c-rise">2.34</td>                     
            </tr>
                        <tr>
                <td>50</td>
                <td><a href="http://q.10jqka.com.cn/thshy/detail/code/881110/" target="_blank">化工合成材料</a></td>
                <td class="c-fall">-0.89</td>
                <td>1414.87</td>
                <td>149.97</td>
                <td>-16.40</td>
                <td class="c-rise">19</td>
                <td class="c-fall">51</td> 
                <td>10.60</td>
                <td><a href="http://stockpage.10jqka.com.cn/300218/" target="_blank">安利股份</a></td>     
                <td class="c-rise">12.33</td>  
                <td class="c-rise">9.99</td>                     
            </tr>
                        </tbody>
        </table>
          <input type="hidden" id="baseUrl" value='thshy/index'>
        <div class="m-pager" id="m-page">
         &nbsp;<a class="cur" page="1" href="javascript:void(0)">1</a>&nbsp;&nbsp;<a class="changePage" page="2" href="javascript:void(0);">2</a>&nbsp;&nbsp;<a class="changePage" page="2" href="javascript:void(0);">下一页</a><a class="changePage" page="2" href="javascript:void(0);">尾页</a><span class="page_info">1/2</span>
        </div>
           
    </div>
</div>
</div>
 <div class="bottom-map-warp">
        <div class="bottom-map clearfix">
            <dl class="item">
                <dt class="icon-pdzx">频道资讯</dt>
                <dd><a href="http://news.10jqka.com.cn/yaowen/" target="_blank">财经要闻</a></dd>
                <dd><a href="http://news.10jqka.com.cn/cjzx_list/ " target="_blank">宏观经济</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/bidu/" target="_blank">股票必读</a></dd>
                <dd><a href="http://master.10jqka.com.cn/" target="_blank">名家100</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/company.shtml" target="_blank">公司频道</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/market.shtml" target="_blank">市场频道</a></dd>
                <dd><a href="http://futures.10jqka.com.cn/" target="_blank">股指期货</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/newstock/" target="_blank">新股频道</a></dd>
                <dd><a href="http://news.10jqka.com.cn/guojicj_list/" target="_blank">国际财经</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/chuangye/" target="_blank">创业板</a></dd>
                <dd><a href="http://xinsanban.10jqka.com.cn/" target="_blank">新三板</a></dd>
                <dd><a href="http://news.10jqka.com.cn/bigdata.shtml" target="_blank">图解财经</a></dd>                
            </dl>
            <dl class="item">
                <dt class="icon-tzrd">投资热点</dt>
                <dd><a href="http://stock.10jqka.com.cn/bktt_list/" target="_blank">四大报刊</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/fupan/" target="_blank">每日复盘</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/fincalendar.shtml" target="_blank">投资日历</a></dd>
                <dd><a href="http://data.10jqka.com.cn/financial/yjyg/" target="_blank">财报大全</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/zaopan/" target="_blank">早盘必读</a></dd>
                <dd><a href="http://news.10jqka.com.cn/hudong/" target="_blank">互动平台</a></dd>
                <dd><a href="http://doctor.10jqka.com.cn/" target="_blank">牛叉诊股</a></dd>
                <dd><a href="http://data.10jqka.com.cn/tradetips/tfpts/" target="_blank">交易提示</a></dd>
                <dd><a href="http://stock.10jqka.com.cn/thsgd/" target="_blank">实时新闻</a></dd>
                <dd><a href="http://data.10jqka.com.cn/market/xsjj/" target="_blank">限售解禁</a></dd>
                <dd><a href="http://data.10jqka.com.cn/ipo/xgpt/" target="_blank">新股日历</a></dd>
                <dd><a href="http://data.10jqka.com.cn/market/ggsd/" target="_blank">公告速递</a></dd>
            </dl>
            <dl class="item">
                <dt class="icon-sjjh">数据精华</dt>
                <dd><a href="http://data.10jqka.com.cn/market/longhu/" target="_blank">龙虎榜单</a></dd>
                <dd><a href="http://data.10jqka.com.cn/market/dzjy/" target="_blank">大宗交易</a></dd>
                <dd><a href="http://data.10jqka.com.cn/market/rzrq/" target="_blank">融资融券</a></dd>
                <dd><a href="http://data.10jqka.com.cn/financial/yjyg/" target="_blank">业绩预告</a></dd>
                <dd><a href="http://data.10jqka.com.cn/funds/ggzjl/" target="_blank">个股资金</a></dd>
                <dd><a href="http://data.10jqka.com.cn/funds/ddzz/" target="_blank">大单追踪</a></dd>
                <dd><a href="http://data.10jqka.com.cn/hgt/hgtb/" target="_blank">沪港通</a></dd>
                <dd><a href="http://data.10jqka.com.cn/funds/hyzjl/" target="_blank">行业资金</a></dd>
                <dd><a href="http://data.10jqka.com.cn/ipo/xgyp/" target="_blank">新股预披</a></dd>
                <dd><a href="http://data.10jqka.com.cn/market/ggsyl/" target="_blank" class="overw">个股市盈率</a></dd>
                <dd><a href="http://data.10jqka.com.cn/rank/cxfl/" target="_blank">持续放量</a></dd>
                <dd><a href="http://data.10jqka.com.cn/rank/xstp/" target="_blank">向上突破</a></dd>
            </dl>
        </div>
    </div>		<div class="alert_box hide" id="resBox">
	        <div class="hd">
                <h2>提示</h2>
                <span class="close"></span>
            </div>
            <div class="bd warn_con">
                <p></p>
            </div> 
		</div>
<div class="bottom-link">
        <div id="footer">
            <p id="bottom-scroll-listen" data-scroll-taid="web_2bottom" class="ta-scroll-box scroll-ta-over"><a target="_blank" href="http://news.10jqka.com.cn/tzz/" rel="nofollow">投资者关系</a> 			<span class="ff">|</span> 			<a target="_blank" href="http://news.10jqka.com.cn/20100105/c61833421.shtml" rel="nofollow">关于同花顺</a> 			<span>|</span> 			<a target="_blank" href="http://download.10jqka.com.cn/">软件下载</a> 			<span>|</span> 			<a target="_blank" href="http://www.10jqka.com.cn/ia/pass_buck.php" rel="nofollow">法律声明</a> 			<span>|</span> 			<a target="_blank" href="http://www.10jqka.com.cn/hexin_license.htm" rel="nofollow">运营许可</a> 			<span>|</span> 			<a target="_blank" href="http://www.10jqka.com.cn/modules.php?name=what&amp;page=cooperate" rel="nofollow">内容合作</a> 			<span>|</span> 			<a target="_blank" href="http://www.10jqka.com.cn/hexin_contact.htm" rel="nofollow">联系我们</a> 			<span>|</span> 			<a target="_blank" href="http://news.10jqka.com.cn/link.shtml" rel="nofollow">友情链接</a> 			<span>|</span>
                <!--<a target="_blank" href="http://news.10jqka.com.cn/msg/" rel="nofollow">网友意见箱</a> 			<span>|</span> -->
                <a target="_blank" href="http://job.10jqka.com.cn/" rel="nofollow">招聘英才</a> 			<span class="ff">|</span> 			<a target="_blank" href="http://vote.10jqka.com.cn/webvote/suggest.html" rel="nofollow">用户体验计划</a></p> <p class="c333">不良信息举报电话：(0571)88933003 			<a href=" mailto:jubao@myhexin.com" class="smarterwiki-linkify">举报邮箱：jubao@myhexin.com</a> 			增值电信业务经营许可证：B2-20080207</p> <p class="c333">CopyrightHithink RoyalFlush Information Network Co.,Ltd. All rights reserved. 浙江核新同花顺网络信息股份有限公司版权所有</p> <p class="c333">ICP证： 			<a href="http://www.miitbeian.gov.cn/" target="_blank">浙ICP备09003598号</a> 			证券投资咨询服务提供：浙江同花顺云软件有限公司 （中国证监会核发证书编号：ZX0050）</p> <div id="myVerifyImageBox" class="verifyImageBox" siteid="43" style="margin-bottom:20px;"></div>

        </div>
    </div><script type="text/javascript" src="http://s.thsi.cn/cb?js/;jquery-1.8.3.min.js;ta.min.js;storage.min.js&20151106"></script>
<script type="text/javascript" src="http://s.thsi.cn/cb?js/home/;ths_core.min.js;ths_quote.min.js;ths_index_v3.3.min.js"></script>
<script type="text/javascript" src="http://s.thsi.cn/cb?js/ucenter/subMenu_v4.js"></script>
<script type="text/javascript" src="http://s.thsi.cn/js/q/newq/common_v2.1.min.js" ></script>
<script type="text/javascript" src="http://s.thsi.cn/cb?js/datacenter/rzrq/highcharts.js"></script>
<script type="text/javascript" src="http://s.thsi.cn/cb?js/webHQ/resources/require.min.js"></script>
<script type="text/javascript" src="http://s.thsi.cn/cb?js/home/v5/app/flash/;puredataprovider-gbk.js;2.0.7/drawChart.min.js"></script>
<script type="text/javascript" src="http://s.thsi.cn/cb?js/q/newq/flash.min.js"></script>
<script type="text/javascript" src="http://s.thsi.cn/js/q/newq/index2.js"></script>
<script type="text/javascript" src="http://s.thsi.cn/cb?js/q/newq/;concept.min.js&20161201"></script>
<script type="text/javascript" src="http://s.thsi.cn/js/home/v6/weblogin_v3.20170609.js"></script>

<script>

var fidId = 'hqzx_bk';

if (typeof(fidId)!="undefined" && fidId!=null) {
	TA.log({id:'qsthshy',fid:'info_gather,qcenter,'+fidId});
} else {
	TA.log({id:'qsthshy',fid:'info_gather,qcenter'});
}
	//TA.log({id: 'qsthshy',fid: 'qcenter'});
	$(function(){ 
		/*锟叫伙拷锟斤拷色*/
		$("#red_check").click(function(){
          $("body").addClass("reversedColor");

		});
		$("#green_check").click(function(){
			$("body").removeClass("reversedColor");

		});
	});	
</script>

<script src="http://s.thsi.cn/js/q/newq/main.min.js"></script>

<script>
	$(function(){
	    if($('.m-pager-box').length > 0){
	        var pager = new mpager('.m-pager-box');
	        pager.init();
	    }
	});
	
	
</script>

</body>
</html>
'''

#print(response.text)
def getAllIndustryNameAndLink():
    response = requests.get(get_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    print(response.text)
    try:
        for items in soup.find_all(class_='cate_items'):
            try:
                for link in items.find_all('a'):
                    href = link.attrs['href']
                    if href is not None:
                        print(f'name={link.string}, href={href}')
            except Exception as e:
                pass
    except Exception as e:
        pass

def getIndustryOrder():
    response = requests.get(get_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    #soup = BeautifulSoup(testText, 'lxml')
    #print(response.text)
    count = 0
    try:
        tbody = soup.find('tbody')
        try:
            for tr in tbody.find_all(name='tr'):
                href = tr.find('a')
                fudu = tr.find(class_ = re.compile('^(c-)+'))

                #获取前20个板块
                if fudu is not None and count < 20:
                    print(f'板块名字 = {href.string}, 涨幅 = {fudu.string}')
                    count += 1
                    continue
        except Exception as e:
            pass
    except Exception as e:
        pass

getIndustryOrder()

def getIndustryList():

    pro = ts.pro_api()
    #df = pro.daily(ts_code='603881.SH', start_date='20200731', end_date='20200803', fields = 'trade_date, close')

    # https://tushare.pro/document/2?doc_id=181 申万行业分类
    #获取申万一级行业列表
    df = pro.index_classify(level='L1', src='SW')
    #print(df)

    #获取申万二级行业列表
    df = pro.index_classify(level='L2', src='SW')
    #print(df)

    #获取申万三级级行业列表
    df = pro.index_classify(level='L3', src='SW')
    #print(df)

    #https: // tushare.pro / document / 2?doc_id = 182 申万行业成分构成
    #获取黄金分类的成份股
    df = pro.index_member(index_code='850531.SI')
    #print(df)

    #获取000001.SZ所属行业
    df = pro.index_member(ts_code='000001.SZ')
    #print(df)

