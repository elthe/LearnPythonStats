package {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}};

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import java.util.List;

import org.apache.commons.lang.builder.ReflectionToStringBuilder;
import org.apache.commons.lang.builder.ToStringStyle;

import {{config.core_base_package}}.facade.abs.AbstractLcsAppRequest;
{% for c in service.reqProps %}
{% if c.hasBean %}
import {{config.core_base_package}}.facade.bean.dubbo.{{config.package_sysname}}.{{module.moduleName}}.{{c.bean.className}};
{% endif %}
{% endfor %}

/**
 * ClassName: {{service.className}}Req <br/>
 * Function: {{service.desc}}请求对象类. <br/>
 * Reason: TODO ADD REASON. <br/>
 * Date: {{module.codeCreateTime}} <br/>
 *
 * @author {{config.author}}
 * @version
 * @since JDK 1.7
* {{config.copyrightEN}}
 * {{config.copyrightCN}}版权所有.
 */
public class {{service.className}}Req extends AbstractLcsAppRequest implements Serializable {

	private static final long serialVersionUID = 1L;

{% for c in service.reqProps %}
	/**
	 * {{c.id}}: {{c.name}} {{c.desc}}.
	 * @since JDK 1.7
	 */
	private {{c.type}} {{c.id}};

{% endfor %}

{% for c in service.reqProps %}
	/**
	 * get{{c.id|capitalize}}: 获取{{c.name}}.
	 *
	 * @author {{config.author}}
	 * @since JDK 1.7
	 */
	public {{c.type}} get{{c.id|capitalize}}() {
		return {{c.id}};
	}

	/**
	 * set{{c.id|capitalize}}: 设置{{c.name}}.
	 *
	 * @author {{config.author}}
	 * @param p{{c.id|capitalize}} {{c.name}}
	 * @since JDK 1.7
	 */
 	public void set{{c.id|capitalize}}({{c.type}} p{{c.id|capitalize}}) {
		this.{{c.id}} = p{{c.id|capitalize}};
	}

{% endfor %}
	@Override
	public String toString() {
		return ReflectionToStringBuilder.toString(this,ToStringStyle.DEFAULT_STYLE);
	}

}
