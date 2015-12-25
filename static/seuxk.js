$(".button1").each(function()
{
    var clickfunc = $(this).attr('onclick').toString();
    var jhkcdm = clickfunc.split("'")[1];
    var jxbbh = clickfunc.split("'")[3];
    var xkkclx = clickfunc.split("'")[5];
    $(this).click(function(){
        alert("开始对此课进行抢课，可按F12打开控制台看抢课进度");
        var flag = true;
        alert("SEU 选课助手已打开");
        while(flag){
            $.ajax({ 
                    async:false,
                    type:"post", 
                    contentType:"application/json", 
                    url:"runSelectclassSelectionAction.action?select_jxbbh="+jxbbh+"&select_xkkclx="+xkkclx+"&select_jhkcdm="+jhkcdm, 
                    data:"{}", 
                    dataType:"json", 
                    success:function(data){ 
                        var myDate = new Date();
                        if(data.rso.isSuccess == 'false'){
                            console.log(myDate.toLocaleTimeString()+document.getElementById(jhkcdm).innerText +'选课失败');
                        }else{
                            console.log(myDate.toLocaleTimeString()+document.getElementById(jhkcdm).innerText +'选课成功');
                            flag = false;
                        }
                    }
        });
        }   
    });
});


$(".button2").each(function()
{
    var clickfunc = $(this).attr('onclick').toString();
    // console.log(clickfunc.split("'"));
    var jhkcdm = clickfunc.split("'")[1];
    var xkkclx = clickfunc.split("'")[3];
    var mkbh = clickfunc.split("'")[5];
    var ind = clickfunc.split("'")[7];
    $(this).click(function(){
        _w_table_td5_font2_Obj = $("#selectList tr:nth-child("+ ind +") td:nth-child(5) p:nth-child(2) font");
        _w_table_td5_font1_Obj = $("#selectList tr:nth-child("+ ind +") td:nth-child(5) p:nth-child(1) font");
        _w_table_td6_button3_Obj = $("#selectList tr:nth-child("+ ind +") td:nth-child(6) .button3");
        _w_table_td6_button1_Obj = $("#selectList tr:nth-child("+ ind +") td:nth-child(6) .button1");
        var obj = new Object();
        sFeatures   ="dialogWidth:"   +   window.screen.width  + ";dialogHeight:" + window.screen.height;
        obj.select_jhkcdm = jhkcdm;
        var retObj = window.open("runViewsecondSelectClassAction.action?Wv3opdZQ89ghgd88wjff43Dsdf4Fsd4SSg9FsgG49koguSd2fRVsfweSUj=" + new Date() + "&select_jhkcdm=" + jhkcdm+"&select_mkbh=" + mkbh+"&select_xkkclx="+xkkclx+"&select_dxdbz=0",obj,sFeatures);
            
            if(retObj != null && retObj.handlingtype != null){
            if(retObj.handlingtype == 'select'){
                //同模块编号下的
           /*   if(retObj.mkbh != ''){
            *       mkObj = $(".jg_"+retObj.mkbh + " p:nth-child(1) font");
            *       mkObj.text("[尚未选择]");
            *       mkObj.css("color","#FF0000");
            *       buttonObj = $(".button_"+retObj.mkbh + " #button3");
            *       buttonObj.attr("disabled","true");
            *   }
            */
                _w_table_td5_font1_Obj.text(retObj.str);
                _w_table_td5_font1_Obj.css("color","#009900");
                _w_table_td6_button3_Obj.attr("disabled",false);
                if(retObj.tjjxb == 'true'){
                    _w_table_td6_button1_Obj.attr("disabled",true);
                }
                if(retObj.zyqz != "0"){
                    _w_table_td5_font1_Obj.append("<span style='color:FF0000'>[占用权重]"+ retObj.zyqz +"</span>");
                }
                $("#select_xkjxb_"+ind).val(retObj.yxjxbbh);
            }else if(retObj.handlingtype == 'cancle'){
                _w_table_td5_font1_Obj.text("[尚未选择]");
                _w_table_td5_font1_Obj.css("color","#FF0000");
                _w_table_td6_button1_Obj.attr("disabled",false);
                _w_table_td6_button3_Obj.attr("disabled",true);
            }
            $(".Context_weightScores").text("当前剩余权重:" + retObj.syqz);
            }
    });
});

$("td[id!='']").each(function()
{
    var jxbbh = $(this).attr("id");
    if(jxbbh.toString().length == 20){
        $(this).click(function(){
        var flag = true;
        while(flag){
        $.ajax({ 
            async:false,
            type:"post", 
            contentType:"application/json", 
            url:"runSelectclassSelectionAction.action?select_jxbbh="+jxbbh+"&select_xkkclx="+$("#select_xkkclx").val()+"&select_jhkcdm="+$("#select_jhkcdm").val()+"&select_mkbh="+$("#select_mkbh").val(), 
            data:"{}", 
            dataType:"json", 
            success:function(data){ 
                var myDate = new Date();
                if(data.rso.isSuccess == 'false'){
                    console.log(myDate.toLocaleTimeString() +data.rso.errorStr);
                    return;
                }else{
                    console.log(myDate.toLocaleTimeString()+'选课成功');
                    flag = false;
                }
            }
            });
        }
    });
    }
});