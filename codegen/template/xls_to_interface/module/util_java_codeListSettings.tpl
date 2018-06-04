package {{config.base_package}}.util.select;

/**
* ClassName: {{module.moduleNameFcu}}CodeListSettings <br/>
* Function: {{module.moduleDesc}}相关CS定义. <br/>
* Reason: TODO ADD REASON. <br/>
* Date: {{module.codeCreateTime}} <br/>
*
* @author {{config.author}}
* @version
* @since JDK 1.7
* {{config.copyrightEN}}
* {{config.copyrightCN}}版权所有.
*/

public class {{module.moduleNameFcu}}CodeListSettings {

    {% for c in module.codes %}
    /**
     * {{c.name}}
     *
     * @since JDK 1.7
     */
    public static final String[][] {{c.key}} = new String[][] {
        {% for o in c.options %}
        { "{{o.key}}", "{{o.name}}", "{{o.code}}" }{% if not loop.last %},{% endif %}
        {% endfor %}
    };

    {% endfor %}
}