<p class="key">{{code.name}}</p>
<div class="val relative">
  <p class="seinp" :click="@{{code.varname}}Showlist = !@{{code.varname}}Showlist">{$ @{{code.varname}}Txt $}</p>
  <ul class="selist" :visible="@{{code.varname}}Showlist" :click="select{{code.classname}}">
{% for c in code.options %}
    <li title="{{c.key}}">{{c.name}}</li>
{% endfor %}
  </ul>
</div>


