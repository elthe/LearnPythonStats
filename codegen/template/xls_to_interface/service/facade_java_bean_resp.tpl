package {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}};

import java.io.Serializable;
{% if service.hasBigDecimalResp %}
import java.math.BigDecimal;
{% endif %}
{% if service.hasDateResp %}
import java.util.Date;
{% endif %}
{% if service.hasListResp %}
import java.util.List;
{% endif %}

import org.apache.commons.lang.builder.ReflectionToStringBuilder;
import org.apache.commons.lang.builder.ToStringStyle;

import {{config.core_base_package}}.facade.abs.AbstractDubboResponse;
{% for c in service.respProps %}
{% if c.hasBean %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.bean.className}};
{% endif %}
{% endfor %}

/**
 * ClassName: {{service.className}}Resp <br/>
 * Function: {{service.desc}}返回对象类. <br/>
 * Reason: TODO ADD REASON. <br/>
 * Date: {{module.codeCreateTime}} <br/>
 *
 * @author {{config.author}}
 * @version
 * @since JDK 1.7
 * {{config.copyrightEN}}
 * {{config.copyrightCN}}版权所有.
 */
public class {{service.className}}Resp extends AbstractDubboResponse implements Serializable {

    private static final long serialVersionUID = 1L;

    {% for c in service.respProps %}
    /**
     * {{c.id}}: {{c.name}}{{c.descFormat}}.
     * @since JDK 1.7
     */
    private {{c.type}} {{c.id}};

    {% endfor %}

    {% for c in service.respProps %}
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