## 去掉中间所有空格的方法
{% for i in config -%}
    abcd: {{i}}
{%- endfor %}

## 同一行循环
{% for i in config %}    abcd: {{i}}{% endfor %}

## 注释
{#
    -----不会输出-----
#}

## loop变量
{% for i in config %}
{{loop.index}}/{{loop.length}} : [{{i}}]
{% endfor %}

## 原样输出
{% raw %}
<div>
    {%+ if True %}yay{% endif %}
</div>
{% endraw %}

## 缩进滤镜
<div>
    {% if True %}{{txt|indent|upper}}{% endif %}
</div>

{%+ if True %}
<!-- 1 -->
    <!-- 2 -->
    foo<!-- 3 -->
<!-- 4 -->
    <!-- 5 -->
{%+ endif %}