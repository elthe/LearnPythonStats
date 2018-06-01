package {{config.core_base_package}}.facade.bean.dubbo.${config.package_sysname}.${module.moduleName};

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import java.util.List;

import org.apache.commons.lang.builder.ReflectionToStringBuilder;
import org.apache.commons.lang.builder.ToStringStyle;

import ${config.core_base_package}.facade.abs.AbstractLcsAppRequest;
<#list service.reqProps as c >
<#if (c.hasBean == 'Y') >
import ${config.core_base_package}.facade.bean.dubbo.${config.package_sysname}.${module.moduleName}.${c.bean.className};
</#if>
</#list>

/**
 * ClassName: ${service.className}Req <br/>
 * Function: ${service.desc}请求对象类. <br/>
 * Reason: TODO ADD REASON. <br/>
 * Date: ${module.codeCreateTime?string("yyyy年M月d日 00:00:00")} <br/>
 *
 * @author ${config.author}
 * @version
 * @since JDK 1.7
 * Copyright (c) 2017, www.leadfund.com.cn All Rights Reserved.
 * 版权所有.
 */
public class ${service.className}Req extends AbstractLcsAppRequest implements Serializable {

	private static final long serialVersionUID = 1L;

<#list service.reqProps as c >
	/**
	 * ${c.id}: ${c.name?if_exists}${c.descFormat?if_exists}.
	 * @since JDK 1.7
	 */
	private ${c.type} ${c.id};

</#list>

<#list service.reqProps as c >
	/**
	 * get${c.idFcu}: 获取${c.name?if_exists}.
	 *
	 * @author ${config.author}
	 * @since JDK 1.7
	 */
	public ${c.type} get${c.idFcu}() {
		return ${c.id};
	}

	/**
	 * set${c.idFcu}: 设置${c.name?if_exists}.
	 *
	 * @author ${config.author}
	 * @param p${c.idFcu} ${c.name?if_exists}
	 * @since JDK 1.7
	 */
 	public void set${c.idFcu}(${c.type} p${c.idFcu}) {
		this.${c.id} = p${c.idFcu};
	}

</#list>
	@Override
	public String toString() {
		return ReflectionToStringBuilder.toString(this,ToStringStyle.DEFAULT_STYLE);
	}

}
