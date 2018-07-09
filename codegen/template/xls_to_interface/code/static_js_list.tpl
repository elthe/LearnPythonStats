{
    {{code.varname}}Showlist: false, // {{code.name}}下拉框显示
    {{code.varname}}Txt: '', // {{code.name}}显示文本
    {{code.varname}}: '', // {{code.name}}


    select{{code.classname}}: function(ev) { // 选择{{code.name}}
        var ev = ev || window.event;
        var target = ev.target || ev.srcElement;
        if (target.nodeName.toLowerCase() == "li") {
            xxxxx.{{code.varname}}Txt = target.innerText;
            xxxxx.{{code.varname}}Showlist = false;
            xxxxx.{{code.varname}} = target.title;
        }
    }
}