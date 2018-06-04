package {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}};

import java.io.Serializable;
{% if bean.hasBigDecimalProp %}
import java.math.BigDecimal;
{% endif %}
{% if bean.hasDateProp %}
import java.util.Date;
{% endif %}
{% if bean.hasListProp %}
import java.util.List;
{% endif %}

import org.apache.commons.lang.builder.ReflectionToStringBuilder;
import org.apache.commons.lang.builder.ToStringStyle;

{% for c in bean.beans %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.className}};
{% endfor %}
{% if bean.hasSuperClass %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{bean.superClassName}};
{% endif %}

/**
* ClassName: {{bean.className}} <br/>
* Function: {{bean.name}}. <br/>
* Reason: TODO ADD REASON. <br/>
* Date: {{module.codeCreateTime}} <br/>
*
* @author {{config.author}}
* @version
* @since JDK 1.7
* {{config.copyrightEN}}
* {{config.copyrightCN}}版权所有.
*/
public class {{bean.className}} {% if bean.hasSuperClass %}extends {{bean.superClassName}} {% endif %}implements Serializable {

    private static final long serialVersionUID = 1L;

    {% for c in bean.props %}
    /**
     * {{c.id}}: {{c.name}}{{c.desc}}.
     * @since JDK 1.7
     */
    private {{c.type}} {{c.id}};

    {% endfor %}

    {% for c in bean.props %}
    /**
     * get{{c.idFcu}}: 获取{{c.name}}.
     *
     * @author {{config.author}}
     * @since JDK 1.7
     */
    public {{c.type}} get{{c.idFcu}}() {
        return {{c.id}};
    }

    /**
     * set{{c.idFcu}}: 设置{{c.name}}.
     *
     * @author {{config.author}}
     * @param p{{c.idFcu}} {{c.name}}
     * @since JDK 1.7
     */
    public void set{{c.idFcu}}({{c.type}} p{{c.idFcu}}) {
        this.{{c.id}} = p{{c.idFcu}};
    }

    {% endfor %}
    @Override
    public String toString() {
        return ReflectionToStringBuilder.toString(this,ToStringStyle.DEFAULT_STYLE);
    }
}