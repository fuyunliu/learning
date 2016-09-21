
from bs4 import BeautifulSoup


html_doc = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>

    <title>许可证列表</title>
    <link href="style.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
  <table cellPadding="2" cellSpacing="2" width="100%" align="center">

        <tr><td align="center" height="30"><font size="3">安全生产许可证查询结果</font></td></tr>

        <tr><td>
                <TABLE width="100%" cellPadding="0" cellSpacing="0" style="border-left: 1px solid #C1DAD7;">
                    <tr>
                        <th class="thstyle">安全生产许可证编号</th>
                        <th class="thstyle">地区</th>
                        <th class="thstyle">企业名称</th>
                        <th class="thstyle">企业负责人</th>
                        <th class="thstyle">行    业</th>
                        <th class="thstyle">企业类别</th>
                        <th class="thstyle">矿井核定生产能力（万吨/年）</th>
                        <th class="thstyle">瓦斯等级</th>
                        <th class="thstyle">发证时间</th>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(京)ＭＫ安许证字[2005]0001</td>
                        <td class="tdstyle" align="center">北京市</td>
                        <td class="tdstyle" align="center">北京西兴隆煤矿有限公司</td>
                        <td class="tdstyle" align="center">张  京</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">3.5</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2005-03-18</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(京)ＭＫ安许证字[2005]0002</td>
                        <td class="tdstyle" align="center">北京市</td>
                        <td class="tdstyle" align="center">北京兴达煤矿</td>
                        <td class="tdstyle" align="center">宋立武</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">3.5</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2005-03-18</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(京)ＭＫ安许证字[2005]0003</td>
                        <td class="tdstyle" align="center">北京市</td>
                        <td class="tdstyle" align="center">北京振兴煤矿</td>
                        <td class="tdstyle" align="center">李文刚</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">5.0</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2005-03-18</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(京)ＭＫ安许证字[2005]0004</td>
                        <td class="tdstyle" align="center">北京市</td>
                        <td class="tdstyle" align="center">北京色树坟村煤矿</td>
                        <td class="tdstyle" align="center">王炳东</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">3.5</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2005-03-18</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(冀)ＭＫ安许证字[2005]0061</td>
                        <td class="tdstyle" align="center">河北省</td>
                        <td class="tdstyle" align="center">井陉矿区贾庄煤矿西王舍井</td>
                        <td class="tdstyle" align="center">王秋元</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">3.0</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2004-12-31</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(冀)ＭＫ安许证字[2005]0062</td>
                        <td class="tdstyle" align="center">河北省</td>
                        <td class="tdstyle" align="center">井陉矿区贾庄煤矿</td>
                        <td class="tdstyle" align="center">苏不喜</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">3.0</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2004-12-31</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(冀)ＭＫ安许证字[2004]0063</td>
                        <td class="tdstyle" align="center">河北省</td>
                        <td class="tdstyle" align="center">内邱县远大煤矿</td>
                        <td class="tdstyle" align="center">王计增</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">6.0</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2004-12-30</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(冀)ＭＫ安许证字[2005]0076</td>
                        <td class="tdstyle" align="center">河北省</td>
                        <td class="tdstyle" align="center">平泉杨树岭矿业有限公司</td>
                        <td class="tdstyle" align="center">李常海</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">30.0</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2005-01-19</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(冀)ＭＫ安许证字[2005]0070</td>
                        <td class="tdstyle" align="center">河北省</td>
                        <td class="tdstyle" align="center">井陉矿区贾庄煤矿北寨矿井</td>
                        <td class="tdstyle" align="center">王保新</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">3.0</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2005-01-13</td>
                    </tr>

                    <tr>
                        <td class="tdstyle" align="left">(冀)ＭＫ安许证字[2005]0068</td>
                        <td class="tdstyle" align="center">河北省</td>
                        <td class="tdstyle" align="center">井陉矿区贾庄煤矿贾庄西井</td>
                        <td class="tdstyle" align="center">毕麦忠</td>
                        <td class="tdstyle" align="center">煤矿</td>
                        <td class="tdstyle" align="center">乡镇煤矿</td>
                        <td class="tdstyle" align="center">3.0</td>
                        <td class="tdstyle" align="center">&nbsp;</td>
                        <td class="tdstyle" align="center">2005-01-13</td>
                    </tr>

                </TABLE>
        <tr><td>
            <table width="100%" border="0" style="margin-top:10px;">
              <tr>

                    <td align="left">&nbsp;&nbsp;4198条&nbsp;共420页</td>

                    <td align="right">第&nbsp;1&nbsp;页&nbsp;<a href="aqxkzcx_jg.jsp?currentPage=2"><img src="images/right0.gif" border=0></a>&nbsp;<a href="aqxkzcx_jg.jsp?currentPage=420"><img src="images/end0.gif" border=0></a>&nbsp;&nbsp;&nbsp;</td>

                </tr>
            </table>
        </td></tr>

    </table>
  </body>
</html>
"""

soup = BeautifulSoup(html_doc, "lxml")
